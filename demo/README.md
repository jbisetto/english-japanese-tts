# English-Japanese Text-to-Speech Demo Application

This directory contains the Gradio application for demonstrating the English-Japanese Text-to-Speech system. The application provides an intuitive interface for converting mixed English-Japanese text into natural-sounding speech.

For detailed API documentation and architecture overview, see:
- [Main Project Documentation](../README.md)
- [API Reference](../docs/api.md)
- [Architecture Overview](../docs/architecture.md)

## System Requirements

- Python 3.10 or higher
- ffmpeg (for audio format conversion)
- 2GB RAM minimum
- Modern web browser (Chrome, Firefox, Safari)
- Internet connection for TTS service access

## Features

- Automatic language detection and segmentation
- Support for both AWS Polly and Google Cloud TTS services
- Multiple voice options for both English and Japanese, with gender information
- Natural pauses between language transitions
- Multiple output formats (WAV, MP3, OGG)
- Sample text loading functionality
- Real-time service availability status
- Clean application exit with automatic file cleanup

## Setup

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Download NLTK data:**
    ```bash
    python download_nltk_data.py
    ```
    This downloads the required NLTK data for sentence segmentation and text processing.

3. **Set environment variables:**

    The application supports two TTS services. You can configure either or both:

    * **AWS Polly:**
        * `AWS_ACCESS_KEY_ID`
        * `AWS_SECRET_ACCESS_KEY`
        * `AWS_REGION_NAME`
    * **Google Cloud TTS:**
        * `GOOGLE_APPLICATION_CREDENTIALS` (path to your Google Cloud service account key file)

4. **Run the application:**

    ```bash
    python demo/app.py
    ```

## Usage

1. **Text Input:**
    - Enter your text directly in the input box
    - Use the sample text dropdown to load pre-configured examples
    - Mix English and Japanese freely - the system will detect languages automatically

2. **Voice Selection:**
    - Choose your preferred TTS service (AWS Polly or Google Cloud TTS)
    - Select from available English voices
    - Select from available Japanese voices (labeled with gender information)

3. **Audio Settings:**
    - Choose your preferred output format (WAV, MP3, OGG)
    - The system automatically adds natural pauses between language switches

4. **Synthesis:**
    - Click the blue "Synthesize" button to generate speech
    - View the detected language segments in the "Segmented Text" display
    - Listen to the generated audio in the player
    - Download the audio file using the download button

5. **Exiting the Application:**
    - Use the "Exit Application" button at the bottom of the interface
    - The application will clean up temporary files and display a confirmation message
    - The window will attempt to close automatically after cleanup

## Sample Texts

The application includes pre-configured example texts in the `sample_texts` directory:
- Basic greetings in both languages
- Technical documentation examples
- Conversational examples
- Literature excerpts

## File Management

- Temporary audio files are stored in `demo/temp/`
- Files are automatically cleaned up when using the Exit button or closing the application
- Each synthesis generates a new audio file

## Service Status

The application shows the availability status of configured TTS services at the top of the interface:
- "Available" indicates the service is properly configured
- "Not configured" indicates missing credentials

## Browser Compatibility

The application is designed to work on modern browsers (Chrome, Firefox, Safari, Edge).

## Troubleshooting

### Common Issues

1. **Browser Audio Playback**
   - Enable autoplay in your browser settings
   - Check browser audio output device
   - Try a different browser if issues persist

2. **Service Availability**
   - Check your internet connection
   - Verify AWS/Google Cloud service status
   - Ensure credentials are correctly configured

3. **Audio Format Issues**
   - Verify ffmpeg installation
   - Try a different output format
   - Check system audio codecs

4. **Performance Issues**
   - Close other resource-intensive applications
   - Check available disk space
   - Monitor system memory usage

### Error Messages

1. **"No TTS services available"**
   - Check environment variables
   - Verify credential file paths
   - Test service connectivity

2. **"Failed to load sample text"**
   - Check file permissions
   - Verify file encoding (UTF-8 required)
   - Ensure sample text files exist

3. **"Error during synthesis"**
   - Check input text length
   - Verify voice ID availability
   - Monitor service quotas

For additional help, refer to:
- [Main Project Documentation](../README.md)
- [API Documentation](../docs/api.md)
- Service provider documentation:
  - [AWS Polly Documentation](https://docs.aws.amazon.com/polly/)
  - [Google Cloud TTS Documentation](https://cloud.google.com/text-to-speech/docs)
