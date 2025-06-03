#!/usr/bin/env python3

import os
import json
from media_cleaner_bot import MediaCleanerBot
from advanced_cleaner import AdvancedMediaCleaner

def basic_usage_example():
    """Basic usage of the media cleaner bot."""
    print("=== Basic Usage Example ===")
    
    bot = MediaCleanerBot()
    
    test_file = "sample_image.jpg"
    if os.path.exists(test_file):
        result = bot.clean_single_file(test_file)
        
        if result['success']:
            print(f"✅ Successfully cleaned: {test_file}")
            print(f"Operations performed: {', '.join(result['operations'])}")
        else:
            print(f"❌ Failed to clean: {test_file}")
            print(f"Errors: {', '.join(result['errors'])}")
    else:
        print(f"Test file {test_file} not found. Create a sample image to test.")

def advanced_usage_example():
    """Advanced usage with steganography detection."""
    print("\n=== Advanced Usage Example ===")
    
    cleaner = AdvancedMediaCleaner()
    
    test_file = "sample_image.jpg"
    if os.path.exists(test_file):
        analysis = cleaner.detect_hidden_data(test_file)
        
        print(f"📊 Analysis for: {test_file}")
        print(f"File size: {analysis['file_size']} bytes")
        print(f"Entropy: {analysis['entropy']:.2f}")
        print(f"Steganography risk: {analysis['steganography_risk']}")
        
        if analysis['recommendations']:
            print("Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  - {rec}")
        
        result = cleaner.advanced_clean_single_file(test_file)
        if result['success']:
            print(f"✅ Advanced cleaning completed")
            print(f"Operations: {', '.join(result['operations'])}")
    else:
        print(f"Test file {test_file} not found.")

def batch_processing_example():
    """Example of batch processing a directory."""
    print("\n=== Batch Processing Example ===")
    
    bot = MediaCleanerBot()
    
    test_directory = "test_media"
    if os.path.isdir(test_directory):
        results = bot.clean_directory(test_directory)
        
        print(f"📁 Batch processing results for: {test_directory}")
        print(f"Total files found: {results['total_files']}")
        print(f"Successfully processed: {results['processed_files']}")
        print(f"Failed: {results['failed_files']}")
        
        if results['file_results']:
            print("\nDetailed results:")
            for file_result in results['file_results'][:5]:
                status = "✅" if file_result['success'] else "❌"
                filename = os.path.basename(file_result['original_path'])
                print(f"  {status} {filename}")
    else:
        print(f"Test directory {test_directory} not found.")

def custom_config_example():
    """Example using custom configuration."""
    print("\n=== Custom Configuration Example ===")
    
    custom_config = {
        "remove_exif": True,
        "remove_video_metadata": True,
        "randomize_timestamps": False,
        "rename_files": True,
        "backup_originals": False,
        "output_directory": "cleaned_media",
        "log_level": "DEBUG"
    }
    
    with open("custom_config.json", "w") as f:
        json.dump(custom_config, f, indent=2)
    
    bot = MediaCleanerBot("custom_config.json")
    
    print("Custom configuration loaded:")
    for key, value in custom_config.items():
        print(f"  {key}: {value}")
    
    os.remove("custom_config.json")

def steganography_analysis_example():
    """Example of steganography analysis only."""
    print("\n=== Steganography Analysis Example ===")
    
    cleaner = AdvancedMediaCleaner()
    
    test_files = ["sample_image.jpg", "test_photo.png", "video_file.mp4"]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            analysis = cleaner.detect_hidden_data(test_file)
            
            print(f"\n📊 {test_file}:")
            print(f"  Entropy: {analysis['entropy']:.2f}")
            print(f"  Risk Level: {analysis['steganography_risk']}")
            print(f"  File Size: {analysis['file_size']} bytes")
            
            if analysis['suspicious_patterns']:
                print(f"  Suspicious patterns found: {len(analysis['suspicious_patterns'])}")
            
            if analysis['recommendations']:
                print("  Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"    - {rec}")

def performance_comparison_example():
    """Compare basic vs advanced cleaning performance."""
    print("\n=== Performance Comparison Example ===")
    
    import time
    
    test_file = "sample_image.jpg"
    if not os.path.exists(test_file):
        print(f"Test file {test_file} not found.")
        return
    
    basic_bot = MediaCleanerBot()
    advanced_bot = AdvancedMediaCleaner()
    
    start_time = time.time()
    basic_result = basic_bot.clean_single_file(test_file)
    basic_time = time.time() - start_time
    
    if os.path.exists(f"{test_file}.backup"):
        os.rename(f"{test_file}.backup", test_file)
    
    start_time = time.time()
    advanced_result = advanced_bot.advanced_clean_single_file(test_file)
    advanced_time = time.time() - start_time
    
    print(f"⏱️  Performance Comparison:")
    print(f"Basic cleaning: {basic_time:.3f}s")
    print(f"Advanced cleaning: {advanced_time:.3f}s")
    print(f"Time difference: {advanced_time - basic_time:.3f}s")
    
    print(f"\nBasic operations: {len(basic_result.get('operations', []))}")
    print(f"Advanced operations: {len(advanced_result.get('operations', []))}")

def create_test_files():
    """Create sample test files for demonstration."""
    print("\n=== Creating Test Files ===")
    
    try:
        from PIL import Image
        import random
        
        os.makedirs("test_media", exist_ok=True)
        
        for i in range(3):
            img = Image.new('RGB', (200, 200), 
                          color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            img.save(f"test_media/test_image_{i+1}.jpg", quality=95)
        
        img = Image.new('RGB', (150, 150), color='blue')
        img.save("sample_image.jpg", quality=95)
        
        print("✅ Test files created:")
        print("  - sample_image.jpg")
        print("  - test_media/test_image_1.jpg")
        print("  - test_media/test_image_2.jpg")
        print("  - test_media/test_image_3.jpg")
        
    except ImportError:
        print("❌ PIL not available. Cannot create test images.")

def cleanup_test_files():
    """Clean up test files created during examples."""
    print("\n=== Cleaning Up Test Files ===")
    
    import shutil
    
    files_to_remove = [
        "sample_image.jpg",
        "sample_image.jpg.backup",
        "custom_config.json"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
    
    if os.path.exists("test_media"):
        shutil.rmtree("test_media")
        print("Removed: test_media directory")

def main():
    """Run all examples."""
    print("🚀 Media Cleaner Bot - Usage Examples")
    print("=" * 50)
    
    create_test_files()
    
    basic_usage_example()
    advanced_usage_example()
    batch_processing_example()
    custom_config_example()
    steganography_analysis_example()
    performance_comparison_example()
    
    print("\n" + "=" * 50)
    print("Examples completed! Check the output above for results.")
    
    response = input("\nClean up test files? (y/n): ").lower().strip()
    if response == 'y':
        cleanup_test_files()

if __name__ == "__main__":
    main()