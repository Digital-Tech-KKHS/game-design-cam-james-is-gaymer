[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=7252999&assignment_repo_type=AssignmentRepo)
# Arcade-template

Template repo for final arcade projects Kerikeri High School DTC

## Installing dependencies

`pip install -r requirements.txt`

## Lint & style commands
```bash
black .
isort .
flake8
```

```bash 
python -m black --config pyproject.toml .
python -m isort .
python -m flake8 --config .flake8
```