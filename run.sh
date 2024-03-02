#!/bin/bash

# Define variables
REPO_URL="https://github.com/strangedreamer4/TERCHAT.git"
SCRIPT_NAME="terchat.py"
VENV_DIR="terchat_venv"

# Create or activate virtual environment
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

# Update or clone the repository
if [ -d "$SCRIPT_NAME" ]; then
    cd "$SCRIPT_NAME" || exit
    git pull origin main  # assuming 'main' is your main branch
    cd ..
else
    git clone "$REPO_URL"
fi

# Install dependencies
pip3 install -r "$SCRIPT_NAME/requirements.txt"

# Run the terchat.py script
python3 "$SCRIPT_NAME"
