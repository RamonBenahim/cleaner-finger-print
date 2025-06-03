#!/bin/bash

# Setup GitHub Repository
echo "Setting up GitHub repository..."

# Initialize git if not already done
if [ ! -d ".git" ]; then
    git init
    echo "Git repository initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.backup
cleaned_*
custom_config.json

# Compiled extensions
*.o
*.so
fast_cleaner.c.o
EOF
    echo ".gitignore created"
fi

# Add all files
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit"
else
    # Commit
    git commit -m "Initial commit: Advanced Media Fingerprint Remover Bot

Features:
- Remove EXIF data from images
- Clean video metadata
- Steganography detection and removal
- Pixel randomization
- Timestamp randomization
- Batch processing GUI
- C extensions for performance
- Advanced entropy analysis
- Decoy metadata injection

Supports: JPG, PNG, TIFF, BMP, MP4, AVI, MOV, MKV, WMV"
    echo "Files committed successfully!"
fi

echo ""
echo "Repository ready for GitHub!"
echo ""
echo "Files included:"
echo "- Core bot (media_cleaner_bot.py)"
echo "- Advanced cleaner (advanced_cleaner.py)"
echo "- GUI batch processor (batch_processor.py)"
echo "- C extensions (fast_cleaner.c)"
echo "- Hybrid cleaner (hybrid_cleaner.py)"
echo "- Test suite (test_bot.py)"
echo "- Usage examples (example_usage.py)"
echo "- Installation script (install.sh)"
echo "- Documentation (README.md)"
echo ""
echo "Next steps:"
echo "1. Create a new repository on GitHub"
echo "2. Run: git remote add origin https://github.com/USERNAME/REPO_NAME.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo ""
echo "Suggested repository name: media-fingerprint-remover"