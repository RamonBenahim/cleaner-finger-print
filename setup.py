from setuptools import setup, Extension
import numpy

# C extension module
fast_cleaner_module = Extension(
    'fast_cleaner',
    sources=['fast_cleaner.c'],
    include_dirs=[numpy.get_include()],
    extra_compile_args=['-O3', '-march=native']  # Optimization flags
)

setup(
    name='media-fingerprint-remover',
    version='1.0.0',
    description='Remove fingerprints and metadata from media files',
    ext_modules=[fast_cleaner_module],
    install_requires=[
        'Pillow>=9.0.0',
        'opencv-python>=4.5.0',
        'numpy>=1.21.0',
        'mutagen>=1.45.0'
    ],
    python_requires='>=3.7',
)