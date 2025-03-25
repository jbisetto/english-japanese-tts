import pytest
from unittest.mock import MagicMock
from src.speech.service import SpeechService
from src.speech.exceptions import TTSConnectionError, TTSInvalidInputError, TTSSynthesisError
from src.config import Config

class MockTTSService:
    def __init__(self, config):
        pass
        
    def synthesize(self, language: str, text: str, voice_id: str = None) -> bytes:
        # Return different bytes for different inputs to simulate synthesis
        return f"{language}:{text}:{voice_id}".encode()

def test_speech_service():
    # Create a config with test settings
    config = Config()
    config.tts_service = "aws_polly"
    config.english_voice_id = "en-voice"
    config.japanese_voice_id = "ja-voice"
    
    # Test service initialization
    service = SpeechService(config)
    assert service.tts_service_name == "aws_polly"
    assert service.english_voice_id == "en-voice"
    assert service.japanese_voice_id == "ja-voice"
    
    # Replace real TTS service with mock
    service.tts_service = MockTTSService(config)
    
    # Test single segment synthesis
    result = service.synthesize_segment("Hello", "en", "test-voice")
    assert result == b"en:Hello:test-voice"
    
    # Test voice selection based on language
    segments = [
        ("en", "Hello"),
        ("en-US", "World"),
        ("ja", "Konnichiwa")  # Using romaji instead of Japanese characters
    ]
    results = service.synthesize_all(segments)
    assert len(results) == 3
    assert results[0] == b"en:Hello:en-voice"  # English voice
    assert results[1] == b"en-US:World:en-voice"  # English voice (en-US)
    assert results[2] == b"ja:Konnichiwa:ja-voice"  # Japanese voice
    
    # Test dictionary-style segments
    dict_segments = [
        {"text": "Hello", "language": "en", "voice_id": "custom-voice"},
        {"text": "World", "language": "en"}
    ]
    results = service.synthesize_all_segments(dict_segments)
    assert len(results) == 2
    assert results[0] == b"en:Hello:custom-voice"  # Custom voice
    assert results[1] == b"en:World:None"  # No voice specified
    
    # Test invalid service name
    with pytest.raises(ValueError) as exc:
        config.tts_service = "invalid"
        SpeechService(config)
    assert "Invalid TTS service name" in str(exc.value)
    
    # Test error propagation
    def mock_synthesize_with_error(*args):
        raise TTSInvalidInputError("Test error")
    
    service.tts_service.synthesize = mock_synthesize_with_error
    with pytest.raises(TTSInvalidInputError) as exc:
        service.synthesize_segment("test", "en")
    assert "aws_polly: Test error" in str(exc.value)
