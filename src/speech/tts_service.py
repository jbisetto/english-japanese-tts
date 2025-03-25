from abc import ABC, abstractmethod
from .exceptions import TTSError, TTSConnectionError, TTSInvalidInputError, TTSSynthesisError

class TTSService(ABC):
    @abstractmethod
    def synthesize(self, language: str, text: str) -> bytes:
        """Synthesizes speech from the given text and language.

        Args:
            language: The language of the text.
            text: The text to synthesize.

        Returns:
            The synthesized audio data as bytes.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with the service.
            TTSInvalidInputError: If the input text or parameters are invalid.
            TTSSynthesisError: If there's an error during speech synthesis.
            TTSError: For other TTS-related errors.
        """
        pass
