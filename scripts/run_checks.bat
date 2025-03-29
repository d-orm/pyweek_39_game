@echo off
echo Setting PYTHONPATH...
set PYTHONPATH=%CD%

echo Running Ruff Formatting...
ruff format .

echo Running Ruff Import Sorting...
ruff check --fix --select I .

echo Running Mypy Type Checking...
mypy .

echo All checks completed!
