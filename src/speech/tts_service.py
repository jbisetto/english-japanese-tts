from abc import ABC, abstractmethod
from typing import Optional
from .exceptions import TTSError, TTSConnectionError, TTSInvalidInputError, TTSSynthesisError

class TTSService(ABC):
    """Abstract base class for Text-to-Speech services.
    
    This class defines the interface that all TTS service implementations must follow.
    Implementations must handle authentication, voice selection, and audio synthesis
    according to the specifications defined in this interface.

    Audio Format Specifications:
    - Sample Rate: 16kHz
    - Bit Depth: 16-bit
    - Channels: Mono
    - Format: PCM (raw audio data)

    Language Code Format:
    - For English: 'en' or specific variants like 'en-US'
    - For Japanese: 'ja' or specific variants like 'ja-JP'
    """

    @abstractmethod
    def __init__(self, config) -> None:
        """Initialize the TTS service with configuration.

        Args:
            config: Configuration object containing service-specific settings
                   (credentials, region, etc.)

        Raises:
            TTSConnectionError: If unable to initialize the service (e.g., invalid credentials)
            TTSError: For other initialization errors
        """
        pass

    @abstractmethod
    def synthesize(self, language: str, text: str, voice_id: Optional[str] = None) -> bytes:
        """Synthesizes speech from the given text and language.

        Args:
            language: The language code for the text ('en', 'ja', or service-specific variants).
            text: The text to synthesize. Must not be empty.
            voice_id: Optional voice identifier. If not provided, a default voice for the
                     specified language should be used.

        Returns:
            The synthesized audio data as bytes in 16kHz, 16-bit, mono PCM format.

        Raises:
            TTSConnectionError: If there are connection/authentication issues with the service.
                               Implementations should catch service-specific connection errors
                               and wrap them in this exception.
            
            TTSInvalidInputError: If the input is invalid, including:
                                 - Empty or whitespace-only text
                                 - Unsupported language code
                                 - Invalid voice_id
                                 - Text too long for service limits
            
            TTSSynthesisError: If there's an error during speech synthesis, including:
                              - Service-specific synthesis errors
                              - Audio format conversion errors
                              - Resource allocation failures
            
            TTSError: For other TTS-related errors not covered by the above.

        Implementation Requirements:
        1. Must validate input text is not empty or whitespace
        2. Must handle service-specific errors and wrap them in appropriate TTSError types
        3. Must return audio in the specified format (16kHz, 16-bit, mono PCM)
        4. Should use a sensible default voice if voice_id is None
        5. Should handle service-specific language code variants appropriately
        """
        pass
