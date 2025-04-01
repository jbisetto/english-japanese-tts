#!/usr/bin/env python3
"""
NLTK Data Downloader for English-Japanese TTS System

This script downloads the required NLTK data packages for the text-to-speech system.
Required packages:
- punkt: For sentence tokenization and handling abbreviations
- averaged_perceptron_tagger: For part-of-speech tagging (used in text processing)

Usage:
    python download_nltk_data.py

The script will create the NLTK data directory if it doesn't exist and download
the required packages. It will skip packages that are already downloaded.
"""

import nltk
import sys
from pathlib import Path

def download_nltk_data():
    """Download required NLTK data packages."""
    required_packages = ['punkt', 'averaged_perceptron_tagger']
    
    try:
        for package in required_packages:
            print(f"Downloading {package}...")
            nltk.download(package, quiet=True)
        print("Successfully downloaded all required NLTK data.")
        return True
    except Exception as e:
        print(f"Error downloading NLTK data: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = download_nltk_data()
    sys.exit(0 if success else 1) 