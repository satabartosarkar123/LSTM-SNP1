import os
import glob
import json
import traceback

paper1_dir = "/Users/satabarto/Research/Paper 1"
all_notebooks = glob.glob(os.path.join(paper1_dir, "**/*.ipynb"), recursive=True)
print(f"Verifying syntax for {len(all_notebooks)} notebooks...")

errors = 0
for nb_path in all_notebooks:
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
        
        code_cells = [c for c in nb.get('cells', []) if c.get('cell_type') == "code"]
        combined_code = ""
        for cell in code_cells:
            combined_code += "".join(cell.get('source', [])) + "\n"
        
        compile(combined_code, nb_path, 'exec')
    except Exception as e:
        print(f"❌ Syntax/Compilation error in: {nb_path}")
        traceback.print_exc()
        errors += 1

if errors == 0:
    print("✅ All notebooks are syntax valid and compiled successfully!")
else:
    print(f"❌ Found {errors} syntax/compilation errors in total.")
