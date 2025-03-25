"""Exceptions for the speech synthesis module."""

class TTSError(Exception):
    """Base exception for TTS-related errors."""
    pass

class TTSConnectionError(TTSError):
    """Raised when there are connection/authentication issues with the TTS service."""
    pass

class TTSInvalidInputError(TTSError):
    """Raised when the input text or parameters are invalid."""
    pass

class TTSSynthesisError(TTSError):
    """Raised when there's an error during speech synthesis."""
    pass 