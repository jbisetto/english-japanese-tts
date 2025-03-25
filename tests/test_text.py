from src.text.parser import TextParser
from src.text.segmenter import TextSegmenter

def test_parser_whitespace():
    """Test preprocessing of text with extra whitespace."""
    parser = TextParser()
    input_text = "Hello  World    Test"
    expected = "Hello World Test"
    assert parser.preprocess_text(input_text) == expected

def test_parser_newlines():
    """Test preprocessing of text with newlines."""
    parser = TextParser()
    input_text = "Hello\n\nWorld\nTest"
    expected = "Hello World Test"
    assert parser.preprocess_text(input_text) == expected

def test_parser_mixed_whitespace():
    """Test preprocessing of text with mixed whitespace and punctuation."""
    parser = TextParser()
    input_text = "Hello,  World!\n\nThis is   a test."
    expected = "Hello, World! This is a test."
    assert parser.preprocess_text(input_text) == expected

def test_parser_empty_text():
    """Test preprocessing of empty or whitespace-only text."""
    parser = TextParser()
    assert parser.preprocess_text("") == ""
    assert parser.preprocess_text("   ") == ""
    assert parser.preprocess_text("\n\n") == ""

def test_segmenter_basic():
    """Test basic sentence segmentation."""
    segmenter = TextSegmenter()
    text = "Hello! This is a test. How are you?"
    segments = segmenter.segment_by_sentence(text)
    assert len(segments) == 3
    assert segments[0] == "Hello!"
    assert segments[1] == "This is a test."
    assert segments[2] == "How are you?"

def test_segmenter_abbreviations():
    """Test handling of common abbreviations."""
    segmenter = TextSegmenter()
    text = "Mr. Smith went to Dr. Jones. Mrs. Brown arrived at 3 P.M."
    segments = segmenter.segment_by_sentence(text)
    assert len(segments) == 2
    assert segments[0] == "Mr. Smith went to Dr. Jones."
    assert segments[1] == "Mrs. Brown arrived at 3 P.M."

def test_segmenter_single_sentence():
    """Test segmentation of single sentences."""
    segmenter = TextSegmenter()
    text = "This is a single sentence."
    segments = segmenter.segment_by_sentence(text)
    assert len(segments) == 1
    assert segments[0] == "This is a single sentence."

def test_segmenter_empty_text():
    """Test segmentation of empty or whitespace text."""
    segmenter = TextSegmenter()
    segments = segmenter.segment_by_sentence("")
    assert len(segments) == 1
    assert segments[0] == ""
