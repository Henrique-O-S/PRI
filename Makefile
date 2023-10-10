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
run_companies:
	.\venv\Scripts\$(PYTHON) run_companies.py

run_articles:
	.\venv\Scripts\$(PYTHON) run_articles.py

# Clean up generated files and virtual environment
clean:
	rm -rf venv
	rm -rf __pycache__

# PHONY targets (targets that don't represent files)
.PHONY: all venv install run clean
