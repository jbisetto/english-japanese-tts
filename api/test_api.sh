#!/bin/bash

echo "Testing health endpoint..."
curl -s -X GET "http://localhost:8001/health"
echo -e "\n\n"

echo "Getting available voices..."
curl -s -X GET "http://localhost:8001/voices" | json_pp
echo -e "\n\n"

echo "Synthesizing text to speech..."
RESPONSE=$(curl -s -X POST "http://localhost:8001/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, こんにちは. This is a test of English and Japanese mixed text.",
    "tts_service": "aws_polly",
    "english_voice_id": "Joanna",
    "japanese_voice_id": "Mizuki",
    "audio_format": "wav"
  }')

echo $RESPONSE | json_pp
echo -e "\n\n"

# Extract request_id from response
REQUEST_ID=$(echo $RESPONSE | grep -o '"request_id":"[^"]*' | sed 's/"request_id":"//')

if [ -z "$REQUEST_ID" ]; then
    echo "No request ID found in response. Exiting."
    exit 1
fi

echo "Downloading audio file for request $REQUEST_ID..."
curl -s -X GET "http://localhost:8001/audio/$REQUEST_ID/output.wav" --output test_output.wav
echo "Audio saved to test_output.wav"
echo -e "\n\n"

echo "Deleting audio files..."
curl -s -X DELETE "http://localhost:8001/audio/$REQUEST_ID" | json_pp
echo -e "\n\n"

echo "Test completed successfully!" 