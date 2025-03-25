# English-Japanese Text-to-Speech System

This project implements a text-to-speech system that converts text containing both English and Japanese into natural-sounding speech using AWS Polly and Google Cloud TTS services.

## Overview

This system processes text input, detects language boundaries between English and Japanese sections, and generates speech appropriately based on the detected language. It ensures proper pronunciation and natural prosody for each language and merges speech segments into a coherent audio output.

## Dependencies

1. Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

2. Download required NLTK data:

    ```
    python download_nltk_data.py
    ```

## Environment Setup

1. Set the environment variables:

    For AWS Polly:
    ```
    AWS_REGION_NAME=your_aws_region
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    ENGLISH_VOICE_ID=your_english_voice_id
    JAPANESE_VOICE_ID=your_japanese_voice_id
    ```

    For Google Cloud TTS:
    ```
    GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google_cloud_credentials.json
    ```

## Usage

Run the example:

```
python examples/simple_tts.py
```

Note: You may need to add the current directory to the PYTHONPATH environment variable to run the example:

```
PYTHONPATH=. python examples/simple_tts.py
```

## Running the Demo Application

1. Ensure all dependencies are installed and NLTK data is downloaded (see Dependencies section)

2. Set the environment variables:

    The application requires the following environment variables to be set:

    * **AWS Polly:**
        * `AWS_ACCESS_KEY_ID`
        * `AWS_SECRET_ACCESS_KEY`
        * `AWS_REGION_NAME`
    * **Google Cloud TTS:**
        * `GOOGLE_APPLICATION_CREDENTIALS` (path to your Google Cloud service account key file)

3. Run the application:

    ```bash
    python demo/app.py
    ```

## Development

### Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

### Project Structure
- `src/`: Source code
  - `text/`: Text processing (language detection, sentence segmentation)
  - `speech/`: TTS service integrations
  - `output/`: Audio processing and format conversion
- `tests/`: Test suite
- `demo/`: Demo application
- `examples/`: Usage examples

## Supported Features
- Mixed English-Japanese text processing
- Intelligent sentence segmentation with abbreviation handling
- Multiple TTS service support (AWS Polly, Google Cloud TTS)
- Multiple output formats (WAV, MP3, OGG)
- Natural transitions between language segments
