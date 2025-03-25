## Usage Guide

1.  Install the dependencies:

    ```
    pip install -r requirements.txt
    ```

2.  Set the environment variables:

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

3.  Run the example:

    ```
    python examples/simple_tts.py
