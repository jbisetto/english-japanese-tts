from src.language.detector import LanguageDetector
from src.config import Config

def test_detect_english():
    config = Config()
    detector = LanguageDetector(config)
    
    # Basic English detection
    assert detector.detect_language("Hello, this is a test.") == "en"
    
    # Non-Japanese text should return "en"
    assert detector.detect_language("Bonjour!") == "en"
    assert detector.detect_language("Hola mundo!") == "en"

def test_detect_japanese():
    config = Config()
    detector = LanguageDetector(config)
    
    # Test hiragana
    assert detector.detect_language("こんにちは") == "ja"
    assert detector.detect_language("ありがとう") == "ja"
    
    # Test kanji
    assert detector.detect_language("私は日本語を話します") == "ja"
    assert detector.detect_language("漢字") == "ja"
    
    # Test mixed scripts
    assert detector.detect_language("私のなまえは") == "ja"

def test_detect_empty_text():
    config = Config()
    detector = LanguageDetector(config)
    
    assert detector.detect_language("") == "en"
    assert detector.detect_language("   ") == "en"
    assert detector.detect_language("\n\t") == "en"

def test_segment_mixed_language():
    config = Config()
    detector = LanguageDetector(config)
    
    mixed_text = "Hello! こんにちは。This is a test. 私は日本語を話します。"
    segments = detector.segment_by_language(mixed_text)
    
    assert len(segments) == 4
    assert segments[0] == ("en", "Hello!")
    assert segments[1] == ("ja", "こんにちは。")
    assert segments[2] == ("en", "This is a test.")
    assert segments[3] == ("ja", "私は日本語を話します。")

def test_segment_single_language():
    config = Config()
    detector = LanguageDetector(config)
    
    # Test English-only text
    english_text = "Hello! This is a test."
    english_segments = detector.segment_by_language(english_text)
    assert len(english_segments) == 1
    assert english_segments[0] == ("en", "Hello! This is a test.")
    
    # Test Japanese-only text
    japanese_text = "こんにちは。私は日本語を話します。"
    japanese_segments = detector.segment_by_language(japanese_text)
    assert len(japanese_segments) == 1
    assert japanese_segments[0] == ("ja", "こんにちは。 私は日本語を話します。")

def test_segment_empty_text():
    config = Config()
    detector = LanguageDetector(config)
    
    empty_segments = detector.segment_by_language("")
    assert len(empty_segments) == 0
    
    whitespace_segments = detector.segment_by_language("   \n\t   ")
    assert len(whitespace_segments) == 0
