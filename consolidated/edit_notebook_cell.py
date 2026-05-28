#!/usr/bin/env python3
"""
Reusable utility to edit cells in a Jupyter notebook (.ipynb) file.

Usage
-----
  python edit_notebook_cell.py <notebook> <cell_index> <new_source_file>

  python edit_notebook_cell.py <notebook> --find <pattern> <new_source_file>

  python edit_notebook_cell.py <notebook> --interactive

Examples
--------
  # Replace cell at index 12 with contents from fix.txt
  python edit_notebook_cell.py experiments.ipynb 12 fix.txt

  # Replace first cell whose source contains "run_xgb_contrastive_experiment"
  python edit_notebook_cell.py experiments.ipynb --find "run_xgb_contrastive_experiment" new_code.py

  # Show cell indices with preview
  python edit_notebook_cell.py experiments.ipynb --list
"""

import json, sys, re, shutil
from pathlib import Path


def load_notebook(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notebook(nb: dict, path: str, backup: bool = True) -> None:
    p = Path(path)
    if backup:
        bak = p.with_suffix(".ipynb.bak")
        shutil.copy2(p, bak)
        print(f"  Backup saved to {bak}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print(f"  Notebook saved to {path}")


def get_cell_source(nb: dict, idx: int) -> str:
    """Return the source text of cell at index idx."""
    src = nb["cells"][idx]["source"]
    if isinstance(src, list):
        return "".join(src)
    return src


def set_cell_source(nb: dict, idx: int, new_source: str) -> None:
    """Replace the source of cell at index idx."""
    nb["cells"][idx]["source"] = new_source.splitlines(keepends=True)
    # Jupyter stores source as list of lines; make sure last line ends with newline
    src_list = nb["cells"][idx]["source"]
    if src_list and not src_list[-1].endswith("\n"):
        src_list[-1] += "\n"


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_cells(nb: dict) -> None:
    """Print cell indices with type and first line preview."""
    cells = nb["cells"]
    print(f"{'Index':>6}  {'Type':>8}  {'Exec?':>5}  Preview")
    print("-" * 80)
    for i, c in enumerate(cells):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        first = src.strip().split("\n")[0] if src.strip() else "(empty)"
        exec_count = c.get("execution_count", " ")
        print(f"{i:>6}  {c['cell_type']:>8}  {str(exec_count):>5}  {first[:60]}")


def find_cell_by_content(nb: dict, pattern: str, regex: bool = False) -> list:
    """Return indices of cells whose source contains pattern."""
    matches = []
    for i, c in enumerate(nb["cells"]):
        src = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if regex:
            if re.search(pattern, src):
                matches.append(i)
        else:
            if pattern in src:
                matches.append(i)
    return matches


def replace_in_source(nb: dict, idx: int, old: str, new: str, count: int = 1) -> bool:
    """
    Find and replace text within a cell's source.
    Returns True if replacement was made.
    """
    src = get_cell_source(nb, idx)
    if old not in src:
        return False
    new_src = src.replace(old, new, count)
    set_cell_source(nb, idx, new_src)
    return True


def main():
    args = sys.argv[1:]
    if not args or "-h" in args or "--help" in args:
        print(__doc__)
        sys.exit(0)

    nb_path = args[0]

    if not Path(nb_path).exists():
        print(f"ERROR: notebook not found: {nb_path}")
        sys.exit(1)

    nb = load_notebook(nb_path)

    # --list : show cells
    if "--list" in args:
        list_cells(nb)
        return

    # --find <pattern> <new_source_file>
    if "--find" in args:
        try:
            p_idx = args.index("--find")
            pattern = args[p_idx + 1]
            new_source_file = args[p_idx + 2]
        except IndexError:
            print("ERROR: --find requires <pattern> and <new_source_file>")
            sys.exit(1)
        matches = find_cell_by_content(nb, pattern)
        if not matches:
            print(f"No cells contain pattern: {pattern}")
            sys.exit(1)
        if len(matches) > 1:
            print(f"Multiple cells match. Using first match (index {matches[0]}).")
            print(f"  Matches at indices: {matches}")
        idx = matches[0]
        new_src = read_file(new_source_file)
        set_cell_source(nb, idx, new_src)
        save_notebook(nb, nb_path)
        print(f"  Replaced cell {idx} with contents from {new_source_file}")
        return

    # --interactive : edit cells interactively
    if "--interactive" in args:
        list_cells(nb)
        idx = int(input("\nEnter cell index to edit: "))
        print(f"\nCurrent content of cell {idx}:")
        print("-" * 60)
        print(get_cell_source(nb, idx))
        print("-" * 60)
        new_src = input("\nPaste new cell content (end with '---' on its own line):\n")
        lines = []
        while True:
            line = input()
            if line.strip() == "---":
                break
            lines.append(line)
        new_src = "\n".join(lines) + "\n"
        set_cell_source(nb, idx, new_src)
        save_notebook(nb, nb_path)
        return

    # <cell_index> <new_source_file>
    try:
        idx = int(args[1])
        new_source_file = args[2]
    except (IndexError, ValueError):
        print("ERROR: usage: edit_notebook_cell.py <notebook> <cell_index> <new_source_file>")
        print("  Or:  edit_notebook_cell.py <notebook> --find <pattern> <new_source_file>")
        sys.exit(1)

    new_src = read_file(new_source_file)
    set_cell_source(nb, idx, new_src)
    save_notebook(nb, nb_path)
    print(f"  Replaced cell {idx} with contents from {new_source_file}")


if __name__ == "__main__":
    main()
