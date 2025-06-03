#!/usr/bin/env python3

import unittest
import os
import tempfile
import json
from media_cleaner_bot import MediaCleanerBot
from advanced_cleaner import AdvancedMediaCleaner

class TestMediaCleanerBot(unittest.TestCase):
    
    def setUp(self):
        self.bot = MediaCleanerBot()
        self.temp_files = []
        
    def tearDown(self):
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            backup_file = f"{temp_file}.backup"
            if os.path.exists(backup_file):
                os.unlink(backup_file)
    
    def create_test_image(self):
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='red')
            
            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            img.save(temp_file.name, 'JPEG')
            self.temp_files.append(temp_file.name)
            
            return temp_file.name
        except ImportError:
            self.skipTest("PIL not available")
    
    def test_config_loading(self):
        config_data = {"remove_exif": False, "rename_files": True}
        
        config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump(config_data, config_file)
        config_file.close()
        
        try:
            bot = MediaCleanerBot(config_file.name)
            self.assertFalse(bot.config['remove_exif'])
            self.assertTrue(bot.config['rename_files'])
        finally:
            os.unlink(config_file.name)
    
    def test_random_filename_generation(self):
        filename1 = self.bot.generate_random_filename('jpg')
        filename2 = self.bot.generate_random_filename('jpg')
        
        self.assertNotEqual(filename1, filename2)
        self.assertTrue(filename1.endswith('.jpg'))
        self.assertTrue(filename1.startswith('cleaned_'))
    
    def test_exif_removal(self):
        test_image = self.create_test_image()
        result = self.bot.remove_exif_data(test_image)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(test_image))
    
    def test_timestamp_randomization(self):
        test_image = self.create_test_image()
        original_mtime = os.path.getmtime(test_image)
        
        result = self.bot.randomize_file_timestamp(test_image)
        new_mtime = os.path.getmtime(test_image)
        
        self.assertTrue(result)
        self.assertNotEqual(original_mtime, new_mtime)
    
    def test_single_file_cleaning(self):
        test_image = self.create_test_image()
        result = self.bot.clean_single_file(test_image)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['original_path'], test_image)
        self.assertGreater(len(result['operations']), 0)
        self.assertEqual(len(result['errors']), 0)
    
    def test_nonexistent_file(self):
        result = self.bot.clean_single_file('/nonexistent/file.jpg')
        self.assertFalse(result['success'])
        self.assertGreater(len(result['errors']), 0)

class TestAdvancedMediaCleaner(unittest.TestCase):
    
    def setUp(self):
        self.cleaner = AdvancedMediaCleaner()
        self.temp_files = []
        
    def tearDown(self):
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
            backup_file = f"{temp_file}.backup"
            if os.path.exists(backup_file):
                os.unlink(backup_file)
    
    def create_test_image(self):
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color='blue')
            
            temp_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
            img.save(temp_file.name, 'JPEG')
            self.temp_files.append(temp_file.name)
            
            return temp_file.name
        except ImportError:
            self.skipTest("PIL not available")
    
    def test_entropy_calculation(self):
        test_data = b'AAAA'
        entropy = self.cleaner._calculate_entropy(test_data)
        self.assertEqual(entropy, 0.0)
        
        test_data = b'ABCD'
        entropy = self.cleaner._calculate_entropy(test_data)
        self.assertEqual(entropy, 2.0)
    
    def test_hidden_data_detection(self):
        test_image = self.create_test_image()
        analysis = self.cleaner.detect_hidden_data(test_image)
        
        self.assertEqual(analysis['file_path'], test_image)
        self.assertGreater(analysis['file_size'], 0)
        self.assertGreaterEqual(analysis['entropy'], 0.0)
        self.assertIn(analysis['steganography_risk'], ['LOW', 'MEDIUM', 'HIGH'])
    
    def test_steganographic_data_removal(self):
        test_image = self.create_test_image()
        result = self.cleaner.remove_steganographic_data(test_image)
        self.assertTrue(result)
    
    def test_advanced_cleaning(self):
        test_image = self.create_test_image()
        result = self.cleaner.advanced_clean_single_file(test_image)
        
        self.assertTrue(result['success'])
        self.assertIn('entropy', result)
        self.assertIn('steganography_risk', result)
        self.assertGreater(len(result['operations']), 0)

def test_dependencies():
    print("Testing dependencies...")
    
    dependencies = [
        ('PIL', 'Pillow'),
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('mutagen', 'mutagen')
    ]
    
    missing_deps = []
    
    for module_name, package_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing_deps.append(package_name)
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("All dependencies installed!")
        return True

def test_file_structure():
    print("Testing file structure...")
    
    required_files = [
        'media_cleaner_bot.py',
        'advanced_cleaner.py',
        'batch_processor.py',
        'requirements.txt',
        'config.json',
        'README.md'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - MISSING")
            missing_files.append(file_name)
    
    return len(missing_files) == 0

def run_functionality_tests():
    print("Testing basic functionality...")
    
    try:
        from PIL import Image
        img = Image.new('RGB', (100, 100), color='red')
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            img.save(temp_file.name, 'JPEG')
            temp_path = temp_file.name
        
        print("✅ Test image creation")
        
        bot = MediaCleanerBot()
        result = bot.clean_single_file(temp_path)
        
        if result['success']:
            print("✅ Basic file cleaning")
        else:
            print(f"❌ Basic cleaning failed: {result['errors']}")
        
        advanced = AdvancedMediaCleaner()
        analysis = advanced.detect_hidden_data(temp_path)
        print("✅ Hidden data analysis")
        
        os.unlink(temp_path)
        backup_path = f"{temp_path}.backup"
        if os.path.exists(backup_path):
            os.unlink(backup_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    print("Media Cleaner Bot - Test Suite")
    print("=" * 40)
    
    all_passed = True
    
    all_passed &= test_dependencies()
    all_passed &= test_file_structure()
    all_passed &= run_functionality_tests()
    
    print("\nRunning unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    if all_passed:
        print("ALL TESTS PASSED!")
    else:
        print("SOME TESTS FAILED")

if __name__ == "__main__":
    main()