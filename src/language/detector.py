from typing import List, Tuple
from src.config import Config
from langdetect import detect
import re

class LanguageDetector:
    def __init__(self, config: Config):
        self.config = config

    def detect_language(self, text_segment: str) -> str:
        """Detect the language of a text segment.
        
        Args:
            text_segment: Text to detect language for
            
        Returns:
            Language code ('en' for English, 'ja' for Japanese)
        """
        try:
            # Clean the text segment
            text_segment = text_segment.strip()
            if not text_segment:
                return "en"
                
            # Detect if text contains Japanese characters
            if any(ord(char) > 0x3040 for char in text_segment):
                return "ja"
                
            # For non-Japanese text, use langdetect
            return detect(text_segment)
        except:
            return "en"

    def segment_by_language(self, text: str) -> List[Tuple[str, str]]:
        """Split text into segments based on detected language.
        
        Args:
            text: Input text that may contain multiple languages
            
        Returns:
            List of (language_code, text_segment) tuples
        """
        # Split text into sentences first
        sentences = re.split(r'([。．.!?\n])', text)
        
        # Recombine sentences with their punctuation
        sentences = [''.join(i) for i in zip(sentences[::2], sentences[1::2] + [''])]
        
        # Remove empty sentences and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]
        
        segments = []
        current_lang = None
        current_text = []
        
        for sentence in sentences:
            lang = self.detect_language(sentence)
            
            # If language changes or it's the first segment, start a new segment
            if lang != current_lang and current_text:
                segments.append((current_lang, ' '.join(current_text)))
                current_text = []
            
            current_lang = lang
            current_text.append(sentence)
        
        # Add the last segment
        if current_text:
            segments.append((current_lang, ' '.join(current_text)))
        
        return segments
