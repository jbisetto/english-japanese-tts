from src.language.detector import LanguageDetector
from src.config import Config

def test_language_detector():
    # Create a minimal config for testing
    config = Config()
    detector = LanguageDetector(config)
    
    # Test non-Japanese text returns "en"
    assert detector.detect_language("Hello, this is a test.") == "en"
    assert detector.detect_language("Bonjour!") == "en"  # Even French text returns "en"
    
    # Test Japanese detection (using hiragana)
    assert detector.detect_language("こんにちは") == "ja"
    
    # Test Japanese detection (using kanji)
    assert detector.detect_language("私は日本語を話します") == "ja"
    
    # Test empty text defaults to English
    assert detector.detect_language("") == "en"
    assert detector.detect_language("   ") == "en"
    
    # Test language segmentation with mixed text
    mixed_text = "Hello! こんにちは。This is a test. 私は日本語を話します。"
    segments = detector.segment_by_language(mixed_text)
    
    # Should have 4 segments alternating between en and ja
    assert len(segments) == 4
    assert segments[0] == ("en", "Hello!")
    assert segments[1] == ("ja", "こんにちは。")
    assert segments[2] == ("en", "This is a test.")
    assert segments[3] == ("ja", "私は日本語を話します。")
    
    # Test single language text
    english_text = "Hello! This is a test."
    english_segments = detector.segment_by_language(english_text)
    assert len(english_segments) == 1
    assert english_segments[0] == ("en", "Hello! This is a test.")
