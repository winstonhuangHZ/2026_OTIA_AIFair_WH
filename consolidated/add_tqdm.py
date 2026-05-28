#!/usr/bin/env python3
"""
Add tqdm progress bars to training/evaluation loops in the notebook.

Adds tqdm to:
  1. Cell 2  (imports)  – from tqdm import tqdm, trange
  2. Cell 8  (affine calibrator epoch loop)
  3. Cell 18 (multi-baselines model enumeration loop)
  4. Cell 20 (weight sweep model + weight loops)
  5. Cell 22 (main execution experiment loops)
"""
import json, shutil, re
from pathlib import Path

NB = "consolidated_experiments.ipynb"

with open(NB, "r") as f:
    nb = json.load(f)

def get_src(cell_idx):
    src = nb["cells"][cell_idx]["source"]
    return "".join(src) if isinstance(src, list) else src

def set_src(cell_idx, text):
    nb["cells"][cell_idx]["source"] = text.splitlines(keepends=True)

# =====================================================================
# 1. Cell 2: add tqdm import
# =====================================================================
src = get_src(2)
old_import = "import os, re, sys, time, random, warnings"
new_import = "import os, re, sys, time, random, warnings\nfrom tqdm import tqdm, trange"
if old_import in src:
    src = src.replace(old_import, new_import, 1)
    set_src(2, src)
    print("Cell 2: added tqdm import")
else:
    print("WARN Cell 2: import line not found")

# =====================================================================
# 2. Cell 8 (index 8): affine calibrator epoch loop
#    Change: for ep in range(epochs):  ->  for ep in trange(epochs, desc=f'[calib] {mode}'):
#    Add tqdm to inner batch loop too
# =====================================================================
src = get_src(8)

# Replace outer epoch loop
old_epoch = "    for ep in range(epochs):"
new_epoch = "    for ep in trange(epochs, desc=f'[calib] {mode}', leave=False):"
if old_epoch in src:
    src = src.replace(old_epoch, new_epoch, 1)
    print("Cell 8: replaced epoch loop with trange")
else:
    print("WARN Cell 8: epoch loop line not found")

# Replace inner batch loop
old_batch = "        for start in range(0, n, batch_size):"
new_batch = "        for start in tqdm(range(0, n, batch_size), desc='  batch', leave=False):"
if old_batch in src:
    src = src.replace(old_batch, new_batch, 1)
    print("Cell 8: replaced batch loop with tqdm")
else:
    print("WARN Cell 8: batch loop line not found")

# Remove the manual print at end of each epoch (tqdm replaces this)
old_print = """        print(f'[calib] ep={ep+1}/{epochs} loss={lf:.6f} '
              f'rmse={rmse_f:.6f} cl={cl_f:.6f} a={a:.5f} b={b:.5f}', flush=True)"""
new_print = """        tqdm.write(f'[calib] ep={ep+1}/{epochs} loss={lf:.6f} '
                  f'rmse={rmse_f:.6f} cl={cl_f:.6f} a={a:.5f} b={b:.5f}')"""
if old_print in src:
    src = src.replace(old_print, new_print, 1)
    print("Cell 8: replaced print with tqdm.write")
else:
    print("WARN Cell 8: epoch print line not found")

set_src(8, src)

# =====================================================================
# 3. Cell 18 (index 18): multi-baselines model loop
#    Change: for i, bname in enumerate(model_names, 1):
#            print(f'\n--- [{i}/{len(model_names)}] {bname} ---')
#     ->
#            for bname in tqdm(model_names, desc='Models'):
#                print(f'\n--- {bname} ---')
# =====================================================================
src = get_src(18)

old_model_loop = """    for i, bname in enumerate(model_names, 1):
        print(f'\\n--- [{i}/{len(model_names)}] {bname} ---')"""
new_model_loop = """    for bname in tqdm(model_names, desc='Models'):
        tqdm.write(f'\\n--- {bname} ---')"""
