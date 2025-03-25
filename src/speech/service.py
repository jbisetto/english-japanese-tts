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
            self.tts_service = AWSPollyService()
        elif tts_service_name == "google_cloud":
            self.tts_service = GoogleCloudTTSService()
        else:
            raise ValueError(f"Invalid TTS service: {tts_service_name}")
        self.english_voice_id = config.english_voice_id
        self.japanese_voice_id = config.japanese_voice_id

    def synthesize_segment(self, language: str, text_segment: str) -> bytes:
        # Select appropriate TTS voice based on detected language
        # Handle pronunciation of foreign words within each language
        # Support speaking style parameters (speed, pitch, emphasis)
        return self.tts_service.synthesize(language, text_segment)

    def synthesize_all(self, language_segments: List[Tuple[str, str]]) -> List[bytes]:
        # Convert text to speech using appropriate models/voices
        return [self.synthesize_segment(lang, text) for lang, text in language_segments]
