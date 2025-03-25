## API Documentation

### TTSAgent

The `TTSAgent` class provides the main API for the system.

#### `synthesize(text: str, output_path: str) -> Tuple[str, List[str]]`

Synthesizes the given text and saves the audio to the specified output path.

Parameters:
- `text`: The text to synthesize
- `output_path`: The path to save the audio file

Returns:
- A tuple containing:
  - The output path of the generated audio file
  - A list of language-segmented text showing which parts were synthesized in each language

Raises:
- `TTSConnectionError`: When connection to TTS service fails
- `TTSInvalidInputError`: When input text or parameters are invalid
- `TTSSynthesisError`: When speech synthesis fails
- `TTSError`: For other TTS-related errors

### TextSegmenter

The `TextSegmenter` class handles text segmentation and preprocessing.

#### `segment_by_sentence(text: str) -> List[str]`

Segments text into sentences using NLTK's PunktSentenceTokenizer.

Parameters:
- `text`: The input text to segment

Returns:
- A list of sentences

Features:
- Handles common abbreviations (Mr., Dr., Mrs., P.M., A.M., etc.)
- Preserves whitespace and formatting
- Maintains sentence boundaries

#### `detect_language(text: str) -> str`

Detects the language of a text segment.

Parameters:
- `text`: The text to analyze

Returns:
- Language code ('en' for English, 'ja' for Japanese)

### GradioAdapter

The `GradioAdapter` class provides a convenient interface between the Gradio UI and the TTS system.

#### `synthesize(text: str, tts_service: str, english_voice_id: str, japanese_voice_id: str, audio_format: str) -> Tuple[str, str, Optional[str]]`

Synthesizes the given text using the specified service and voices.

Parameters:
- `text`: The text to synthesize
- `tts_service`: The TTS service to use ("aws_polly" or "google_cloud")
- `english_voice_id`: The voice ID to use for English text
- `japanese_voice_id`: The voice ID to use for Japanese text
- `audio_format`: The desired output format ("wav", "mp3", or "ogg")

Returns:
- A tuple containing:
  - The path to the generated audio file
  - The segmented text showing language detection results
  - Any error message (None if successful)

Raises:
- `TTSConnectionError`: When connection to TTS service fails
- `TTSInvalidInputError`: When input parameters are invalid
- `TTSSynthesisError`: When speech synthesis fails

#### `cleanup() -> None`

Cleans up temporary audio files created during synthesis.

- Called automatically when using the Exit button or closing the application
- Removes all files in the temporary directory specified during initialization
- Returns None

### Exceptions

#### `TTSError`
Base exception class for all TTS-related errors.

#### `TTSConnectionError`
Raised when connection to TTS service fails.
- Network connectivity issues
- Authentication failures
- Service unavailability

#### `TTSInvalidInputError`
Raised when input text or parameters are invalid.
- Empty text
- Unsupported language
- Invalid voice ID
- Unsupported output format

#### `TTSSynthesisError`
Raised when speech synthesis fails.
- Service-specific synthesis errors
- Resource limitations
- Invalid SSML
