#!/bin/bash
set -e

# Project root assumed
VENV_DIR=venv

echo "=== Creating virtual environment ==="
python3 -m venv $VENV_DIR

echo "=== Activating virtual environment ==="
source $VENV_DIR/bin/activate

echo "=== Upgrading pip, setuptools, wheel ==="
pip install --upgrade pip setuptools wheel

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Checking ffmpeg installation ==="
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg could not be found. Please install it:"
    echo "  Mac: brew install ffmpeg"
    echo "  Ubuntu: sudo apt-get install ffmpeg"
fi

echo "=== Virtual environment setup complete ==="
echo "Activate it using: source $VENV_DIR/bin/activate"
