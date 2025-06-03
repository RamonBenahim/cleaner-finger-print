# Media Fingerprint Remover

Remove digital fingerprints and traces from images and videos.

- **EXIF Data Removal**: Removes all metadata from images
- **Video Metadata Cleaning**: Cleans metadata from video files
- **Watermark Removal**: Removes visible watermarks using AI
- **Timestamp Randomization**: Modifies file timestamps
- **File Renaming**: Generates random names for files
- **Steganography Detection**: Detects and removes hidden data
- **Pixel Randomization**: Adds subtle noise to prevent analysis
- **Batch Processing**: Process multiple files at once
- **GUI Interface**: Easy-to-use graphical interface

## Installation

### Quick Install

```bash
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Single file
python3 media_cleaner_bot.py image.jpg

# Directory
python3 media_cleaner_bot.py /path/to/directory

# Advanced cleaning
python3 advanced_cleaner.py image.jpg
```

### GUI Interface

```bash
python3 batch_processor.py
```

### Examples

```bash
python3 example_usage.py
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "remove_exif": true,
  "remove_watermarks": true,
  "randomize_timestamps": true,
  "rename_files": false,
  "pixel_randomization_intensity": 0.005
}
```

## High Performance Mode

For better performance, compile C extensions:

```bash
chmod +x compile_extensions.sh
./compile_extensions.sh
python3 hybrid_cleaner.py image.jpg
```

## Testing

```bash
python3 test_bot.py
```

## Important Notes

- **Use only on files you own**
- **Always backup important files before processing**
- **Test on small files first**
- **Check local laws regarding metadata removal**

## License

MIT License - See LICENSE file for details

## Disclaimer

This tool is for educational and legitimate privacy purposes only. Users are responsible for complying with applicable laws and regulations.
