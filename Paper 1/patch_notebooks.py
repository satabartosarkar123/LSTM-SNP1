import os
import glob
import json
import re

def patch_notebooks():
    paper_dir = r"c:\Users\USER\Cost-Aware-Test-Time\LSTM-SNP1\Paper 1"
    notebooks = glob.glob(os.path.join(paper_dir, "**/*.ipynb"), recursive=True)
    
    for nb_path in notebooks:
        if "Master_Runner" in nb_path or ".ipynb_checkpoints" in nb_path:
            continue
            
        with open(nb_path, "r", encoding="utf-8") as f:
            try:
                nb = json.load(f)
            except Exception as e:
                print(f"Error loading {nb_path}: {e}")
                continue
                
        modified = False
        has_noise_loop = False
        noise_cell_idx = -1
        
        # We will track if we need to insert the table code at the end of the cell
        for idx, cell in enumerate(nb.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
                
            source = cell.get("source", [])
            new_source = []
            in_noise_loop = False
            
            for i, line in enumerate(source):
                original_line = line
                
                # Progress tracking updates
                if "verbose=0" in line:
                    line = line.replace("verbose=0", "verbose=1")
                if "verbose=False" in line:
                    line = line.replace("verbose=False", "verbose=True")
                    
                # Noise levels update
                if re.search(r"noise_levels\s*=\s*\[.*?\]", line) or re.search(r"NOISE_LEVELS\s*=\s*\[.*?\]", line):
                    # Replace with all 4 noise levels
                    line = re.sub(r"noise_levels\s*=\s*\[.*?\]", "noise_levels = [0.0, 0.005, 0.05, 0.10]", line)
                    line = re.sub(r"NOISE_LEVELS\s*=\s*\[.*?\]", "noise_levels = [0.0, 0.005, 0.05, 0.10]", line) 
                    
                    # Also inject our tracking dict
                    line += "    _molab_results = []\n"
                    has_noise_loop = True
                    noise_cell_idx = idx
                
                # Check if it's the end of a run (where it prints Best Run Metrics)
                if has_noise_loop and "print(f'NMSE:" in line and "best_idx" in line:
                    # Inject capture logic
                    new_source.append(line)
                    indent = line[:len(line) - len(line.lstrip())]
                    new_source.append(f"{indent}_molab_results.append([lam, all_rmse[best_idx], all_mse[best_idx], all_nmse[best_idx]])\n")
                    continue
                    
                new_source.append(line)
                
            if source != new_source:
                cell["source"] = new_source
                modified = True
                
            # If this cell had the noise loop, let's append the table printing code at its very end
            if has_noise_loop and idx == noise_cell_idx:
                table_code = [
                    "\n# ============================================================\n",
                    "# FINAL RESULTS TABLE ACROSS ALL NOISE LEVELS\n",
                    "# ============================================================\n",
                    "import pandas as pd\n",
                    "from tabulate import tabulate\n",
                    "if len(_molab_results) > 0:\n",
                    "    df_res = pd.DataFrame(_molab_results, columns=['Noise Level (lambda)', 'RMSE', 'MSE', 'NMSE'])\n",
                    "    print('\\n' + '='*80)\n",
                    "    print('FINAL RESULTS TABLE ACROSS ALL 4 NOISE LEVELS')\n",
                    "    print('='*80)\n",
                    "    print(tabulate(df_res, headers='keys', tablefmt='github', showindex=False))\n"
                ]
                cell["source"].extend(table_code)
                has_noise_loop = False # reset so we don't inject multiple times
                modified = True
                
        if modified:
            with open(nb_path, "w", encoding="utf-8") as f:
                json.dump(nb, f, indent=1)
                
    print("Notebook patching complete.")

if __name__ == "__main__":
    patch_notebooks()
