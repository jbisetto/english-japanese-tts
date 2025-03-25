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

def test_speech_service_initialization():
    # Test with AWS Polly config
    aws_config = Config()
    aws_config.tts_service = "aws_polly"
    aws_config.english_voice_id = "aws-en-voice"
    aws_config.japanese_voice_id = "aws-ja-voice"
    
    service = SpeechService(aws_config)
    assert service.tts_service_name == "aws_polly"
    assert service.english_voice_id == "aws-en-voice"
    assert service.japanese_voice_id == "aws-ja-voice"

def test_speech_service_invalid_service():
    config = Config()
    config.tts_service = "invalid_service"
    
    with pytest.raises(ValueError) as exc:
        SpeechService(config)
    assert "Invalid TTS service name" in str(exc.value)

def test_speech_service_single_segment():
    config = Config()
    config.tts_service = "aws_polly"
    config.english_voice_id = "en-voice-1"
    config.japanese_voice_id = "ja-voice-1"
    
    service = SpeechService(config)
    service.tts_service = MockTTSService(config)
    
    # Test with explicit voice ID
    result = service.synthesize_segment("Hello", "en", "custom-voice")
    assert result == b"en:Hello:custom-voice"
    
    # Test without voice ID (should use None)
    result = service.synthesize_segment("Hello", "en")
    assert result == b"en:Hello:None"

def test_speech_service_language_based_voice_selection():
    config = Config()
    config.tts_service = "aws_polly"
    config.english_voice_id = "en-voice-2"
    config.japanese_voice_id = "ja-voice-2"
    
    service = SpeechService(config)
    service.tts_service = MockTTSService(config)
    
    segments = [
        ("en", "Hello"),
        ("en-US", "World"),
        ("ja", "Konnichiwa")
    ]
    results = service.synthesize_all(segments)
    
    assert len(results) == 3
    assert results[0] == b"en:Hello:en-voice-2"
    assert results[1] == b"en-US:World:en-voice-2"
    assert results[2] == b"ja:Konnichiwa:ja-voice-2"

def test_speech_service_dictionary_segments():
    config = Config()
    config.tts_service = "aws_polly"
    config.english_voice_id = "en-voice-3"
    config.japanese_voice_id = "ja-voice-3"
    
    service = SpeechService(config)
    service.tts_service = MockTTSService(config)
    
    dict_segments = [
        {"text": "Hello", "language": "en", "voice_id": "custom-voice"},
        {"text": "World", "language": "en"}
    ]
    results = service.synthesize_all_segments(dict_segments)
    
    assert len(results) == 2
    assert results[0] == b"en:Hello:custom-voice"
    assert results[1] == b"en:World:None"

def test_speech_service_error_propagation():
    config = Config()
    config.tts_service = "aws_polly"
    
    service = SpeechService(config)
    mock_service = MockTTSService(config)
    service.tts_service = mock_service
    
    def mock_synthesize_with_error(*args):
        raise TTSInvalidInputError("Test error")
    
    mock_service.synthesize = mock_synthesize_with_error
    with pytest.raises(TTSInvalidInputError) as exc:
        service.synthesize_segment("test", "en")
    assert "aws_polly: Test error" in str(exc.value)