if old_model_loop in src:
    src = src.replace(old_model_loop, new_model_loop, 1)
    print("Cell 18: replaced model loop with tqdm")
else:
    print("WARN Cell 18: model loop not found")

# Also fix the print inside fit_one_model_three_variants - replace with tqdm.write
old_fit_print = "    print(f'Fitting {baseline_name} on {target} | n_tr={len(y_tr)}')"
new_fit_print = "    tqdm.write(f'Fitting {baseline_name} on {target} | n_tr={len(y_tr)}')"
if old_fit_print in src:
    src = src.replace(old_fit_print, new_fit_print, 1)
    print("Cell 18: replaced fitting print with tqdm.write")
else:
    print("WARN Cell 18: fitting print not found")

old_done_print = "    print(f'Done {baseline_name} in {dt:.1f}s')"
new_done_print = "    tqdm.write(f'Done {baseline_name} in {dt:.1f}s')"
if old_done_print in src:
    src = src.replace(old_done_print, new_done_print, 1)
    print("Cell 18: replaced done print with tqdm.write")
else:
    print("WARN Cell 18: done print not found")

set_src(18, src)

# =====================================================================
# 4. Cell 20 (index 20): weight sweep loops
#    Change: for mi, mname in enumerate(model_names, 1):
#            for w in weights:
# =====================================================================
src = get_src(20)

old_model_loop2 = """    for mi, mname in enumerate(model_names, 1):
        if verbose:
            print(f'[{mi}/{len(model_names)}] {mname}: fitting...', end=' ', flush=True)"""
new_model_loop2 = """    for mi, mname in enumerate(tqdm(model_names, desc='Sweep Models')):
        if verbose:
            tqdm.write(f'[{mi+1}/{len(model_names)}] {mname}: fitting...', end=' ')"""
if old_model_loop2 in src:
    src = src.replace(old_model_loop2, new_model_loop2, 1)
    print("Cell 20: replaced model loop with tqdm")
else:
    print("WARN Cell 20: model loop not found")

old_cal_print = "            print('calibrating...', end=' ', flush=True)"
new_cal_print = "            tqdm.write('calibrating...', end=' ')"
if old_cal_print in src:
    src = src.replace(old_cal_print, new_cal_print, 1)
    print("Cell 20: replaced calibrating print with tqdm.write")
else:
    print("WARN Cell 20: calibrating print not found")

old_sweep_print = "            print(f'sweeping {len(weights)} weights', flush=True)"
new_sweep_print = "            tqdm.write(f'sweeping {len(weights)} weights')"
if old_sweep_print in src:
    src = src.replace(old_sweep_print, new_sweep_print, 1)
    print("Cell 20: replaced sweep print with tqdm.write")
else:
    print("WARN Cell 20: sweep print not found")

old_weight_loop = """        for w in weights:"""
# Find the exact indentation of the weight loop
# It's inside two for loops and the verbose block
# Let me check the actual code again
# It should be: 
#         for w in weights:
#             w = float(w)
new_weight_loop = """        for w in tqdm(weights, desc=f'  weights [{mname}]', leave=False):"""
if old_weight_loop in src:
    src = src.replace(old_weight_loop.replace("        ", ""), new_weight_loop.replace("        ", ""), 1)
    # Try again with proper indent
    pass

# Let me find the exact weight loop line
lines = src.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == "for w in weights:" and "tqdm" not in line:
        indent = line[:len(line) - len(line.lstrip())]
        new_line = indent + "for w in tqdm(weights, desc=f'  weights [{mname}]', leave=False):"
        lines[i] = new_line
        print(f"Cell 20: replaced weight loop with tqdm (line {i})")
        break
set_src(20, "\n".join(lines))

# =====================================================================
# 5. Cell 22 (index 22): main execution loops
#    Add outer-level tqdm for experiment phases
# =====================================================================
src = get_src(22)

