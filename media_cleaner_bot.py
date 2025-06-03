#!/usr/bin/env python3

import os
import sys
import json
import logging
import tempfile
import shutil
import string
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

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
    def __init__(self, config_path: str = "config.json"):
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_path: str) -> dict:
        default_config = {
            "remove_exif": True,
            "remove_video_metadata": True,
            "randomize_timestamps": True,
            "rename_files": False,
            "backup_originals": True,
            "output_directory": "cleaned_media",
            "log_level": "INFO"
        }
        
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_path} not found, using defaults")
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in {config_path}, using defaults")
            
        return default_config
    
    def setup_logging(self):
        log_level = getattr(logging, self.config.get('log_level', 'INFO'))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('media_cleaner.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def generate_random_filename(self, extension: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
        return f"cleaned_{timestamp}_{random_suffix}.{extension}"

    def remove_exif_data(self, image_path: str) -> bool:
        if not PIL_AVAILABLE:
            self.logger.warning("PIL not available, skipping EXIF removal")
            return False
            
        try:
            with Image.open(image_path) as img:
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    clean_img = Image.new(img.mode, img.size)
                    clean_img.putdata(list(img.getdata()))
                    clean_img.save(image_path, quality=95, optimize=True)
                    self.logger.info(f"EXIF data removed from: {image_path}")
                    return True
                else:
                    self.logger.info(f"No EXIF data found in: {image_path}")
                    return True
        except Exception as e:
            self.logger.error(f"Error removing EXIF from {image_path}: {e}")
            return False

    def remove_video_metadata(self, video_path: str) -> bool:
        if not MUTAGEN_AVAILABLE:
            self.logger.warning("Mutagen not available, skipping video metadata removal")
            return False
            
        try:
            audio_file = MutagenFile(video_path)
            if audio_file is not None:
                audio_file.delete()
                audio_file.save()
                self.logger.info(f"Video metadata removed from: {video_path}")
                return True
            else:
                self.logger.info(f"No metadata found in: {video_path}")
                return True
        except Exception as e:
            self.logger.error(f"Error removing video metadata from {video_path}: {e}")
            return False

    def randomize_file_timestamp(self, file_path: str) -> bool:
        try:
            random_timestamp = random.randint(1577836800, 1893456000)
            os.utime(file_path, (random_timestamp, random_timestamp))
            self.logger.info(f"Timestamp randomized for: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error randomizing timestamp for {file_path}: {e}")
            return False

    def clean_single_file(self, file_path: str, rename_file: bool = False) -> dict:
        result = {
            'success': False,
            'original_path': file_path,
            'cleaned_path': file_path,
            'operations': [],
            'errors': []
        }
        
        if not os.path.exists(file_path):
            result['errors'].append(f"File not found: {file_path}")
            return result
            
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if self.config.get('backup_originals', True):
                backup_path = f"{file_path}.backup"
                shutil.copy2(file_path, backup_path)
                result['operations'].append("Backup created")
            
            if file_ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'] and self.config.get('remove_exif', True):
                if self.remove_exif_data(file_path):
                    result['operations'].append("EXIF data removed")
            
            if file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv'] and self.config.get('remove_video_metadata', True):
                if self.remove_video_metadata(file_path):
                    result['operations'].append("Video metadata removed")
            
            if self.config.get('randomize_timestamps', True):
                if self.randomize_file_timestamp(file_path):
                    result['operations'].append("Timestamp randomized")
            
            if rename_file or self.config.get('rename_files', False):
                new_filename = self.generate_random_filename(file_ext[1:])
                new_path = os.path.join(os.path.dirname(file_path), new_filename)
                os.rename(file_path, new_path)
                result['cleaned_path'] = new_path
                result['operations'].append("File renamed")
            
            result['success'] = True
            self.logger.info(f"Successfully cleaned: {file_path}")
            
        except Exception as e:
            result['errors'].append(str(e))
            self.logger.error(f"Error cleaning {file_path}: {e}")
            
        return result

    def clean_directory(self, directory_path: str) -> dict:
        results = {
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'file_results': []
        }
        
        if not os.path.isdir(directory_path):
            self.logger.error(f"Directory not found: {directory_path}")
            return results
            
        supported_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.mp4', '.avi', '.mov', '.mkv', '.wmv']
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file_path).suffix.lower()
                
                if file_ext in supported_extensions:
                    results['total_files'] += 1
                    result = self.clean_single_file(file_path)
                    results['file_results'].append(result)
                    
                    if result['success']:
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
        
        self.logger.info(f"Directory cleaning complete. Success: {results['successful']}, Failed: {results['failed']}")
        return results

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Media Cleaner Bot - Remove fingerprints from media files")
    parser.add_argument("path", help="File or directory path to clean")
    parser.add_argument("--config", default="config.json", help="Configuration file path")
    parser.add_argument("--rename", action="store_true", help="Rename files with random names")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    bot = MediaCleanerBot(args.config)
    
    if os.path.isfile(args.path):
        result = bot.clean_single_file(args.path, args.rename)
        print(f"File: {result['original_path']}")
        print(f"Success: {result['success']}")
        print(f"Operations: {', '.join(result['operations'])}")
        if result['errors']:
            print(f"Errors: {', '.join(result['errors'])}")
    elif os.path.isdir(args.path):
        results = bot.clean_directory(args.path)
        print(f"Total files processed: {results['total_files']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")
    else:
        print(f"Error: Path not found - {args.path}")

if __name__ == "__main__":
    main()