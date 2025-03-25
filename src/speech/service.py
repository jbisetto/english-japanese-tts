from typing import List, Tuple
from src.config import Config
from src.speech.tts_service import TTSService
from src.speech.aws_polly_service import AWSPollyService
from src.speech.google_cloud_tts_service import GoogleCloudTTSService

class SpeechService:
    def __init__(self, config: Config):
        self.config = config
        tts_service_name = config.tts_service
        if tts_service_name == "aws_polly":
            self.tts_service = AWSPollyService(config)
        elif tts_service_name == "google_cloud":
            self.tts_service = GoogleCloudTTSService()
        else:
            raise ValueError(f"Invalid TTS service: {tts_service_name}")
        self.english_voice_id = config.english_voice_id
        self.japanese_voice_id = config.japanese_voice_id

    def synthesize_segment(self, language: str, text_segment: str) -> bytes:
        """Select appropriate TTS voice based on detected language.
        
        Args:
            language: The language code ('en' or 'ja')
            text_segment: The text to synthesize
            
        Returns:
            The synthesized audio as bytes
        """
        # Select voice based on language
        voice_id = self.english_voice_id if language == "en" else self.japanese_voice_id
        return self.tts_service.synthesize(language, text_segment, voice_id)

    def synthesize_all(self, language_segments: List[Tuple[str, str]]) -> List[bytes]:
        """Convert text to speech using appropriate models/voices.
        
        Args:
            language_segments: List of (language_code, text) tuples
            
        Returns:
            List of audio segments as bytes
        """
        return [self.synthesize_segment(lang, text) for lang, text in language_segments]
