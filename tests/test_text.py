from src.text.parser import TextParser
from src.text.segmenter import TextSegmenter

def test_text_parser():
    parser = TextParser()
    
    # Test preprocessing of text with extra whitespace and newlines
    input_text = "Hello  World!\n\nThis is   a test."
    expected = "Hello World! This is a test."
    assert parser.preprocess_text(input_text) == expected

def test_text_segmenter():
    segmenter = TextSegmenter()
    
    # Test basic sentence segmentation
    text = "Hello! This is a test. How are you?"
    segments = segmenter.segment_by_sentence(text)
    assert len(segments) == 3
    assert segments[0] == "Hello!"
    assert segments[1] == "This is a test."
    assert segments[2] == "How are you?"
    
    # Test handling of abbreviations (e.g., Mr., Dr.)
    text = "Mr. Smith went to Dr. Jones."
    segments = segmenter.segment_by_sentence(text)
    assert len(segments) == 1
    assert segments[0] == "Mr. Smith went to Dr. Jones."
