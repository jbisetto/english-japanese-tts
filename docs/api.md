## API Documentation

### TTSAgent

The `TTSAgent` class provides the main API for the system.

#### `synthesize(text: str, output_path: str, voice_id: str = "Joanna") -> str`

Synthesizes the given text and saves the audio to the specified output path.

-   `text`: The text to synthesize.
-   `output_path`: The path to save the audio file.
-   `voice_id`: (Optional) The voice ID to use for AWS Polly synthesis. Defaults to "Joanna".

Returns the output path of the generated audio file.
