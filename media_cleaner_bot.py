#!/usr/bin/env python3

import os
import json
import random
import string
import time
import hashlib
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image
    from PIL.ExifTags import TAGS
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

try:
    from mutagen import File as MutagenFile
    MUTAGEN_AVAILABLE = True
except ImportError:
    MUTAGEN_AVAILABLE = False

class MediaCleanerBot:
    
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp'}
    SUPPORTED_VIDEO_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def _load_config(self, config_path: str) -> dict:
        default_config = {
            "remove_exif": True,
            "remove_video_metadata": True,
            "randomize_timestamps": True,
            "rename_files": False,
            "backup_originals": True,
            "output_directory": "cleaned_media",
            "log_level": "INFO"
        }
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Config error: {e}. Using defaults.")
        
        return default_config
    
    def _setup_logging(self):
        level = getattr(logging, self.config.get('log_level', 'INFO'))
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('media_cleaner.log'),
                logging.StreamHandler()
            ]
        )
    
    def generate_random_filename(self, extension: str) -> str:
        random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
        return f"cleaned_{random_part}.{extension.lstrip('.')}"
    
    def create_backup(self, file_path: str) -> bool:
        if not self.config.get('backup_originals', True):
            return True
            
        try:
            backup_path = f"{file_path}.backup"
            if not os.path.exists(backup_path):
                with open(file_path, 'rb') as src, open(backup_path, 'wb') as dst:
                    dst.write(src.read())
            return True
        except Exception as e:
            self.logger.error(f"Backup failed for {file_path}: {e}")
            return False
    
    def remove_exif_data(self, image_path: str) -> bool:
        if not PIL_AVAILABLE:
            self.logger.warning("PIL not available for EXIF removal")
            return False
            
        try:
            with Image.open(image_path) as img:
                if hasattr(img, '_getexif') and img._getexif():
                    clean_img = Image.new(img.mode, img.size)
                    clean_img.putdata(list(img.getdata()))
                    clean_img.save(image_path, quality=95, optimize=True)
                    return True
            return True
        except Exception as e:
            self.logger.error(f"EXIF removal failed for {image_path}: {e}")
            return False
    
    def remove_video_metadata(self, video_path: str) -> bool:
        if not CV2_AVAILABLE:
            self.logger.warning("OpenCV not available for video metadata removal")
            return False
            
        try:
            temp_path = f"{video_path}.temp"
            cap = cv2.VideoCapture(video_path)
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            
            cap.release()
            out.release()
            
            os.replace(temp_path, video_path)
            return True
            
        except Exception as e:
            self.logger.error(f"Video metadata removal failed for {video_path}: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False
    
    def randomize_file_timestamp(self, file_path: str) -> bool:
        try:
            random_days = random.randint(-365, 365)
            random_seconds = random.randint(0, 86400)
            
            new_time = datetime.now() + timedelta(days=random_days, seconds=random_seconds)
            timestamp = new_time.timestamp()
            
            os.utime(file_path, (timestamp, timestamp))
            return True
        except Exception as e:
            self.logger.error(f"Timestamp randomization failed for {file_path}: {e}")
            return False
    
    def randomize_pixels(self, image_path: str, intensity: float = 0.01) -> bool:
        if not PIL_AVAILABLE:
            return False
            
        try:
            with Image.open(image_path) as img:
                if img.mode not in ['RGB', 'RGBA']:
                    img = img.convert('RGB')
                
                pixels = list(img.getdata())
                num_pixels_to_change = int(len(pixels) * intensity)
                
                for _ in range(num_pixels_to_change):
                    idx = random.randint(0, len(pixels) - 1)
                    if len(pixels[idx]) == 3:
                        r, g, b = pixels[idx]
                        r = max(0, min(255, r + random.randint(-2, 2)))
                        g = max(0, min(255, g + random.randint(-2, 2)))
                        b = max(0, min(255, b + random.randint(-2, 2)))
                        pixels[idx] = (r, g, b)
                
                new_img = Image.new(img.mode, img.size)
                new_img.putdata(pixels)
                new_img.save(image_path, quality=95, optimize=True)
                return True
                
        except Exception as e:
            self.logger.error(f"Pixel randomization failed for {image_path}: {e}")
            return False
    
    def clean_single_file(self, file_path: str) -> Dict:
        result = {
            'success': False,
            'original_path': file_path,
            'new_path': file_path,
            'operations': [],
            'errors': []
        }
        
        if not os.path.exists(file_path):
            result['errors'].append("File not found")
            return result
        
        file_ext = Path(file_path).suffix.lower()
        
        if not self.create_backup(file_path):
            result['errors'].append("Backup creation failed")
            return result
        else:
            result['operations'].append("Backup created")
        
        try:
            if file_ext in self.SUPPORTED_IMAGE_FORMATS:
                if self.config.get('remove_exif', True):
                    if self.remove_exif_data(file_path):
                        result['operations'].append("EXIF data removed")
                
                if self.randomize_pixels(file_path):
                    result['operations'].append("Pixels randomized")
            
            elif file_ext in self.SUPPORTED_VIDEO_FORMATS:
                if self.config.get('remove_video_metadata', True):
                    if self.remove_video_metadata(file_path):
                        result['operations'].append("Video metadata removed")
            
            if self.config.get('randomize_timestamps', True):
                if self.randomize_file_timestamp(file_path):
                    result['operations'].append("Timestamp randomized")
            
            if self.config.get('rename_files', False):
                new_filename = self.generate_random_filename(file_ext)
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                os.rename(file_path, new_path)
                result['new_path'] = new_path
                result['operations'].append(f"File renamed to {new_filename}")
            
            result['success'] = True
            
        except Exception as e:
            result['errors'].append(f"Processing error: {str(e)}")
        
        return result
    
    def clean_directory(self, directory_path: str) -> Dict:
        results = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'file_results': []
        }
        
        if not os.path.isdir(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return results
        
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file_path).suffix.lower()
                
                if file_ext in (self.SUPPORTED_IMAGE_FORMATS | self.SUPPORTED_VIDEO_FORMATS):
                    results['total_files'] += 1
                    
                    file_result = self.clean_single_file(file_path)
                    results['file_results'].append(file_result)
                    
                    if file_result['success']:
                        results['processed_files'] += 1
                        self.logger.info(f"Successfully processed: {file_path}")
                    else:
                        results['failed_files'] += 1
                        self.logger.error(f"Failed to process: {file_path}")
        
        return results
    
    def get_file_hash(self, file_path: str) -> str:
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception:
            return ""

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Advanced Media Fingerprint Remover')
    parser.add_argument('path', help='File or directory path to clean')
    parser.add_argument('--config', default='config.json', help='Configuration file path')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup creation')
    
    args = parser.parse_args()
    
    bot = MediaCleanerBot(args.config)
    
    if args.no_backup:
        bot.config['backup_originals'] = False
    
    if os.path.isfile(args.path):
        result = bot.clean_single_file(args.path)
        if result['success']:
            print(f"✅ Successfully cleaned: {args.path}")
            print(f"Operations: {', '.join(result['operations'])}")
        else:
            print(f"❌ Failed to clean: {args.path}")
            print(f"Errors: {', '.join(result['errors'])}")
    
    elif os.path.isdir(args.path):
        results = bot.clean_directory(args.path)
        print(f"📁 Directory processing complete:")
        print(f"Total files: {results['total_files']}")
        print(f"Processed: {results['processed_files']}")
        print(f"Failed: {results['failed_files']}")
    
    else:
        print(f"❌ Path not found: {args.path}")

if __name__ == "__main__":
    main()