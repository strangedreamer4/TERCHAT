#!/bin/bash

# Check if Python is installed
if ! [ -x "$(command -v python3)" ]; then
  echo "Python not found. Please install Python and run the script again."
  
fi

# System update and Python installation
echo "Updating system and installing Python..."
apt update -y
apt upgrade -y
pkg install python -y
pkg install python2 -y
pkg install python3 -y
clear

# Install Git (if not installed)
if ! [ -x "$(command -v git)" ]; then
  echo "Installing Git..."
  pkg install git -y
fi
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
