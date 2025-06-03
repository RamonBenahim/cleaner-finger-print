#!/bin/bash

echo "Compiling C extensions for high performance..."

# Check if Python development headers are available
if ! python3-config --includes > /dev/null 2>&1; then
    echo "ERROR: Python development headers not found"
    echo "Install with: sudo apt-get install python3-dev (Ubuntu/Debian)"
    echo "Or: brew install python3 (macOS)"
    exit 1
fi

# Compile C extension
echo "Building C extension..."
python3 setup.py build_ext --inplace

if [ $? -eq 0 ]; then
    echo "SUCCESS: C extensions compiled successfully"
    echo "High performance mode available"
    
    # Test the extension
    echo "Testing C extension..."
    python3 -c "
import fast_cleaner
print('SUCCESS: C extension import successful')
print('Testing entropy calculation...')
result = fast_cleaner.calculate_entropy(b'test data')
print(f'Entropy: {result:.4f}')
"
else
    echo "ERROR: Compilation failed"
    echo "The bot will work in Python-only mode"
fi

echo ""
echo "Usage:"
echo "  python3 hybrid_cleaner.py file.jpg"
echo "  python3 hybrid_cleaner.py --benchmark"