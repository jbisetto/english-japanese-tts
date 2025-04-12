# English-Japanese TTS API

A FastAPI-based REST API for the English-Japanese Text-to-Speech service.

## Features

- Convert text to speech with automatic language detection (English/Japanese)
- Support for AWS Polly and Google Cloud TTS services
- Multiple voice options for each language
- Different audio format output options (WAV, MP3, OGG)

## API Endpoints

### `GET /`

Returns basic information about the API.

### `GET /health`

Health check endpoint.

### `GET /voices`

Returns a list of all available TTS voices for the configured services.

### `POST /synthesize`

Converts text to speech.

**Request Body:**

```json
{
  "text": "Hello, こんにちは",
  "tts_service": "aws_polly",
  "english_voice_id": "Joanna",
  "japanese_voice_id": "Mizuki",
  "audio_format": "wav"
}
```

**Response:**

```json
{
  "audio_url": "/audio/1234-5678-90ab-cdef/output.wav",
  "segments": ["en: Hello", "ja: こんにちは"],
  "request_id": "1234-5678-90ab-cdef"
}
```

### `GET /audio/{request_id}/{filename}`

Serves the generated audio file. Note that files are automatically deleted after being accessed.

### `DELETE /audio/{request_id}`

Deletes all audio files associated with the specified request ID.

**Response:**

```json
{
  "message": "Audio files for request 1234-5678-90ab-cdef deleted successfully"
}
```

## File Retention Policy

- Audio files are automatically deleted after being accessed through the `/audio` endpoint
- Any files not accessed are automatically cleaned up after 5 minutes
- If needed, files can be explicitly deleted using the DELETE endpoint

## Running with Docker Compose

1. Create an `.env` file with your AWS/Google Cloud credentials:

```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION_NAME=us-east-1
TTS_SERVICE=aws_polly
ENGLISH_VOICE_ID=Joanna
JAPANESE_VOICE_ID=Mizuki
```

2. If using Google Cloud TTS:
   - Set `TTS_SERVICE=google_cloud` in your `.env` file
   - Place your Google credentials JSON file in the project root as `google_credentials.json`
   - Uncomment the volume mount line in `docker-compose.yml`

3. Run the service:

```bash
docker-compose up -d
```

4. Access the API at http://localhost:8001

## Development

To run the API locally:

1. Install dependencies:

```bash
pip install -r api/requirements.txt
```

2. Download NLTK data:

```bash
python api/download_nltk_data.py
```

3. Run the API:

```bash
cd api
uvicorn main:app --reload
```

4. Access the API documentation at http://localhost:8001/docs 