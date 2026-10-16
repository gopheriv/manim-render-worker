"""Self-contained CI render script for the GitHub Actions ManimGX worker.

Reads the scene code + params from env, renders with ManimGX, and writes the
result to out/render.mp4 (plus out/storyboard.png when ManimGX produces one).
Has NO project dependencies so a minimal public worker repo needs only this
file + .github/workflows/render-manimgx.yml.

Env inputs: CODE_GZ (gzip+base64 scene code), SCENE (class name), RESOLUTION
(WxH), FPS, JOB_ID. CI_RENDER_TIMEOUT overrides the render cap (seconds).
"""

import ast
import base64
import gzip
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OUT = ROOT / "out"

# ── Safety allowlist (ManimGX twin of the classic-Manim ci_render.py gate) ────
# This worker EXECUTES the dispatched scene, so an injected `import os` would
# run with the runner's permissions/secrets. Kept inlined so the worker stays
# a single self-contained file.
_ALLOWED_IMPORT_ROOTS = {
    "manimgx", "numpy", "math", "cmath", "random", "statistics",
    "itertools", "functools", "operator", "fractions", "decimal",
    "typing", "dataclasses", "collections", "enum", "string", "json",
    "__future__",
}
_BANNED_NAMES = {
    "exec", "eval", "compile", "__import__", "open", "input",
    "breakpoint", "globals", "locals", "vars",
}
_BANNED_DUNDERS = {
    "__globals__", "__builtins__", "__subclasses__", "__bases__",
    "__mro__", "__code__", "__import__", "__loader__", "__spec__",
}

# Validator shapes for workflow inputs (fail-closed before they reach a shell).
_SCENE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_RESOLUTION_RE = re.compile(r"^(\d{3,4})x(\d{3,4})$")

# Inlined twin of the fence-stripper in ci_render.py: an LLM preamble
# ("I'll fix ...:") must never become scene.py line 1. Keep in sync.
_FENCED_BLOCK_RE = re.compile(r"```[^\S\r\n]*[A-Za-z0-9_+-]*[^\S\r\n]*\r?\n(.*?)```", re.DOTALL)
_OPEN_FENCE_RE = re.compile(r"(?m)^[^\S\r\n]*```[^\S\r\n]*[A-Za-z0-9_+-]*[^\S\r\n]*\r?\n")
_STRAY_FENCE_LINE_RE = re.compile(r"(?m)^[^\S\r\n]*```.*\r?\n?")
_CODE_LINE_RE = re.compile(
    r'^[^\S\r\n]*(?:from\s+[.\w]|import\s+\w|#|@\w|class\s+\w|(?:async\s+)?def\s+\w|"""|\'\'\')'
)


def extract_python_code(text: str) -> str:
    """Strip any LLM prose/markdown wrapping so only runnable Python remains."""
    if not text:
        return ""
    s = text.strip()
    blocks = _FENCED_BLOCK_RE.findall(s)
    if blocks:
        return max(blocks, key=lambda b: (any(k in b for k in ("import ", "class ", "def ")), len(b))).strip("\r\n")
    open_fence = _OPEN_FENCE_RE.search(s)
    if open_fence:
        s = s[open_fence.end():]
    else:
        lines = s.splitlines()
        for i, line in enumerate(lines):
            if _CODE_LINE_RE.match(line):
                s = "\n".join(lines[i:])
                break
    return _STRAY_FENCE_LINE_RE.sub("", s).strip("\r\n")


