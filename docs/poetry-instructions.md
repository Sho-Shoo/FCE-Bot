# Guides on using Poetry for dependency management 

## Environment setup 

If there is already a `pyproject.toml` file in project root, you can simply create a virtual python environment using 
`poetry env use python`. You can then enter the virtual environment using `poetry shell`. 

## Managing dependencies 

- `poetry add <denependency_name>` to add a dependency 
- `poetry remove <denependency_name>` to remove a dependency

The two commands above will change both `pyproject.toml` and `poetry.lock` files, and install the package in your venv. 
If you ever need to update `pyproject.toml` yourself, use `poetry lock` to update lock file. 

- `poetry show` to list all dependencies; or `poetry show --tree` to show dependencies relationships in tree structure 

## Managing deployment 

Since we want to use Docker for deployment, it is easier to just do `pip install -r requirements.txt`, so we can use 
`poetry export -f requirements.txt -o requirements.txt --without-hashes` to export a `requirements.txt` file from the 
lock file. 