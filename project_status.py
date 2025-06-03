#!/usr/bin/env python3

import os
import sys

def check_project_status():
    """Check the current status of the project files."""
    
    print("🔍 Advanced Media Fingerprint Remover - Project Status")
    print("=" * 60)
    
    required_files = {
        'media_cleaner_bot.py': 'Core bot functionality',
        'advanced_cleaner.py': 'Advanced features with steganography detection',
        'batch_processor.py': 'GUI for batch processing',
        'hybrid_cleaner.py': 'C extension integration',
        'fast_cleaner.c': 'C performance extensions',
        'example_usage.py': 'Usage examples and demonstrations',
        'test_bot.py': 'Comprehensive test suite',
        'config.json': 'Configuration file',
        'requirements.txt': 'Python dependencies',
        'README.md': 'Project documentation',
        'install.sh': 'Installation script',
        'setup.py': 'C extension build script',
        'LICENSE': 'MIT license',
        '.gitignore': 'Git ignore rules'
    }
    
    print("\n📁 File Status:")
    missing_files = []
    
    for filename, description in required_files.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:<25} ({size:,} bytes) - {description}")
        else:
            print(f"❌ {filename:<25} MISSING - {description}")
            missing_files.append(filename)
    
    print(f"\n📊 Summary:")
    print(f"Total files: {len(required_files)}")
    print(f"Present: {len(required_files) - len(missing_files)}")
    print(f"Missing: {len(missing_files)}")
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    print("\n🎯 Project Features:")
    features = [
        "✅ EXIF data removal from images",
        "✅ Video metadata cleaning",
        "✅ Timestamp randomization",
        "✅ Pixel randomization and scrambling",
        "✅ Steganography detection and removal",
        "✅ Entropy analysis for hidden data",
        "✅ Batch processing with GUI",
        "✅ C extensions for performance",
        "✅ Comprehensive test suite",
        "✅ Command-line interface",
        "✅ Python API",
        "✅ Configuration system"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n🚀 Ready for GitHub!")
    print("Repository: https://github.com/RamonBenahim/cleaner-finger-print")
    
    return True

def check_dependencies():
    """Check if required dependencies are available."""
    
    print("\n🔧 Dependency Check:")
    
    dependencies = [
        ('PIL', 'Pillow', 'Image processing'),
        ('cv2', 'opencv-python', 'Video processing'),
        ('numpy', 'numpy', 'Numerical operations'),
        ('mutagen', 'mutagen', 'Audio metadata'),
        ('tkinter', 'tkinter', 'GUI framework')
    ]
    
    available = []
    missing = []
    
    for module, package, description in dependencies:
        try:
            __import__(module)
            print(f"✅ {package:<20} - {description}")
            available.append(package)
        except ImportError:
            print(f"❌ {package:<20} - {description} (MISSING)")
            missing.append(package)
    
    print(f"\nDependencies: {len(available)}/{len(dependencies)} available")
    
    if missing:
        print(f"Install missing: pip install {' '.join(missing)}")
    
    return len(missing) == 0

def show_usage_examples():
    """Show quick usage examples."""
    
    print("\n💡 Quick Usage Examples:")
    print("-" * 30)
    
    examples = [
        ("Basic cleaning", "python media_cleaner_bot.py image.jpg"),
        ("Directory batch", "python media_cleaner_bot.py /path/to/images/"),
        ("Advanced analysis", "python advanced_cleaner.py --analyze-only image.jpg"),
        ("Advanced cleaning", "python advanced_cleaner.py image.jpg"),
        ("GUI interface", "python batch_processor.py"),
        ("Run examples", "python example_usage.py"),
        ("Run tests", "python test_bot.py")
    ]
    
    for description, command in examples:
        print(f"  {description:<20}: {command}")

def main():
    """Main function to run all checks."""
    
    project_ok = check_project_status()
    deps_ok = check_dependencies()
    
    show_usage_examples()
    
    print("\n" + "=" * 60)
    
    if project_ok and deps_ok:
        print("🎉 PROJECT READY! All files present and dependencies available.")
        print("📤 Ready to push to GitHub!")
    elif project_ok:
        print("⚠️  Project files ready, but some dependencies missing.")
        print("📦 Run: pip install -r requirements.txt")
    else:
        print("❌ Project incomplete. Some files are missing.")
    
    print("\n🔗 Next steps:")
    print("1. git add .")
    print("2. git commit -m 'Advanced Media Fingerprint Remover'")
    print("3. git push -u origin main")

if __name__ == "__main__":
    main()