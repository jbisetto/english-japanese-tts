from typing import List, Dict, Optional, Tuple
from src.config import Config
from src.speech.aws_polly_service import AWSPollyService
from src.speech.google_cloud_tts_service import GoogleCloudTTSService
from src.speech.exceptions import TTSError, TTSConnectionError, TTSInvalidInputError, TTSSynthesisError

class SpeechService:
    def __init__(self, config: Config):
        """Initialize the speech service with the specified TTS service.

        Args:
            config: Configuration object containing TTS service settings.

        Raises:
            ValueError: If an invalid TTS service name is provided.
        """
        self.config = config
        self.tts_service_name = config.tts_service
        if self.tts_service_name == "aws_polly":
            self.tts_service = AWSPollyService(config)
        elif self.tts_service_name == "google_cloud":
            self.tts_service = GoogleCloudTTSService(config)
        else:
            raise ValueError(f"Invalid TTS service name: {self.tts_service_name}")
        self.english_voice_id = config.english_voice_id
        self.japanese_voice_id = config.japanese_voice_id

    def synthesize_segment(self, text: str, language: str, voice_id: Optional[str] = None) -> bytes:
        """Synthesize speech for a single text segment.

        Args:
            text: The text to synthesize.
            language: The language of the text.
            voice_id: Optional voice ID to use for synthesis.

        Returns:
            The synthesized audio data as bytes.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with the TTS service.
            TTSInvalidInputError: If the input text or parameters are invalid.
            TTSSynthesisError: If there's an error during speech synthesis.
        """
        try:
            return self.tts_service.synthesize(language, text, voice_id)
        except TTSError as e:
            # Re-raise TTS errors with service name for better error tracking
            raise type(e)(f"{self.tts_service_name}: {str(e)}")

    def synthesize_all_segments(self, segments: List[Dict[str, str]]) -> List[bytes]:
        """Synthesize speech for multiple text segments.

        Args:
            segments: List of dictionaries containing text and language for each segment.

        Returns:
            List of synthesized audio data as bytes.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with the TTS service.
            TTSInvalidInputError: If any input text or parameters are invalid.
            TTSSynthesisError: If there's an error during speech synthesis.
        """
        audio_segments = []
        for segment in segments:
            try:
                audio_data = self.synthesize_segment(
                    text=segment["text"],
                    language=segment["language"],
                    voice_id=segment.get("voice_id")
                )
                audio_segments.append(audio_data)
            except TTSError as e:
                # Add segment information to the error message
                raise type(e)(f"Error in segment '{segment['text'][:50]}...': {str(e)}")
        return audio_segments

    def synthesize_all(self, language_segments: List[Tuple[str, str]]) -> List[bytes]:
        """Convert text to speech using appropriate models/voices.
        
        Args:
            language_segments: List of (language_code, text) tuples
            
        Returns:
            List of audio segments as bytes
        """
        return [self.synthesize_segment(lang, text) for lang, text in language_segments]
