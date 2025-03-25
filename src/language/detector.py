from typing import List, Tuple
from src.config import Config
from langdetect import detect

class LanguageDetector:
    def __init__(self, config: Config):
        self.config = config

    def detect_language(self, text_segment: str) -> str:
        # Detect the language of the text
        try:
            return detect(text_segment)
        except:
            return "en"

    def segment_by_language(self, text: str) -> List[Tuple[str, str]]:
        # Split text into segments based on detected language
        return [(self.detect_language(text), text)]
