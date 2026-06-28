# manim-render-worker

Cloud render worker for Manim animations using GitHub Actions.

## Usage

This repository is used by the manim-bot to render high-quality animations on GitHub's 16GB/4vCPU runners.

### Workflow Dispatch

The `render` workflow accepts:
- `code_gz`: gzip+base64 encoded Manim scene code
- `quality`: Manim quality flag (-ql/-qm/-qh/-qk)
- `fps`: Frames per second
- `job_id`: Unique job identifier

### Output

Rendered video is uploaded as an artifact named `render-{job_id}`.
