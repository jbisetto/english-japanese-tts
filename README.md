# English-Japanese Text-to-Speech System with Amazon Bedrock

This project implements a text-to-speech system that converts text containing both English and Japanese into natural-sounding speech using Amazon Bedrock.

## Overview

This system processes text input, detects language boundaries between English and Japanese sections, and generates speech appropriately based on the detected language. It ensures proper pronunciation and natural prosody for each language and merges speech segments into a coherent audio output.

## Usage

1.  Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

2.  Set the environment variables:

    ```
    BEDROCK_REGION=your_bedrock_region
    ENGLISH_VOICE_ID=your_english_voice_id
    JAPANESE_VOICE_ID=your_japanese_voice_id
    LANGUAGE_DETECTION_MODEL_ID=your_language_detection_model_id
    ```

    You also need to grant your AWS user account the `AmazonBedrockReadOnly` and `AmazonBedrockInvocation` permissions.

3.  Run the example:

    ```
    python examples/simple_tts.py
    ```

    Note: You may need to add the current directory to the PYTHONPATH environment variable to run the example:

    ```
    PYTHONPATH=. python examples/simple_tts.py
    ```

The `export_audio` method in the `OutputManager` class has a placeholder comment for audio export implementation.
