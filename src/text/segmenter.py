from nltk.tokenize import PunktSentenceTokenizer
from typing import List

class TextSegmenter:
    def __init__(self):
        """Initialize the TextSegmenter with NLTK's sentence tokenizer.
        
        Uses a pre-trained Punkt tokenizer that handles:
        - Common abbreviations (Mr., Mrs., Dr., etc.)
        - Common sentence-final punctuation (.!?)
        - Special cases like decimal numbers and ellipses
        """
        # Initialize with common English abbreviations
        self.tokenizer = PunktSentenceTokenizer()
        self.tokenizer._params.abbrev_types.update([
            'mr', 'mrs', 'dr', 'ms', 'prof', 'inc', 'ltd', 'co', 'corp',
            'vs', 'v', 'jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug',
            'sep', 'oct', 'nov', 'dec', 'dept', 'univ', 'assn', 'bros',
            'p.m', 'a.m', 'u.s', 'u.k', 'i.e', 'e.g', 'etc'
        ])
    
    def segment_by_sentence(self, text: str) -> List[str]:
        """Split text into sentences using NLTK's sentence tokenizer.
        
        Args:
            text: The input text to segment.
            
        Returns:
            A list of sentences. For empty input, returns a list with an empty string
            to maintain backward compatibility.
        """
        if not text.strip():
            return [""]
        return self.tokenizer.tokenize(text)
