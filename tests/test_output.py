import os
import wave
import tempfile
from src.output.manager import OutputManager

def create_test_pcm(duration_ms=500, freq=440):
    """Create a test PCM audio segment of a sine wave.
    Args:
        duration_ms: Duration in milliseconds
        freq: Frequency in Hz
    Returns:
        PCM audio data as bytes
    """
    import numpy as np
    sample_rate = 16000
    samples = np.sin(2 * np.pi * freq * np.linspace(0, duration_ms/1000, int(sample_rate * duration_ms/1000)))
    samples = (samples * 32767).astype(np.int16).tobytes()
    return samples

def test_output_manager():
    manager = OutputManager()
    
    # Create two test PCM segments
    segment1 = create_test_pcm(500)  # 500ms
    segment2 = create_test_pcm(300)  # 300ms
    
    # Test merging segments
    merged = manager.merge_segments([segment1, segment2])
    assert isinstance(merged, bytes)
    assert len(merged) > len(segment1) + len(segment2)  # Should be longer due to added silence
    
    # Test audio export to different formats
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test WAV export
        wav_path = os.path.join(temp_dir, "test.wav")
        manager.export_audio(merged, wav_path, "wav")
        assert os.path.exists(wav_path)
        with wave.open(wav_path, 'rb') as wf:
            assert wf.getnchannels() == 1  # mono
            assert wf.getsampwidth() == 2  # 16-bit
            assert wf.getframerate() == 16000  # 16kHz
        
        # Test MP3 export
        mp3_path = os.path.join(temp_dir, "test.mp3")
        manager.export_audio(merged, mp3_path, "mp3")
        assert os.path.exists(mp3_path)
        assert os.path.getsize(mp3_path) > 0
        
        # Test OGG export
        ogg_path = os.path.join(temp_dir, "test.ogg")
        manager.export_audio(merged, ogg_path, "ogg")
        assert os.path.exists(ogg_path)
        assert os.path.getsize(ogg_path) > 0
        
        # Test invalid format
        try:
            manager.export_audio(merged, "test.invalid", "invalid")
            assert False, "Should raise ValueError for invalid format"
        except ValueError as e:
            assert "Unsupported format" in str(e)
