#!/usr/bin/env python3
"""
Hybrid Media Cleaner - Uses C extensions for performance-critical operations
"""

import os
from media_cleaner_bot import MediaCleanerBot

try:
    import fast_cleaner
    C_EXTENSIONS_AVAILABLE = True
    print("C extensions loaded - High performance mode")
except ImportError:
    C_EXTENSIONS_AVAILABLE = False
    print("WARNING: C extensions not available - Using Python fallback")

class HybridMediaCleaner(MediaCleanerBot):
    """Enhanced cleaner with C extensions for performance"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_c_extensions = C_EXTENSIONS_AVAILABLE
        
    def remove_steganographic_patterns_fast(self, file_path: str) -> bool:
        if not self.use_c_extensions:
            return self.remove_steganographic_patterns_python(file_path)
            
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            patterns = [
                b'\xFF\xE0',
                b'\xFF\xE1',
                b'\xFF\xE2',
                b'\xFF\xED',
                b'\xFF\xEE',
            ]
            
            cleaned_data = fast_cleaner.remove_byte_patterns(data, patterns)
            
            with open(file_path, 'wb') as f:
                f.write(cleaned_data)
                
            self.logger.info(f"Fast pattern removal applied to: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in fast pattern removal: {e}")
            return False
            
    def add_pixel_noise_fast(self, image_path: str, intensity: float = 0.01) -> bool:
        if not self.use_c_extensions:
            return self.add_pixel_noise_python(image_path, intensity)
            
        try:
            import cv2
            import numpy as np
            
            img = cv2.imread(image_path)
            if img is None:
                return False
                
            flat_data = img.flatten().tobytes()
            
            noisy_data = fast_cleaner.add_pixel_noise(flat_data, intensity)
            
            noisy_array = np.frombuffer(noisy_data, dtype=np.uint8)
            noisy_img = noisy_array.reshape(img.shape)
            
            cv2.imwrite(image_path, noisy_img)
            self.logger.info(f"Fast pixel noise applied to: {image_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in fast pixel noise: {e}")
            return False
            
    def calculate_entropy_fast(self, file_path: str) -> float:
        if not self.use_c_extensions:
            return self.calculate_entropy_python(file_path)
            
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            entropy = fast_cleaner.calculate_entropy(data)
            return entropy
            
        except Exception as e:
            self.logger.error(f"Error in fast entropy calculation: {e}")
            return 0.0
            
    def remove_steganographic_patterns_python(self, file_path: str) -> bool:
        from advanced_cleaner import AdvancedMediaCleaner
        cleaner = AdvancedMediaCleaner()
        return cleaner.remove_steganographic_data(file_path)
        
    def add_pixel_noise_python(self, image_path: str, intensity: float = 0.01) -> bool:
        from advanced_cleaner import AdvancedMediaCleaner
        cleaner = AdvancedMediaCleaner()
        return cleaner.randomize_pixel_values(image_path, intensity)
        
    def calculate_entropy_python(self, file_path: str) -> float:
        from advanced_cleaner import AdvancedMediaCleaner
        cleaner = AdvancedMediaCleaner()
        with open(file_path, 'rb') as f:
            data = f.read()
        return cleaner._calculate_entropy(data)
        
    def clean_single_file_hybrid(self, file_path: str, rename_file: bool = False) -> dict:
        result = super().clean_single_file(file_path, rename_file)
        
        if result['success']:
            if self.use_c_extensions:
                self.logger.info(f"Applying high-performance cleaning to: {file_path}")
                
                if self.remove_steganographic_patterns_fast(file_path):
                    result['operations'].append("Fast pattern removal")
                    
                if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if self.add_pixel_noise_fast(file_path):
                        result['operations'].append("Fast pixel noise")
                        
                entropy = self.calculate_entropy_fast(file_path)
                result['entropy'] = entropy
                result['operations'].append(f"Entropy analysis: {entropy:.4f}")
                
        return result

def benchmark_performance():
    import time
    import tempfile
    from PIL import Image
    import numpy as np
    
    print("Performance Benchmark: C vs Python")
    print("=" * 50)
    
    test_img = Image.new('RGB', (1000, 1000), color='red')
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        test_img.save(f.name, 'JPEG')
        test_file = f.name
    
    try:
        cleaner = HybridMediaCleaner()
        
        print("Testing entropy calculation...")
        
        start = time.time()
        entropy_py = cleaner.calculate_entropy_python(test_file)
        time_py = time.time() - start
        
        if C_EXTENSIONS_AVAILABLE:
            start = time.time()
            entropy_c = cleaner.calculate_entropy_fast(test_file)
            time_c = time.time() - start
            
            speedup = time_py / time_c if time_c > 0 else 0
            
            print(f"Python: {entropy_py:.4f} ({time_py:.4f}s)")
            print(f"C:      {entropy_c:.4f} ({time_c:.4f}s)")
            print(f"Speedup: {speedup:.2f}x")
        else:
            print(f"Python: {entropy_py:.4f} ({time_py:.4f}s)")
            print("C extensions not available")
            
    finally:
        os.unlink(test_file)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Hybrid Media Cleaner with C extensions")
    parser.add_argument("path", help="File or directory to clean")
    parser.add_argument("--benchmark", action="store_true", help="Run performance benchmark")
    parser.add_argument("--force-python", action="store_true", help="Force Python mode")
    
    args = parser.parse_args()
    
    if args.benchmark:
        benchmark_performance()
        return
        
    cleaner = HybridMediaCleaner()
    
    if args.force_python:
        cleaner.use_c_extensions = False
        print("Forced Python mode")
    
    print(f"Processing: {args.path}")
    print(f"High performance: {'Yes' if cleaner.use_c_extensions else 'No'}")
    
    if os.path.isfile(args.path):
        result = cleaner.clean_single_file_hybrid(args.path)
        print(f"Operations: {', '.join(result['operations'])}")
    else:
        print("Directory processing not implemented in this example")

if __name__ == "__main__":
    main()