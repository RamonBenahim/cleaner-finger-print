#!/bin/bash

echo "Pushing to GitHub repository..."

# Add all files
echo "Adding files..."
git add .

# Commit changes
echo "Committing changes..."
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

# Set main branch
echo "Setting main branch..."
git branch -M main

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "Repository: https://github.com/RamonBenahim/cleaner-finger-print"
echo ""
echo "Your project is now live on GitHub! 🚀"