# Experiment 1: Contrastive Learning
old_exp1 = """print('='*70)
print('EXPERIMENT: Contrastive Learning (XGB + RF)')
print('='*70)

for split in SPLITS:
    for target in TARGET_COLS:
        # XGB contrastive
        df_xgb = run_xgb_contrastive_experiment(split, target)
        all_results.append(df_xgb)
        
        # RF contrastive
        df_rf = run_rf_contrastive_experiment(split, target)
        all_results.append(df_rf)"""
new_exp1 = """print('='*70)
print('EXPERIMENT: Contrastive Learning (XGB + RF)')
print('='*70)

from itertools import product
exp1_pairs = list(product(SPLITS, TARGET_COLS))
for split, target in tqdm(exp1_pairs, desc='CL (XGB+RF)'):
    # XGB contrastive
    df_xgb = run_xgb_contrastive_experiment(split, target)
    all_results.append(df_xgb)
    
    # RF contrastive
    df_rf = run_rf_contrastive_experiment(split, target)
    all_results.append(df_rf)"""
if old_exp1 in src:
    src = src.replace(old_exp1, new_exp1, 1)
    print("Cell 22: added tqdm to Exp1 loop")
else:
    print("WARN Cell 22: Exp1 loop not found")
    # Print first 200 chars for debugging
    idx1 = src.find("EXPERIMENT: Contrastive")
    if idx1 >= 0:
        print(f"  Found at char {idx1}: '{src[idx1:idx1+100]}'")

# Experiment 2: MoE
old_exp2 = """for split in SPLITS:
    for target in TARGET_COLS:
        df_moe, moe_out = run_moe_experiment(split, target)
        all_results.append(df_moe)
        all_artifacts[f'MoE_{split}_{target}'] = moe_out"""
new_exp2 = """exp2_pairs = list(product(SPLITS, TARGET_COLS))
for split, target in tqdm(exp2_pairs, desc='MoE'):
    df_moe, moe_out = run_moe_experiment(split, target)
    all_results.append(df_moe)
    all_artifacts[f'MoE_{split}_{target}'] = moe_out"""
if old_exp2 in src:
    src = src.replace(old_exp2, new_exp2, 1)
    print("Cell 22: added tqdm to Exp2 loop")
else:
    print("WARN Cell 22: Exp2 loop not found")

# Experiment 3: Multi-Baselines - this one has a different structure (prints are inside)
# Let me look for the specific pattern
old_exp3_loops = """for split in SPLITS:
    if split == 'Random(70/15/15)':
        tr, va, te = make_random_split(df)
    else:
        tr, va, te = make_group_split_by_grid(df)
    
    for target in TARGET_COLS:"""
new_exp3_loops = """exp3_pairs = list(product(SPLITS, TARGET_COLS))
for split, target in tqdm(exp3_pairs, desc='Multi-Baselines'):
    if split == 'Random(70/15/15)':
        tr, va, te = make_random_split(df)
    else:
        tr, va, te = make_group_split_by_grid(df)"""
if old_exp3_loops in src:
    src = src.replace(old_exp3_loops, new_exp3_loops, 1)
    print("Cell 22: added tqdm to Exp3 loops")
else:
    print("WARN Cell 22: Exp3 loops not found")

# Also fix print statements inside cell 22 to use tqdm.write
src = src.replace("print(f'\\n--- Multi-Baselines [{split}, {target}] ---')",
                  "tqdm.write(f'--- Multi-Baselines [{split}, {target}] ---')")
src = src.replace("print_splits(df, tr, va, te, target)",
                  "tqdm.write(f'  n_tr={len(tr)}, n_va={len(va)}, n_te={len(te)}')")

# Also fix the print(f'\\nTotal result rows:...')
src = src.replace("print(f'\\nTotal result rows: {len(results_df)}')",
                  "tqdm.write(f'Total result rows: {len(results_df)}')")

set_src(22, src)

# =====================================================================
# Save
# =====================================================================
bak = Path(NB).with_suffix(".ipynb.bak2")
shutil.copy2(NB, bak)
print(f"\nBackup: {bak}")

with open(NB, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Saved: {NB}")
print("Done! Added tqdm progress bars.")