def _unsafe_reasons(code: str) -> list:
    """Safety violations (empty = safe). Syntax errors are reported later by
    the py_compile step, not here."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    reasons = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in _ALLOWED_IMPORT_ROOTS:
                    reasons.append(f"disallowed import: {a.name}")
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0] if node.level == 0 else ""
            if root not in _ALLOWED_IMPORT_ROOTS:
                reasons.append(f"disallowed import: from {'.' * node.level}{node.module or ''}")
        elif isinstance(node, ast.Name) and node.id in _BANNED_NAMES:
            reasons.append(f"disallowed builtin: {node.id}")
        elif isinstance(node, ast.Attribute) and node.attr in _BANNED_DUNDERS:
            reasons.append(f"disallowed attribute: .{node.attr}")
    seen = set()
    return [r for r in reasons if not (r in seen or seen.add(r))]


# Hard cap on the render so a generated infinite loop can't pin a runner. Must
# stay COMFORTABLY BELOW render-manimgx.yml's `timeout-minutes` (60) minus pip
# setup, so THIS graceful timeout fires before GitHub hard-cancels the job.
RENDER_TIMEOUT_S = int(os.environ.get("CI_RENDER_TIMEOUT", "1800"))  # 30 min
COMPILE_TIMEOUT_S = 60


def fail(msg: str) -> "None":
    sys.stdout.flush()
    sys.stderr.flush()
    print(msg, flush=True)
    # ::error:: is single-line: escape newlines or only the first line survives.
    annotation = msg.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print(f"::error::{annotation}", flush=True)
    sys.stdout.flush()
    sys.exit(1)


def _tail(text: str, limit: int) -> str:
    snippet = (text or "")[-limit:]
    nl = snippet.find("\n")
    if nl != -1 and len(text) > limit:
        snippet = snippet[nl + 1:]
    return snippet


def main() -> None:
    blob = os.environ.get("CODE_GZ", "")
    scene = os.environ.get("SCENE", "").strip()
    resolution = os.environ.get("RESOLUTION", "1280x720").strip() or "1280x720"
    fps = os.environ.get("FPS", "30").strip() or "30"
    job_id = os.environ.get("JOB_ID", "job").strip()
    if not blob:
        fail("CODE_GZ env is empty")
    if not _SCENE_RE.match(scene):
        fail(f"SCENE {scene!r} is not a valid Python identifier")
    if not _RESOLUTION_RE.match(resolution):
        fail(f"RESOLUTION {resolution!r} must look like 1280x720")
    try:
        fps_int = int(fps)
        if not 1 <= fps_int <= 120:
            raise ValueError
    except ValueError:
        fail(f"FPS {fps!r} must be an integer 1..120")

    try:
        code = gzip.decompress(base64.b64decode(blob)).decode("utf-8")
    except Exception as e:  # noqa: BLE001
        fail(f"could not decode CODE_GZ: {e}")

    code = extract_python_code(code)

    if "import manimgx" not in code or "def construct" not in code:
        fail("scene must 'import manimgx' and define a construct method")
    if f"class {scene}" not in code:
        fail(f"scene class {scene!r} not found in the dispatched code")

    unsafe = _unsafe_reasons(code)
    if unsafe:
        fail("unsafe code rejected: " + "; ".join(unsafe[:10]))

    scene_file = ROOT / "scene.py"
    scene_file.write_text(code, encoding="utf-8")

    try:
        pc = subprocess.run([sys.executable, "-m", "py_compile", str(scene_file)],
                            capture_output=True, text=True,
                            encoding="utf-8", errors="replace", timeout=COMPILE_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        fail(f"py_compile timed out after {COMPILE_TIMEOUT_S}s")
    if pc.returncode != 0:
        fail(f"python syntax error:\n{_tail(pc.stderr or pc.stdout, 1500)}")

    cmd = ["manimgx", "render", str(scene_file), scene,
           "-r", resolution, "--fps", str(fps_int)]
    print("Running:", " ".join(cmd), flush=True)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=RENDER_TIMEOUT_S)
    except subprocess.TimeoutExpired as e:
        partial = (e.stdout or "") + (e.stderr or "")
        if partial.strip():
            print("----- manimgx output (before timeout) -----", flush=True)
            print(partial, flush=True)
        fail(f"manimgx render timed out after {RENDER_TIMEOUT_S}s "
             "(likely an infinite loop in the generated scene)")
    if r.returncode != 0:
        print("----- manimgx stdout -----", flush=True)
        print(r.stdout or "(empty)", flush=True)
        print("----- manimgx stderr -----", flush=True)
        print(r.stderr or "(empty)", flush=True)
        fail(f"manimgx render failed (exit {r.returncode}) — see the output above")

    mp4s = sorted(ROOT.glob(f"{scene}.mp4"))
    mp4s = [p for p in mp4s if p.stat().st_size > 1024]
    if not mp4s:
        fail(f"manimgx exited 0 but no {scene}.mp4 was produced")

    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copy(mp4s[0], OUT / "render.mp4")
    storyboards = sorted(ROOT.glob(f"{scene}*.png"))
    if storyboards:
        shutil.copy(storyboards[0], OUT / "storyboard.png")
        print(f"storyboard: {storyboards[0].name}", flush=True)
    size_kb = (OUT / "render.mp4").stat().st_size / 1024
    print(f"::notice::rendered job {job_id} -> out/render.mp4 ({size_kb:.0f} KB)", flush=True)


if __name__ == "__main__":
    main()
