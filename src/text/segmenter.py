import re
from typing import List

class TextSegmenter:
    def segment_by_sentence(self, text: str) -> List[str]:
        sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s", text)
        return sentences
