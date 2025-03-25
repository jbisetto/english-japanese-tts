# English-Japanese Text-to-Speech Demo Application

This directory contains the Gradio application for demonstrating the English-Japanese Text-to-Speech system. The application provides an intuitive interface for converting mixed English-Japanese text into natural-sounding speech.

## Features

- Automatic language detection and segmentation
- Support for both AWS Polly and Google Cloud TTS services
- Multiple voice options for both English and Japanese, with gender information
- Natural pauses between language transitions
- Multiple output audio formats (WAV, MP3, OGG)
- Sample text loading functionality
- Real-time service availability status
- Clean application exit with automatic file cleanup

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Set environment variables:**

    The application supports two TTS services. You can configure either or both:

    *   **AWS Polly:**
        *   `AWS_ACCESS_KEY_ID`
        *   `AWS_SECRET_ACCESS_KEY`
        *   `AWS_REGION_NAME`
    *   **Google Cloud TTS:**
        *   `GOOGLE_APPLICATION_CREDENTIALS` (path to your Google Cloud service account key file)

3.  **Run the application:**

    ```bash
    python demo/app.py
    ```

## Usage

1.  **Text Input:**
    - Enter your text directly in the input box
    - Use the sample text dropdown to load pre-configured examples
    - Mix English and Japanese freely - the system will detect languages automatically

2.  **Voice Selection:**
    - Choose your preferred TTS service (AWS Polly or Google Cloud TTS)
    - Select from available English voices
    - Select from available Japanese voices (labeled with gender information)

3.  **Audio Settings:**
    - Choose your preferred output format (WAV, MP3, OGG)
    - The system automatically adds natural pauses between language switches

4.  **Synthesis:**
    - Click the blue "Synthesize" button to generate speech
    - View the detected language segments in the "Segmented Text" display
    - Listen to the generated audio in the player
    - Download the audio file using the download button

5.  **Exiting the Application:**
    - Use the "Exit Application" button at the bottom of the interface
    - The application will clean up temporary files and display a confirmation message
    - The window will attempt to close automatically after cleanup

## Sample Texts

The application includes sample texts in the `sample_texts` directory. You can add your own sample texts by placing `.txt` files in this directory. The files should contain mixed English-Japanese text examples.

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
