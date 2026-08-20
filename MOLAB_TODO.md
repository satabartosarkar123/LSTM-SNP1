# Molab (Marimo) Setup Guide

Since Molab currently requires manual uploads (no cloning) and runs on Marimo, I have created a specific orchestrator for this workflow: `Master_Runner_Molab.ipynb`.

## Step-by-Step Instructions

1. **Upload the Folder**:
   - On your local PC, download or clone this repository.
   - Go into your Molab (Marimo) instance and **upload the `Paper 1` folder** so that its path in Molab is exactly `/marimo/Paper 1`.

2. **Upload the Orchestrator**:
   - Upload the `Master_Runner_Molab.ipynb` file to your Molab workspace.

3. **Run the Orchestrator**:
   - Open `Master_Runner_Molab.ipynb` in Molab.
   - Run all the cells.
   - **Cell 1**: Installs `papermill`, `tabulate`, and registers the `python3` kernel (exactly as you showed in your screenshot).
   - **Cell 2 & 3**: Scans `/marimo/Paper 1` for all 100+ notebooks and executes them sequentially to prevent Out-Of-Memory (OOM) errors.
   - **Cell 4**: Once all notebooks are finished (or if you stop it midway), it automatically zips the entire `/marimo/Paper 1` folder into `/marimo/Paper_1_Results.zip`.

4. **Download Your Results**:
   - After execution finishes, simply download `/marimo/Paper_1_Results.zip` from the Molab UI back to your local PC.

## What's Changed in the Notebooks?

Before zipping, I already ran a patching script across all ~104 notebooks in `Paper 1`. They have been modified to:
1. Show **exact, epoch-by-epoch progress** (`verbose=1`).
2. Run through all 4 noise levels (`0.0, 0.005, 0.05, 0.10`) for notebooks that evaluate noise.
3. Automatically format and print a clean metrics table (RMSE, MSE, NMSE) using `tabulate` at the end of the test cells.

*(You don't need HuggingFace or Ollama for this project. The time-series models train natively from scratch using standard PyTorch/TensorFlow.)*
