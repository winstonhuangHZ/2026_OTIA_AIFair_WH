"""
Merge the notebook parts into a single consolidated_experiments.ipynb.

Run: python merge_notebooks.py
"""

import json
import glob
import os

def merge_ipynb_parts(output_file='final_consolidated.ipynb'):
    # Find all parts: p1, p2, p3, p4, p5 (explicit order)
    parts = []
    for i in range(1, 6):
        p = f'consolidated_experiments_p{i}.ipynb'
        if os.path.exists(p):
            parts.append(p)
    
    if not parts:
        parts = sorted(glob.glob('consolidated_experiments*.ipynb'))
        parts = [p for p in parts if p != output_file]
    
    if not parts:
        print('No parts found. Run from the consolidated/ directory.')
        return
    
    print(f'Merging: {parts}')
    
    # Read all cells from all parts
    all_cells = []
    metadata = None
    
    for part_file in parts:
        with open(part_file, 'r') as f:
            part = json.load(f)
        
        if metadata is None:
            metadata = part.get('metadata', {})
        
        all_cells.extend(part.get('cells', []))
    
    # Write merged notebook
    merged = {
        'cells': all_cells,
        'metadata': metadata or {},
        'nbformat': 4,
        'nbformat_minor': 4,
    }
    
    with open(output_file, 'w') as f:
        json.dump(merged, f, indent=1, ensure_ascii=False)
    
    print(f'Merged notebook saved: {output_file}')
    print(f'Total cells: {len(all_cells)}')

if __name__ == '__main__':
    merge_ipynb_parts()
