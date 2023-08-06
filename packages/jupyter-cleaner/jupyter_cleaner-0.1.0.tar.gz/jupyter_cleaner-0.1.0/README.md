# jupyter-cleaner

jupyter-cleaner makes tracking Jupyter lab files in git easy.

This is done by:
- Removing output of all cells
- Formatting all cells (using black)
- Reordering imports in all cells (using reorder-python-imports)
- Setting the execution count of all cells

It is recommended to run jupyter-cleaner using pre-commit:
```
default_language_version:
  python: python3.11
repos:
- repo: local
  hooks:
      - id: jupyter_cleaner
        name: jupyter_cleaner
        entry: jupyter_cleaner .
        language: system
        pass_filenames: false
        always_run: true
```

## CLI
running `jupyter_cleaner -h` displays:
```
jupyter_cleaner

positional arguments:
  files_or_dir          Jupyter lab files to format or directories to search for lab files

options:
  -h, --help            show this help message and exit
  --execution_count EXECUTION_COUNT
                        Number to set for the execution count of every cell
  --remove_code_output  Number to set for the execution count of every cell
  --format              Format code of every cell (uses black)
  --reorder_imports     Reorder imports of every cell (uses reorder-python-imports)
```

## pyproject.toml
Inputs to jupyter-cleaner can be supplied via pyproject.toml:
```
[tool.jupyter_cleaner]
execution_count=0
remove_code_output=true
format=true
reorder_imports=true
```
