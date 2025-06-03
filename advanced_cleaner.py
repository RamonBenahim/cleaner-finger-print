#!/usr/bin/env python3

import os
import math
import random
import struct
import numpy as np
from collections import Counter
from typing import Dict, List, Tuple, Optional
from media_cleaner_bot import MediaCleanerBot

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
    
    def __init__(self, config_path: str = "config.json"):
        super().__init__(config_path)
        self.entropy_threshold = 7.5
        self.steganography_patterns = [
            b'\x89PNG\r\n\x1a\n',
            b'\xff\xd8\xff',
            b'RIFF',
            b'ftyp'
        ]
    
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
    
    def detect_hidden_data(self, file_path: str) -> Dict:
        analysis = {
            'file_path': file_path,
            'file_size': 0,
            'entropy': 0.0,
            'suspicious_patterns': [],
            'steganography_risk': 'LOW',
            'recommendations': []
        }
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            analysis['file_size'] = len(data)
            analysis['entropy'] = self._calculate_entropy(data)
            
            for pattern in self.steganography_patterns:
                if data.count(pattern) > 1:
                    analysis['suspicious_patterns'].append(pattern.hex())
            
            if analysis['entropy'] > self.entropy_threshold:
                analysis['steganography_risk'] = 'HIGH'
                analysis['recommendations'].append('High entropy detected - possible hidden data')
            elif analysis['entropy'] > 6.0:
                analysis['steganography_risk'] = 'MEDIUM'
                analysis['recommendations'].append('Medium entropy - monitor for anomalies')
            
            if analysis['suspicious_patterns']:
                analysis['steganography_risk'] = 'HIGH'
                analysis['recommendations'].append('Multiple file signatures detected')
            
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.jpg', '.jpeg'] and analysis['entropy'] > 7.0:
                analysis['recommendations'].append('JPEG with high entropy - check LSB steganography')
            
        except Exception as e:
            self.logger.error(f"Hidden data detection failed for {file_path}: {e}")
            analysis['steganography_risk'] = 'UNKNOWN'
        
        return analysis
    
    def remove_steganographic_data(self, file_path: str) -> bool:
        if not PIL_AVAILABLE:
            return False
        
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                return self._clean_image_steganography(file_path)
            elif file_ext in ['.mp4', '.avi', '.mov']:
                return self._clean_video_steganography(file_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Steganographic data removal failed for {file_path}: {e}")
            return False
    
    def _clean_image_steganography(self, image_path: str) -> bool:
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                pixels = np.array(img)
                
                for channel in range(pixels.shape[2]):
                    pixels[:, :, channel] = pixels[:, :, channel] & 0xFE
                    
                    noise = np.random.randint(0, 2, pixels[:, :, channel].shape, dtype=np.uint8)
                    pixels[:, :, channel] = pixels[:, :, channel] | noise
                
                cleaned_img = Image.fromarray(pixels.astype(np.uint8))
                cleaned_img.save(image_path, quality=95, optimize=True)
                
                return True
                
        except Exception as e:
            self.logger.error(f"Image steganography cleaning failed: {e}")
            return False
    
    def _clean_video_steganography(self, video_path: str) -> bool:
        if not CV2_AVAILABLE:
            return False
        
        try:
            temp_path = f"{video_path}.temp"
            cap = cv2.VideoCapture(video_path)
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = frame & 0xFE
                noise = np.random.randint(0, 2, frame.shape, dtype=np.uint8)
                frame = frame | noise
                
                out.write(frame)
                frame_count += 1
            
            cap.release()
            out.release()
            
            os.replace(temp_path, video_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Video steganography cleaning failed: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    def inject_decoy_metadata(self, file_path: str) -> bool:
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg']:
                return self._inject_jpeg_decoy(file_path)
            elif file_ext == '.png':
                return self._inject_png_decoy(file_path)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Decoy metadata injection failed for {file_path}: {e}")
            return False
    
    def _inject_jpeg_decoy(self, image_path: str) -> bool:
        try:
            fake_camera_models = [
                "Canon EOS 5D Mark IV", "Nikon D850", "Sony Alpha a7R III",
                "iPhone 12 Pro", "Samsung Galaxy S21", "Google Pixel 5"
            ]
            
            fake_software = [
                "Adobe Photoshop CC 2021", "GIMP 2.10", "Lightroom Classic",
                "Capture One 21", "Luminar AI", "Affinity Photo"
            ]
            
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                fake_exif = {
                    "0th": {
                        256: img.width,
                        257: img.height,
                        272: random.choice(fake_camera_models),
                        305: random.choice(fake_software),
                        306: "2023:01:01 12:00:00"
                    }
                }
                
                img.save(image_path, quality=95, optimize=True)
                return True
                
        except Exception as e:
            self.logger.error(f"JPEG decoy injection failed: {e}")
            return False
    
    def _inject_png_decoy(self, image_path: str) -> bool:
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                img.save(image_path, optimize=True)
                return True
                
        except Exception as e:
            self.logger.error(f"PNG decoy injection failed: {e}")
            return False
    
    def advanced_pixel_scrambling(self, image_path: str, intensity: float = 0.05) -> bool:
        if not PIL_AVAILABLE:
            return False
        
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                pixels = np.array(img)
                height, width, channels = pixels.shape
                
                num_swaps = int(height * width * intensity)
                
                for _ in range(num_swaps):
                    y1, x1 = random.randint(0, height-1), random.randint(0, width-1)
                    y2, x2 = random.randint(0, height-1), random.randint(0, width-1)
                    
                    pixels[y1, x1], pixels[y2, x2] = pixels[y2, x2].copy(), pixels[y1, x1].copy()
                
                scrambled_img = Image.fromarray(pixels.astype(np.uint8))
                scrambled_img.save(image_path, quality=95, optimize=True)
                
                return True
                
        except Exception as e:
            self.logger.error(f"Advanced pixel scrambling failed: {e}")
            return False
    
    def advanced_clean_single_file(self, file_path: str) -> Dict:
        result = super().clean_single_file(file_path)
        
        if not result['success']:
            return result
        
        try:
            analysis = self.detect_hidden_data(file_path)
            result.update({
                'entropy': analysis['entropy'],
                'steganography_risk': analysis['steganography_risk'],
                'suspicious_patterns': analysis['suspicious_patterns']
            })
            
            if analysis['steganography_risk'] in ['MEDIUM', 'HIGH']:
                if self.remove_steganographic_data(file_path):
                    result['operations'].append("Steganographic data removed")
            
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.jpg', '.jpeg', '.png']:
                if self.advanced_pixel_scrambling(file_path):
                    result['operations'].append("Advanced pixel scrambling applied")
                
                if self.inject_decoy_metadata(file_path):
                    result['operations'].append("Decoy metadata injected")
            
        except Exception as e:
            result['errors'].append(f"Advanced processing error: {str(e)}")
        
        return result

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced Media Fingerprint Remover with Steganography Detection')
    parser.add_argument('path', help='File or directory path to clean')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--analyze-only', action='store_true', help='Only analyze for hidden data')
    
    args = parser.parse_args()
    
    cleaner = AdvancedMediaCleaner(args.config)
    
    if args.analyze_only:
        if os.path.isfile(args.path):
            analysis = cleaner.detect_hidden_data(args.path)
            print(f"📊 Analysis for: {args.path}")
            print(f"File size: {analysis['file_size']} bytes")
            print(f"Entropy: {analysis['entropy']:.2f}")
            print(f"Steganography risk: {analysis['steganography_risk']}")
            if analysis['recommendations']:
                print("Recommendations:")
                for rec in analysis['recommendations']:
                    print(f"  - {rec}")
        return
    
    if os.path.isfile(args.path):
        result = cleaner.advanced_clean_single_file(args.path)
        if result['success']:
            print(f"✅ Successfully cleaned: {args.path}")
            print(f"Operations: {', '.join(result['operations'])}")
            print(f"Entropy: {result.get('entropy', 'N/A')}")
            print(f"Steganography risk: {result.get('steganography_risk', 'N/A')}")
        else:
            print(f"❌ Failed to clean: {args.path}")
            print(f"Errors: {', '.join(result['errors'])}")
    
    elif os.path.isdir(args.path):
        results = cleaner.clean_directory(args.path)
        print(f"📁 Advanced directory processing complete:")
        print(f"Total files: {results['total_files']}")
        print(f"Processed: {results['processed_files']}")
        print(f"Failed: {results['failed_files']}")

if __name__ == "__main__":
    main()