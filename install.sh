#!/bin/bash

echo "Installing Advanced Media Fingerprint Remover..."

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Compiling C extensions (optional)..."
if command -v gcc &> /dev/null; then
    python3 setup.py build_ext --inplace
    echo "C extensions compiled successfully."
else
    echo "Warning: GCC not found. C extensions will not be available."
fi

echo "Setting up permissions..."
chmod +x *.py
chmod +x *.sh

echo "Running tests..."
python3 test_bot.py

echo ""
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  Basic: python3 media_cleaner_bot.py image.jpg"
echo "  Advanced: python3 advanced_cleaner.py image.jpg"
echo "  GUI: python3 batch_processor.py"
echo "  Examples: python3 example_usage.py"