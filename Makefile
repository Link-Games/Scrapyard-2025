# Makefile for Python project with converter/main.py

# Variables
PYTHON = python
SCRIPT = converter/main.py
INPUT_DIR = converter/input
OUTPUT_DIR = converter/output
REQUIREMENTS = converter/requirements.txt

# Default target
all: setup run

# Run the converter/main.py script
run: $(SCRIPT)
	@echo "Running converter/main.py..."
	$(PYTHON) $(SCRIPT)

# Create output directory if it doesn't exist (cross-platform)
setup:
	@echo "Setting up output directory..."
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "Error: $(PYTHON) not found. Please install Python or adjust PYTHON variable."; exit 1; }
	@$(PYTHON) -c "import os; os.makedirs('$(OUTPUT_DIR)', exist_ok=True)" || { echo "Error: Failed to create $(OUTPUT_DIR). Check permissions."; exit 1; }

# Install dependencies
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r $(REQUIREMENTS)

# Clean up output files
clean:
	@echo "Cleaning up output files..."
	-del /Q $(OUTPUT_DIR)\*.bmp 2>nul || rm -f $(OUTPUT_DIR)/*.bmp 2>/dev/null

# Optional: Create bytecode file (.pyc)
bytecode: $(SCRIPT)
	@echo "Creating bytecode for converter/main.py..."
	$(PYTHON) -m py_compile $(SCRIPT)

# Install dependencies and set up directories
setup-all: install setup

# Help message
help:
	@echo "Available commands:"
	@echo "  make all        - Set up directories and run converter/main.py"
	@echo "  make run        - Run converter/main.py"
	@echo "  make install    - Install required Python packages"
	@echo "  make setup      - Create output directory"
	@echo "  make clean      - Remove generated BMP files"
	@echo "  make bytecode   - Generate bytecode for converter/main.py"
	@echo "  make setup-all  - Install dependencies and create directories"
	@echo "  make help       - Show this help message"

.PHONY: all run install setup clean bytecode setup-all help