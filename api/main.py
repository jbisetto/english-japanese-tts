import os
import sys
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uuid
import shutil
from typing import Optional, List

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Try to import TTSAgent, but handle import errors for optional dependencies
try:
    from src.agent import TTSAgent
    has_tts_agent = True
except ImportError as e:
    print(f"Warning: TTSAgent import failed: {e}")
    print("Some TTS services may not be available.")
    has_tts_agent = False

from src.config import Config

# Create FastAPI app
app = FastAPI(
    title="English-Japanese TTS API",
    description="API for multilingual text-to-speech conversion",
    version="1.0.0"
)

# Models for request and response
class TTSRequest(BaseModel):
    text: str
    tts_service: str = "aws_polly"  # Default to AWS Polly
    english_voice_id: str = "Joanna"  # Default English voice
    japanese_voice_id: str = "Mizuki"  # Default Japanese voice
    audio_format: str = "wav"  # Default format

class TTSResponse(BaseModel):
    audio_url: str
    segments: List[str]
    request_id: str

class VoiceInfo(BaseModel):
    id: str
    language: str
    gender: Optional[str] = None
    service: str

class VoicesResponse(BaseModel):
    voices: List[VoiceInfo]

# Setup
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# Available voices
AWS_POLLY_ENGLISH_VOICES = ["Matthew", "Joanna", "Kimberly", "Salli", "Joey"]
AWS_POLLY_JAPANESE_VOICES = ["Takumi", "Mizuki", "Kazuha"]
GOOGLE_CLOUD_ENGLISH_VOICES = ["en-US-Standard-A", "en-US-Standard-B", "en-US-Standard-C"]
GOOGLE_CLOUD_JAPANESE_VOICES = ["ja-JP-Standard-A", "ja-JP-Standard-B", "ja-JP-Standard-C"]

# Helper function to create config
def create_config(tts_service: str, english_voice_id: str, 
                 japanese_voice_id: str) -> Config:
    """Create a Config object based on user selections."""
    config = Config()
    config.tts_service = tts_service
    config.english_voice_id = english_voice_id
    config.japanese_voice_id = japanese_voice_id
    return config

# Helper function to clean up old files
def cleanup_old_files(directory: str, max_age_minutes: int = 5):
    """Remove files older than max_age_minutes from directory."""
    import time
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isdir(file_path):
            try:
                # Check if directory is older than max_age_minutes
                if os.stat(file_path).st_mtime < now - max_age_minutes * 60:
                    shutil.rmtree(file_path, ignore_errors=True)
            except Exception as e:
                print(f"Error deleting directory {file_path}: {e}")

# Routes
@app.get("/")
async def root():
    return {"message": "English-Japanese TTS API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/voices", response_model=VoicesResponse)
async def get_voices():
    """Get available voices for all services"""
    voices = []
    
    # Check if TTS Agent was successfully imported
    if not has_tts_agent:
        return VoicesResponse(voices=[
            VoiceInfo(id="UNAVAILABLE", language="N/A", service="TTS services unavailable - missing dependencies")
        ])
    
    # Check if AWS credentials are available
    aws_available = all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION_NAME")
    ])
    
    # Check if Google Cloud credentials are available
    google_available = os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))
    
    # Add AWS voices if available
    if aws_available:
        for voice in AWS_POLLY_ENGLISH_VOICES:
            voices.append(VoiceInfo(id=voice, language="en-US", service="aws_polly"))
        for voice in AWS_POLLY_JAPANESE_VOICES:
            voices.append(VoiceInfo(id=voice, language="ja-JP", service="aws_polly"))
    
    # Add Google voices if available
    if google_available:
        for voice in GOOGLE_CLOUD_ENGLISH_VOICES:
            # Determine gender from voice ID if possible
            gender = "female" if voice.endswith("A") or voice.endswith("C") else "male"
            voices.append(VoiceInfo(id=voice, language="en-US", gender=gender, service="google_cloud"))
        for voice in GOOGLE_CLOUD_JAPANESE_VOICES:
            gender = "female" if voice.endswith("A") or voice.endswith("C") else "male"
            voices.append(VoiceInfo(id=voice, language="ja-JP", gender=gender, service="google_cloud"))
    
    return VoicesResponse(voices=voices)

@app.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest, background_tasks: BackgroundTasks):
    """
    Synthesize text to speech
    
    - Returns a URL to the generated audio file
    - Segments shows the text broken down by language
    """
    # Check if TTS services are available
    if not has_tts_agent:
        raise HTTPException(
            status_code=503, 
            detail="TTS services are not available. Required dependencies may be missing."
        )
    
    # Generate a unique ID for this request
    request_id = str(uuid.uuid4())
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(TEMP_DIR, request_id)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output path
    output_path = os.path.join(output_dir, f"output.{request.audio_format}")
    
    try:
        # Create config and initialize agent
        config = create_config(
            request.tts_service, 
            request.english_voice_id,
            request.japanese_voice_id
        )
        agent = TTSAgent(config)
        
        # Synthesize audio
        audio_path, segments = agent.synthesize(request.text, output_path)
        
        # Schedule cleanup of old files
        background_tasks.add_task(cleanup_old_files, TEMP_DIR)
        
        # Generate URL for the audio file
        audio_url = f"/audio/{request_id}/output.{request.audio_format}"
        
        return TTSResponse(
            audio_url=audio_url,
            segments=segments,
            request_id=request_id
        )
    except Exception as e:
        # Clean up if there was an error
        shutil.rmtree(output_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{request_id}/{filename}")
async def get_audio(request_id: str, filename: str, background_tasks: BackgroundTasks):
    """Serve the generated audio file and delete it after access"""
    audio_dir = os.path.join(TEMP_DIR, request_id)
    file_path = os.path.join(audio_dir, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    # Schedule deletion of the file after it's served
    background_tasks.add_task(shutil.rmtree, audio_dir, ignore_errors=True)
    
    return FileResponse(
        file_path,
        headers={"Cache-Control": "no-cache, no-store, must-revalidate"}
    )

@app.delete("/audio/{request_id}")
async def delete_audio(request_id: str):
    """Delete audio files for a specific request ID"""
    audio_dir = os.path.join(TEMP_DIR, request_id)
    
    if not os.path.exists(audio_dir):
        raise HTTPException(status_code=404, detail="Audio directory not found")
    
    try:
        shutil.rmtree(audio_dir)
        return {"message": f"Audio files for request {request_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting audio files: {str(e)}")

# Startup event
@app.on_event("startup")
async def startup_event():
    # Clean up any temporary files from previous runs
    cleanup_old_files(TEMP_DIR, max_age_minutes=5)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True) 