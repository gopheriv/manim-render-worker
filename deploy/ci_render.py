"""CI script for rendering Manim scenes.

Reads CODE_GZ (gzip+base64 encoded Python code) from environment,
decodes it, renders using Manim, and outputs the video.
"""
import base64
import gzip
import os
import shutil
import subprocess
import sys
from pathlib import Path

def main():
    code_gz = os.environ.get("CODE_GZ", "")
    quality = os.environ.get("QUALITY", "-qh")
    fps = os.environ.get("FPS", "60")
    job_id = os.environ.get("JOB_ID", "render")

    if not code_gz:
        print("ERROR: CODE_GZ environment variable not set")
        sys.exit(1)

    # Decode the code
    try:
        code_bytes = base64.b64decode(code_gz)
        code = gzip.decompress(code_bytes).decode('utf-8')
    except Exception as e:
        print(f"ERROR: Failed to decode CODE_GZ: {e}")
        sys.exit(1)

    # Write to scene.py
    scene_path = Path("scene.py")
    scene_path.write_text(code, encoding='utf-8')

    # Create output directory
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)

    # Render with Manim
    cmd = [
        "manim",
        "scene.py",
        "GenScene",
        quality,
        "--fps", fps,
        "--media_dir", "./media",
        "-o", "render.mp4"
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Manim failed with code {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        sys.exit(1)

    # Find the rendered video
    video_files = list(Path("media/videos").rglob("render.mp4"))
    if not video_files:
        print("ERROR: No render.mp4 found in media/videos")
        sys.exit(1)

    # Copy to out directory
    shutil.copy(video_files[0], out_dir / "render.mp4")
    print(f"SUCCESS: Rendered to out/render.mp4")

if __name__ == "__main__":
    main()
