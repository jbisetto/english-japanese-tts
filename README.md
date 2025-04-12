# English-Japanese Text-to-Speech System

This project implements a text-to-speech system that converts text containing both English and Japanese into natural-sounding speech using AWS Polly or Google Cloud TTS services. Currently, I have only tested with AWS Polly.

## Quick Links
- [Demo Application Guide](demo/README.md) - Web interface for the TTS system
- [API Documentation](docs/api.md) - Detailed API reference
- [Architecture Overview](docs/architecture.md) - System design and components
- [Usage Guide](docs/usage.md) - Detailed usage examples
- [REST API Guide](api/README.md) - FastAPI REST interface for the TTS system

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

## Configuration

Default configuration values (can be overridden via environment variables):

```python
ENGLISH_VOICE_ID = "Emma"      # Default English voice
JAPANESE_VOICE_ID = "Takumi"   # Default Japanese voice
TTS_SERVICE = "aws_polly"      # Default TTS service
AWS_REGION_NAME = "us-east-1"  # Default AWS region
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

For detailed demo instructions and features, see the [Demo Application Guide](demo/README.md).

## REST API

The system provides a RESTful API powered by FastAPI for integration with other services.

### API Features
- Convert text to speech via HTTP requests
- Automatic language detection between English and Japanese 
- Multiple voice and output format options
- Stateless architecture for scalability

### Running the API Server

#### Using Docker Compose (Recommended)

1. Create a `.env` file with your AWS/Google Cloud credentials:

    ```
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    AWS_REGION_NAME=us-east-1
    TTS_SERVICE=aws_polly
    ENGLISH_VOICE_ID=Joanna
    JAPANESE_VOICE_ID=Mizuki
    ```

2. If using Google Cloud TTS, add the credentials file:
   - Set `TTS_SERVICE=google_cloud` in your `.env` file
   - Place your Google credentials JSON at the project root
   - Uncomment the volume mount in `docker-compose.yml`

3. Start the API server:

    ```bash
    docker-compose up -d
    ```

4. Access the API at http://localhost:8001/docs

#### Running Locally

1. Install the dependencies:

    ```bash
    pip install -r api/requirements.txt
    ```

2. Download NLTK data:

    ```bash
    python api/download_nltk_data.py
    ```

3. Run the API server:

    ```bash
    cd api
    uvicorn main:app --host 0.0.0.0 --port 8001
    ```

For detailed API documentation and example requests, see the [REST API Guide](api/README.md).

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
- `sample_texts/`: Example texts in various formats

## Supported Features
- Mixed English-Japanese text processing
- Intelligent sentence segmentation with abbreviation handling
- Multiple TTS service support (AWS Polly, Google Cloud TTS)
- Multiple output formats (WAV, MP3, OGG)
- Natural transitions between language segments

## Troubleshooting

### Common Issues

1. **NLTK Data Missing**
   ```
   LookupError: Resource punkt not found
   ```
   Solution: Run `python download_nltk_data.py` to download required NLTK data.

2. **AWS Credentials Error**
   ```
   botocore.exceptions.NoCredentialsError
   ```
   Solution: Check that AWS credentials are properly set in environment variables.

3. **Google Cloud Authentication Error**
   ```
   google.auth.exceptions.DefaultCredentialsError
   ```
   Solution: Verify the path to your Google Cloud credentials JSON file.

4. **Audio Output Issues**
   - Check that ffmpeg is installed for MP3/OGG support
   - Ensure write permissions in the output directory
   - Verify that the selected voice IDs are available in your AWS/Google Cloud account

For more detailed troubleshooting, refer to the [Demo Application Guide](demo/README.md).
