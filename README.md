# Advanced Media Fingerprint Remover

Remove digital fingerprints and traces from images and videos.

### Core Functionality

- **EXIF Data Removal** - Strip metadata from images
- **Video Metadata Cleaning** - Remove metadata from video files
- **Timestamp Randomization** - Randomize file creation/modification times
- **Pixel Randomization** - Subtle pixel modifications to prevent fingerprinting
- **File Renaming** - Generate random filenames

### Advanced Features

- **Steganography Detection** - Analyze files for hidden data using entropy analysis
- **LSB Steganography Removal** - Clean least significant bit modifications
- **Decoy Metadata Injection** - Add fake metadata to mislead analysis
- **Advanced Pixel Scrambling** - Sophisticated pixel manipulation
- **Batch Processing GUI** - User-friendly interface for bulk operations

### Performance

- **C Extensions** - Optional C modules for performance-critical operations
- **Hybrid Processing** - Combine Python flexibility with C speed
- **Multi-threading** - Parallel processing for large batches

## Installation

### Quick Install

```bash
chmod +x install.sh
./install.sh
```

### Manual Install

```bash
pip install -r requirements.txt
python setup.py build_ext --inplace  # Optional: C extensions
```

### Dependencies

- Python 3.7+
- Pillow (PIL)
- OpenCV
- NumPy
- Mutagen
- Tkinter (for GUI)

## Usage

### Command Line

**Basic cleaning:**

```bash
python media_cleaner_bot.py image.jpg
python media_cleaner_bot.py /path/to/directory
```

**Advanced cleaning with steganography detection:**

```bash
python advanced_cleaner.py image.jpg
python advanced_cleaner.py --analyze-only suspicious_file.jpg
```

**Batch processing GUI:**

```bash
python batch_processor.py
```

### Python API

**Basic usage:**

```python
from media_cleaner_bot import MediaCleanerBot

bot = MediaCleanerBot()
result = bot.clean_single_file("image.jpg")

if result['success']:
    print(f"Operations: {result['operations']}")
```

**Advanced usage:**

```python
from advanced_cleaner import AdvancedMediaCleaner

cleaner = AdvancedMediaCleaner()

# Analyze for hidden data
analysis = cleaner.detect_hidden_data("image.jpg")
print(f"Entropy: {analysis['entropy']}")
print(f"Risk: {analysis['steganography_risk']}")

# Advanced cleaning
result = cleaner.advanced_clean_single_file("image.jpg")
```

## Configuration

Create `config.json` to customize behavior:

```json
{
  "remove_exif": true,
  "remove_video_metadata": true,
  "randomize_timestamps": true,
  "rename_files": false,
  "backup_originals": true,
  "output_directory": "cleaned_media",
  "log_level": "INFO"
}
```

## Supported Formats

### Images

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff)
- BMP (.bmp)

### Videos

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WMV (.wmv)

## Security Features

### Steganography Detection

- **Entropy Analysis** - Detect unusual data patterns
- **Pattern Recognition** - Identify multiple file signatures
- **LSB Analysis** - Check for least significant bit modifications

### Cleaning Methods

- **Metadata Stripping** - Remove all embedded metadata
- **Pixel Manipulation** - Modify pixels to destroy hidden data
- **Recompression** - Save files with clean compression
- **Timestamp Obfuscation** - Randomize file timestamps

## Performance Optimization

### C Extensions

For maximum performance, compile the C extensions:

```bash
python setup.py build_ext --inplace
python hybrid_cleaner.py image.jpg  # Uses C extensions
```

### Batch Processing

Use the GUI or directory processing for efficient bulk operations:

```python
bot = MediaCleanerBot()
results = bot.clean_directory("/path/to/media")
```

## Testing

Run the test suite:

```bash
python test_bot.py
```

Run examples:

```bash
python example_usage.py
```

## Project Structure

```
├── media_cleaner_bot.py      # Core bot functionality
├── advanced_cleaner.py       # Advanced features
├── batch_processor.py        # GUI application
├── hybrid_cleaner.py         # C extension integration
├── fast_cleaner.c           # C performance extensions
├── example_usage.py         # Usage examples
├── test_bot.py             # Test suite
├── config.json             # Configuration
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool is for legitimate privacy and security purposes. Users are responsible for complying with applicable laws and regulations. Do not use for illegal activities.

## Support

- Check the examples in `example_usage.py`
- Run tests with `test_bot.py`
- Review configuration options in `config.json`
- For issues, check the logs in `media_cleaner.log`
