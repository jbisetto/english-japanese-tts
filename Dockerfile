FROM python:3.9-slim

WORKDIR /app

# Install system dependencies including FFmpeg for audio processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader punkt

# Copy the source code
COPY src/ /app/src/
COPY api/ /app/api/

# Create temp directory
RUN mkdir -p /app/api/temp

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/google_credentials.json

# Create a startup script to handle conditional imports
RUN echo '#!/bin/bash\n\
# Check if TTS_SERVICE is set to use Google Cloud\n\
if [ "$TTS_SERVICE" == "google_cloud" ]; then\n\
  # Validate Google credentials exist\n\
  if [ ! -f "$GOOGLE_APPLICATION_CREDENTIALS" ]; then\n\
    echo "Error: Google Cloud credentials not found at $GOOGLE_APPLICATION_CREDENTIALS"\n\
    echo "You must mount your Google credentials when using google_cloud TTS service"\n\
    exit 1\n\
  fi\n\
fi\n\
\n\
# Start the API\n\
exec uvicorn api.main:app --host 0.0.0.0 --port 8001\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run the startup script
CMD ["/app/start.sh"] 