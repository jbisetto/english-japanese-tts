from abc import ABC, abstractmethod

class TTSService(ABC):
    @abstractmethod
    def synthesize(self, language: str, text: str) -> bytes:
        """Synthesizes speech from the given text and language.

        Args:
            language: The language of the text.
            text: The text to synthesize.

        Returns:
            The synthesized audio data as bytes.
        """
        pass
