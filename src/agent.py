from src.config import Config
from src.text.parser import TextParser
from src.text.segmenter import TextSegmenter
from src.language.detector import LanguageDetector
from src.speech.service import SpeechService
from src.output.manager import OutputManager

class TTSAgent:
    def __init__(self, config: Config):
        self.config = config
        self.text_parser = TextParser()
        self.text_segmenter = TextSegmenter()
        self.language_detector = LanguageDetector(config)
        self.speech_service = SpeechService(config)
        self.output_manager = OutputManager()

    def synthesize(self, text: str, output_path: str):
        processed_text = self.text_parser.preprocess_text(text)
        language_segments = self.language_detector.segment_by_language(processed_text)
        audio_segments = self.speech_service.synthesize_all(language_segments)
        merged_audio = self.output_manager.merge_segments(audio_segments)
        self.output_manager.export_audio(merged_audio, output_path, "wav")
        return output_path, [f"{lang}: {text}" for lang, text in language_segments]
