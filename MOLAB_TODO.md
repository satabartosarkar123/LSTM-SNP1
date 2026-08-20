# Molab Orchestration Guide

You requested a Molab-ready setup for `LSTM-SNP1`, similar to your Cost-Aware Test-Time project.

I have created an automated pipeline that will sequentially execute every comparative notebook and push the output back to GitHub. This avoids Out-Of-Memory (OOM) issues from running 100+ notebooks at once, and ensures that if your Molab instance gets interrupted, your progress up to the last successful notebook is saved.

## Step-by-Step Instructions

1. **Clone your repository** into your Molab instance:
   ```bash
   git clone https://github.com/satabartosarkar123/LSTM-SNP1.git
   cd "LSTM-SNP1/Paper 1"
   ```
2. **Open `molab_run.ipynb`** in the Jupyter environment.
3. **Run All Cells** in `molab_run.ipynb`.
   - The first cell installs `papermill` and `tabulate`.
   - The script will automatically locate all 104 model notebooks.
   - It executes each notebook using Papermill (which automatically handles GPU memory and output cell injection).
   - After a notebook finishes successfully, it performs:
     ```bash
     git add <notebook.ipynb>
     git commit -m "Auto-update <notebook.ipynb> results"
     git push
     ```

## Progress & Output Tracking

All notebooks have been patched to:
1. Show **exact, epoch-by-epoch progress** (`verbose=1` instead of `verbose=0`).
2. Collect metrics for **all 4 noise levels** (`0.0`, `0.005`, `0.05`, `0.10`).
3. Print a **clean markdown table** showing `RMSE`, `MSE`, and `NMSE` for each noise level at the very end of the training cell.

> **Note on HuggingFace:** You do not need to download massive HuggingFace LLM checkpoints (like Qwen or Llama) for this repository. The `LSTM-SNP1` models train natively from scratch using standard PyTorch/TensorFlow.
