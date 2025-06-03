#!/usr/bin/env python3

import os
import tempfile
from media_cleaner_bot import MediaCleanerBot
from advanced_cleaner import AdvancedMediaCleaner

def create_sample_image():
    try:
        from PIL import Image, ExifTags
        import random
        
        img = Image.new('RGB', (800, 600), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        
        temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
        img.save(temp_file.name, 'JPEG', quality=95)
        
        return temp_file.name
        
    except ImportError:
        print("PIL not available for creating sample image")
        return None

def example_basic_cleaning():
    print("Example: Basic Cleaning")
    print("=" * 40)
    
    sample_image = create_sample_image()
    if not sample_image:
        print("ERROR: Could not create sample image")
        return
    
    try:
        bot = MediaCleanerBot()
        
        print(f"Original file: {sample_image}")
        print(f"File size: {os.path.getsize(sample_image)} bytes")
        
        result = bot.clean_single_file(sample_image)
        
        print(f"Cleaning successful: {result['success']}")
        print(f"Operations performed: {', '.join(result['operations'])}")
        
        if result['errors']:
            print(f"Errors: {', '.join(result['errors'])}")
        
        print(f"Final file: {result['cleaned_path']}")
        print(f"Final size: {os.path.getsize(result['cleaned_path'])} bytes")
        
    finally:
        if os.path.exists(sample_image):
            os.unlink(sample_image)
        if sample_image != result.get('cleaned_path') and os.path.exists(result.get('cleaned_path', '')):
            os.unlink(result['cleaned_path'])

def example_advanced_cleaning():
    print("\nExample: Advanced Cleaning with Steganography Detection")
    print("=" * 60)
    
    sample_image = create_sample_image()
    if not sample_image:
        print("ERROR: Could not create sample image")
        return
    
    try:
        advanced_cleaner = AdvancedMediaCleaner()
        
        print(f"Original file: {sample_image}")
        
        analysis = advanced_cleaner.detect_hidden_data(sample_image)
        print(f"Entropy: {analysis['entropy']:.4f}")
        print(f"Steganography risk: {analysis['steganography_risk']}")
        print(f"Suspicious patterns: {len(analysis['suspicious_patterns'])}")
        
        result = advanced_cleaner.advanced_clean_single_file(sample_image)
        
        print(f"Advanced cleaning successful: {result['success']}")
        print(f"Operations performed: {', '.join(result['operations'])}")
        
        if 'entropy' in result:
            print(f"Final entropy: {result['entropy']:.4f}")
            print(f"Final risk level: {result['steganography_risk']}")
        
    finally:
        if os.path.exists(sample_image):
            os.unlink(sample_image)
        if sample_image != result.get('cleaned_path') and os.path.exists(result.get('cleaned_path', '')):
            os.unlink(result['cleaned_path'])

def example_batch_processing():
    print("\nExample: Batch Processing")
    print("=" * 30)
    
    sample_files = []
    
    try:
        for i in range(3):
            sample_file = create_sample_image()
            if sample_file:
                sample_files.append(sample_file)
        
        if not sample_files:
            print("ERROR: Could not create sample files")
            return
        
        bot = MediaCleanerBot()
        
        print(f"Processing {len(sample_files)} files...")
        
        successful = 0
        for file_path in sample_files:
            result = bot.clean_single_file(file_path)
            if result['success']:
                successful += 1
                print(f"SUCCESS: {os.path.basename(file_path)}")
            else:
                print(f"FAILED: {os.path.basename(file_path)}")
        
        print(f"Batch processing complete: {successful}/{len(sample_files)} successful")
        
    finally:
        for file_path in sample_files:
            if os.path.exists(file_path):
                os.unlink(file_path)
            backup_path = f"{file_path}.backup"
            if os.path.exists(backup_path):
                os.unlink(backup_path)

def example_configuration():
    print("\nExample: Custom Configuration")
    print("=" * 35)
    
    custom_config = {
        "remove_exif": True,
        "remove_video_metadata": False,
        "randomize_timestamps": True,
        "rename_files": True,
        "backup_originals": False,
        "log_level": "DEBUG"
    }
    
    import json
    config_file = "custom_config.json"
    
    try:
        with open(config_file, 'w') as f:
            json.dump(custom_config, f, indent=2)
        
        bot = MediaCleanerBot(config_file)
        
        print("Custom configuration loaded:")
        for key, value in custom_config.items():
            print(f"  {key}: {value}")
        
        sample_image = create_sample_image()
        if sample_image:
            result = bot.clean_single_file(sample_image, rename_file=True)
            print(f"File processed with custom config: {result['success']}")
            print(f"Operations: {', '.join(result['operations'])}")
            
            if os.path.exists(sample_image):
                os.unlink(sample_image)
            if result['cleaned_path'] != sample_image and os.path.exists(result['cleaned_path']):
                os.unlink(result['cleaned_path'])
        
    finally:
        if os.path.exists(config_file):
            os.unlink(config_file)

def main():
    print("Media Cleaner Bot - Usage Examples")
    print("=" * 50)
    
    try:
        example_basic_cleaning()
        example_advanced_cleaning()
        example_batch_processing()
        example_configuration()
        
        print("\nAll examples completed successfully!")
        print("\nTo use the GUI batch processor, run:")
        print("python batch_processor.py")
        
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    main()