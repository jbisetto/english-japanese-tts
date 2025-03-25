import wave
from pydub import AudioSegment
import io

class OutputManager:
    def merge_segments(self, audio_segments):
        """Stitch audio segments with natural transitions.
        
        Args:
            audio_segments: List of raw PCM audio data (16kHz, 16-bit, mono)
            
        Returns:
            Merged audio data as bytes with silence between segments
        """
        # Convert each PCM segment to AudioSegment
        segments = []
        for audio_data in audio_segments:
            # Convert PCM to WAV format in memory
            wav_data = io.BytesIO()
            with wave.open(wav_data, "wb") as wf:
                wf.setnchannels(1)  # mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(16000)  # 16kHz
                wf.writeframes(audio_data)
            
            # Create AudioSegment from WAV data
            wav_data.seek(0)
            segment = AudioSegment.from_wav(wav_data)
            segments.append(segment)
        
        # Create a short silence
        silence = AudioSegment.silent(duration=500)  # 500ms silence
        
        # Merge segments with silence between them
        merged = segments[0] if segments else AudioSegment.empty()
        for segment in segments[1:]:
            merged = merged + silence + segment
        
        # Convert back to PCM format
        wav_data = io.BytesIO()
        merged.export(wav_data, format="wav")
        wav_data.seek(0)
        
        # Read the WAV data and extract just the PCM portion
        with wave.open(wav_data, "rb") as wf:
            return wf.readframes(wf.getnframes())

    def export_audio(self, audio_data: bytes, output_path: str, format: str):
        """Export audio data to the specified format.
        
        Args:
            audio_data: Raw PCM audio data (16kHz, 16-bit, mono)
            output_path: Path to save the audio file
            format: Output format (wav, mp3, ogg)
        """
        print(f"Exporting audio to {output_path} in {format} format")
        try:
            # First convert the PCM data to WAV
            wav_data = io.BytesIO()
            with wave.open(wav_data, "wb") as wf:
                wf.setnchannels(1)  # mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(16000)  # 16kHz
                wf.writeframes(audio_data)
            
            # Convert to the desired format using pydub
            wav_data.seek(0)
            audio = AudioSegment.from_wav(wav_data)
            
            format = format.lower()
            if format == "wav":
                audio.export(output_path, format="wav")
            elif format == "mp3":
                audio.export(output_path, format="mp3")
            elif format == "ogg":
                audio.export(output_path, format="ogg")
            else:
                raise ValueError(f"Unsupported format: {format}")
                
        except Exception as e:
            print(f"Error exporting audio: {str(e)}")
            raise
