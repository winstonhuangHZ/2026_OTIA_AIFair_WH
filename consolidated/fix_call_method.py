#!/usr/bin/env python3
"""Fix the __call__ method signature in XGBContrastiveLossObjective (cell 12)."""
import json, shutil
from pathlib import Path

nb_path = "consolidated_experiments.ipynb"

with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell 12 is the code cell with XGBContrastiveLossObjective
cell = nb["cells"][12]
src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]

old = (
    '    def __call__(self, preds, dtrain):\n'
    '        y_true = dtrain.get_label().astype(np.float64)\n'
    '        y_pred = preds.astype(np.float64)'
)

new = (
    '    def __call__(self, labels, preds):\n'
    '        y_true = labels.astype(np.float64)\n'
    '        y_pred = preds.astype(np.float64)'
)

if old in src:
    src = src.replace(old, new, 1)
    # Save backup
    bak = Path(nb_path).with_suffix(".ipynb.bak")
    shutil.copy2(nb_path, bak)
    print(f"Backup: {bak}")
    
    cell["source"] = src.splitlines(keepends=True)
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"Fixed cell 12: __call__(self, labels, preds)")
else:
    print("ERROR: old text not found in cell 12!")
    print("First 200 chars of cell:")
    print(src[:200])
