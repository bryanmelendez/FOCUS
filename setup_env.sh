#!/bin/bash

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate it
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "No requirements.txt found — skipping dependency install."
fi

echo "Environment setup complete. Run 'source .venv/bin/activate' to use it."