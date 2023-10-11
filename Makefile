# Makefile for a Python project

# Variables
PYTHON = python
PIP = pip
VENV = venv

# Main target
all: install

# Create a virtual environment
venv:
	$(PYTHON) -m $(VENV) venv

# Install project dependencies
install: venv
	.\venv\Scripts\$(PIP) install -r requirements.txt

# Run the Python program
run:
	.\venv\Scripts\$(PYTHON) .\src\main.py

# You can update any of the following targets to run the Python program with
# different flags
# The available flags are:
# 	-read_stored: Read the stored data from the database (Options: Y/N) (default: N)
# 	-start: Start the program from a specific year (Options: 2006-2023) (default: 2023)
# 	-clear_db: Clear the database before running the program (Options: Y/N) (default: N) 

# Run the Python program with the -read_stored flag
run_reading:
	.\venv\Scripts\$(PYTHON) .\src\main.py -read_stored Y

# Run the Python program with the -start flag
run_year_2020:
	.\venv\Scripts\$(PYTHON) .\src\main.py -start 2020 -clear_db Y

# Run the Python program with the -clear_db flag
run_cleaning:
	.\venv\Scripts\$(PYTHON) .\src\main.py -clear_db Y

# Run the Python program with the -read_stored flag amd -clear_db flag
run_cleaning_reading:
	.\venv\Scripts\$(PYTHON) .\src\main.py -clear_db Y -read_stored Y

# Clean up generated files and virtual environment
clean:
	rm -rf venv
	rm -rf src\__pycache__

# PHONY targets (targets that don't represent files)
.PHONY: all venv install run clean
