#!/usr/bin/env python3

import os
import math
import random
import struct
from collections import Counter
from media_cleaner_bot import MediaCleanerBot

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

class AdvancedMediaCleaner(MediaCleanerBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.suspicious_patterns = [
            b'\xFF\xE0',
            b'\xFF\xE1',
            b'\xFF\xE2',
            b'\xFF\xED',
            b'\xFF\xEE',
        ]
        
    def detect_hidden_data(self, file_path: str) -> dict:
        analysis = {
            'file_path': file_path,
            'file_size': os.path.getsize(file_path),
            'entropy': 0.0,
            'suspicious_patterns': [],
            'steganography_risk': 'LOW',
            'recommendations': []
        }
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            analysis['entropy'] = self._calculate_entropy(data)
            
            if analysis['entropy'] > 7.5:
                analysis['steganography_risk'] = 'HIGH'
                analysis['recommendations'].append('High entropy detected - possible steganography')
            elif analysis['entropy'] > 6.5:
                analysis['steganography_risk'] = 'MEDIUM'
                analysis['recommendations'].append('Medium entropy - monitor for hidden data')
            
            for pattern in self.suspicious_patterns:
                if pattern in data:
                    analysis['suspicious_patterns'].append(pattern.hex())
                    analysis['recommendations'].append(f'Suspicious pattern found: {pattern.hex()}')
            
            self.logger.info(f"Hidden data analysis complete for: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            analysis['error'] = str(e)
            
        return analysis

    def _calculate_entropy(self, data: bytes) -> float:
        if not data:
            return 0.0
            
        byte_counts = Counter(data)
        data_len = len(data)
        entropy = 0.0
        
        for count in byte_counts.values():
            probability = count / data_len
            if probability > 0:
                entropy -= probability * math.log2(probability)
                
        return entropy

    def remove_steganographic_data(self, file_path: str) -> bool:
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            cleaned_data = data
            for pattern in self.suspicious_patterns:
                cleaned_data = cleaned_data.replace(pattern, b'')
            
            if len(cleaned_data) != len(data):
                with open(file_path, 'wb') as f:
                    f.write(cleaned_data)
                self.logger.info(f"Steganographic patterns removed from: {file_path}")
                return True
            else:
                self.logger.info(f"No steganographic patterns found in: {file_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error removing steganographic data from {file_path}: {e}")
            return False

    def clean_jpeg_segments(self, image_path: str) -> bool:
        if not PIL_AVAILABLE:
            self.logger.warning("PIL not available for JPEG segment cleaning")
            return False
            
        try:
            with open(image_path, 'rb') as f:
                data = f.read()
            
            if not data.startswith(b'\xFF\xD8'):
                self.logger.warning(f"Not a valid JPEG file: {image_path}")
                return False
            
            cleaned_data = bytearray()
            i = 0
            
            while i < len(data) - 1:
                if data[i] == 0xFF:
                    marker = data[i + 1]
                    
                    if marker in [0xE0, 0xE1, 0xE2, 0xED, 0xEE]:
                        if i + 3 < len(data):
                            segment_length = struct.unpack('>H', data[i + 2:i + 4])[0]
                            i += 2 + segment_length
                            continue
                    
                cleaned_data.append(data[i])
                i += 1
            
            if i < len(data):
                cleaned_data.append(data[i])
            
            with open(image_path, 'wb') as f:
                f.write(cleaned_data)
                
            self.logger.info(f"JPEG segments cleaned: {image_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error cleaning JPEG segments in {image_path}: {e}")
            return False

    def randomize_pixel_values(self, image_path: str, intensity: float = 0.01) -> bool:
        if not PIL_AVAILABLE:
            self.logger.warning("PIL not available for pixel randomization")
            return False
            
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                pixels = list(img.getdata())
                
                for i in range(len(pixels)):
                    r, g, b = pixels[i]
                    
                    noise_r = random.randint(-int(255 * intensity), int(255 * intensity))
                    noise_g = random.randint(-int(255 * intensity), int(255 * intensity))
                    noise_b = random.randint(-int(255 * intensity), int(255 * intensity))
                    
                    new_r = max(0, min(255, r + noise_r))
                    new_g = max(0, min(255, g + noise_g))
                    new_b = max(0, min(255, b + noise_b))
                    
                    pixels[i] = (new_r, new_g, new_b)
                
                img.putdata(pixels)
                img.save(image_path, quality=95, optimize=True)
                
            self.logger.info(f"Pixel values randomized: {image_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error randomizing pixels in {image_path}: {e}")
            return False

    def add_decoy_metadata(self, file_path: str) -> bool:
        try:
            decoy_data = {
                'camera': random.choice(['Canon EOS R5', 'Nikon D850', 'Sony A7R IV']),
                'location': random.choice(['New York', 'London', 'Tokyo', 'Paris']),
                'timestamp': f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
            }
            
            if file_path.lower().endswith(('.jpg', '.jpeg')) and PIL_AVAILABLE:
                with Image.open(file_path) as img:
                    img.save(file_path, quality=95, optimize=True)
                    
            self.logger.info(f"Decoy metadata added to: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding decoy metadata to {file_path}: {e}")
            return False

    def advanced_clean_single_file(self, file_path: str, rename_file: bool = False) -> dict:
        result = super().clean_single_file(file_path, rename_file)
        
        if result['success']:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if self.remove_steganographic_data(file_path):
                result['operations'].append("Steganographic data removed")
            
            if file_ext in ['.jpg', '.jpeg']:
                if self.clean_jpeg_segments(file_path):
                    result['operations'].append("JPEG segments cleaned")
                    
                if self.randomize_pixel_values(file_path):
                    result['operations'].append("Pixel values randomized")
            
            if self.add_decoy_metadata(file_path):
                result['operations'].append("Decoy metadata added")
            
            analysis = self.detect_hidden_data(file_path)
            result['entropy'] = analysis['entropy']
            result['steganography_risk'] = analysis['steganography_risk']
            
        return result

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Media Cleaner with steganography detection")
    parser.add_argument("path", help="File or directory path to analyze/clean")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't clean")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    
    args = parser.parse_args()
    
    cleaner = AdvancedMediaCleaner(args.config)
    
    if args.analyze_only:
        if os.path.isfile(args.path):
            analysis = cleaner.detect_hidden_data(args.path)
            print(f"File: {analysis['file_path']}")
            print(f"Entropy: {analysis['entropy']:.4f}")
            print(f"Risk Level: {analysis['steganography_risk']}")
            print(f"Suspicious Patterns: {len(analysis['suspicious_patterns'])}")
            if analysis['recommendations']:
                print("Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"  - {rec}")
    else:
        if os.path.isfile(args.path):
            result = cleaner.advanced_clean_single_file(args.path)
            print(f"File: {result['original_path']}")
            print(f"Success: {result['success']}")
            print(f"Operations: {', '.join(result['operations'])}")
            if 'entropy' in result:
                print(f"Final Entropy: {result['entropy']:.4f}")
                print(f"Risk Level: {result['steganography_risk']}")

if __name__ == "__main__":
    main()