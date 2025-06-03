#!/bin/bash

# Script de instalação do Bot Removedor de Fingerprints
echo "Installing Media Fingerprint Remover"
echo "===================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi

echo "SUCCESS: Python found: $(python3 --version)")")"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 not found. Installing pip..."
    python3 -m ensurepip --upgrade
fi

echo "SUCCESS: pip found: $(pip3 --version)")")"

# Create virtual environment (optional)
read -p "Create virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    echo "Creating virtual environment...""
    python3 -m venv media_cleaner_env
    source media_cleaner_env/bin/activate
    echo "SUCCESS: Virtual environment created and activated" and activated"
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "SUCCESS: Dependencies installed successfully"sfully"
else
    echo "ERROR: Error installing dependencies"cies"
    exit 1
fi

# Make scripts executable
chmod +x media_cleaner_bot.py
chmod +x advanced_cleaner.py
chmod +x batch_processor.py

echo "SUCCESS: Scripts made executable"e"

# Test installation
echo "Testing installation..."
python3 -c "
try:
    from PIL import Image
    import cv2
    import numpy as np
    from mutagen import File
    print('SUCCESS: All dependencies imported successfully')
except ImportError as e:
    print(f'ERROR: Import error: {e}')
    exit(1)
"

echo ""
echo "SUCCESS: Installation completed!"
echo ""
echo "How to use:"
echo "  Command line: python3 media_cleaner_bot.py file.jpg"
echo "  GUI: python3 batch_processor.py"
echo "  Advanced: python3 advanced_cleaner.py"
echo ""
echo "See README.md for more information"

# Create aliases (optional)
read -p "Create aliases for easier use? (y/n): " create_aliases
if [[ $create_aliases == "y" || $create_aliases == "Y" ]]; then
    echo "alias media-clean='python3 $(pwd)/media_cleaner_bot.py'" >> ~/.bashrc
    echo "alias media-gui='python3 $(pwd)/batch_processor.py'" >> ~/.bashrc
    echo "alias media-advanced='python3 $(pwd)/advanced_cleaner.py'" >> ~/.bashrc
    echo "SUCCESS: Aliases created. Run 'source ~/.bashrc' to activate them"
fi

echo ""
echo "WARNING: Use only on files you own!"
echo "IMPORTANT: Always backup before processing important files"