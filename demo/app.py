import os
import sys
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from dotenv import load_dotenv
load_dotenv()

from gradio_adapter import GradioAdapter

# Define available voice IDs
AWS_POLLY_ENGLISH_VOICES = ["Matthew", "Joanna", "Kimberly", "Salli", "Joey"]
AWS_POLLY_JAPANESE_VOICES = ["Takumi (Male)", "Mizuki (Female)", "Kazuha (Female)"]
GOOGLE_CLOUD_ENGLISH_VOICES = ["en-US-Standard-A", "en-US-Standard-B", "en-US-Standard-C"]
GOOGLE_CLOUD_JAPANESE_VOICES = ["ja-JP-Standard-A (Female)", "ja-JP-Standard-B (Male)", "ja-JP-Standard-C (Female)"]

# Default voice IDs
DEFAULT_ENGLISH_VOICE = "Joanna"
DEFAULT_JAPANESE_VOICE = "Mizuki (Female)"

# Audio formats
AUDIO_FORMATS = ["wav", "mp3", "ogg"]
DEFAULT_AUDIO_FORMAT = "wav"

# Directory setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_TEXTS_DIR = os.path.join(SCRIPT_DIR, "sample_texts")
TEMP_AUDIO_DIR = os.path.join(SCRIPT_DIR, "temp")

# Create directories if they don't exist
os.makedirs(SAMPLE_TEXTS_DIR, exist_ok=True)
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)

# Initialize the adapter
adapter = GradioAdapter(TEMP_AUDIO_DIR)

# Map display names to actual voice IDs
def get_voice_id(display_name: str) -> str:
    """Convert display name with gender to actual voice ID."""
    voice_map = {
        "Takumi (Male)": "Takumi",
        "Mizuki (Female)": "Mizuki",
        "Kazuha (Female)": "Kazuha",
        "ja-JP-Standard-A (Female)": "ja-JP-Standard-A",
        "ja-JP-Standard-B (Male)": "ja-JP-Standard-B",
        "ja-JP-Standard-C (Female)": "ja-JP-Standard-C"
    }
    return voice_map.get(display_name, display_name)

def synthesize_adapter(text, tts_service, english_voice_display, japanese_voice_display, audio_format):
    """Adapter function to handle voice display names."""
    english_voice = get_voice_id(english_voice_display)
    japanese_voice = get_voice_id(japanese_voice_display)
    return adapter.synthesize(text, tts_service, english_voice, japanese_voice, audio_format)

def get_available_services():
    """Check which TTS services are available based on credentials."""
    services = []
    aws_creds = all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION_NAME")
    ])
    google_creds = os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))
    
    if aws_creds:
        services.append("aws_polly")
    if google_creds:
        services.append("google_cloud")
    
    return services

def get_credential_status():
    """Get a user-friendly status of available services."""
    aws_creds = all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION_NAME")
    ])
    google_creds = os.path.exists(os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))
    
    status = []
    status.append(f"AWS Polly: {'Available' if aws_creds else 'Not configured'}")
    status.append(f"Google Cloud TTS: {'Available' if google_creds else 'Not configured'}")
    
    return " | ".join(status)

def load_sample_text(sample_text_file):
    """Load sample text from file."""
    file_path = os.path.join(SAMPLE_TEXTS_DIR, sample_text_file)
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error loading sample text: {str(e)}"

def update_voice_ids(tts_service):
    """Update voice ID dropdowns based on TTS service selection."""
    available_services = get_available_services()
    
    if tts_service not in available_services:
        # Service not available, show error and revert to available service
        error_msg = f"{tts_service} is not configured. Please check your credentials."
        if available_services:
            tts_service = available_services[0]
            if tts_service == "aws_polly":
                return (
                    gr.Dropdown.update(choices=AWS_POLLY_ENGLISH_VOICES, value=DEFAULT_ENGLISH_VOICE),
                    gr.Dropdown.update(choices=AWS_POLLY_JAPANESE_VOICES, value=DEFAULT_JAPANESE_VOICE),
                    gr.Radio.update(value=tts_service),
                    error_msg
                )
            else:
                return (
                    gr.Dropdown.update(choices=GOOGLE_CLOUD_ENGLISH_VOICES, value=GOOGLE_CLOUD_ENGLISH_VOICES[0]),
                    gr.Dropdown.update(choices=GOOGLE_CLOUD_JAPANESE_VOICES, value=GOOGLE_CLOUD_JAPANESE_VOICES[0]),
                    gr.Radio.update(value=tts_service),
                    error_msg
                )
        else:
            return (
                gr.Dropdown.update(choices=[], value=None),
                gr.Dropdown.update(choices=[], value=None),
                gr.Radio.update(value=None),
                "No TTS services are configured. Please check your credentials."
            )
    
    if tts_service == "aws_polly":
        return (
            gr.Dropdown.update(choices=AWS_POLLY_ENGLISH_VOICES, value=DEFAULT_ENGLISH_VOICE),
            gr.Dropdown.update(choices=AWS_POLLY_JAPANESE_VOICES, value=DEFAULT_JAPANESE_VOICE),
            gr.Radio.update(value=tts_service),
            None
        )
    else:
        return (
            gr.Dropdown.update(choices=GOOGLE_CLOUD_ENGLISH_VOICES, value=GOOGLE_CLOUD_ENGLISH_VOICES[0]),
            gr.Dropdown.update(choices=GOOGLE_CLOUD_JAPANESE_VOICES, value=GOOGLE_CLOUD_JAPANESE_VOICES[0]),
            gr.Radio.update(value=tts_service),
            None
        )

# Create Gradio interface
with gr.Blocks() as iface:
    gr.Markdown("# English-Japanese Text-to-Speech Demo")
    
    # Add credential status
    credential_status = gr.Markdown(get_credential_status())
    error_output = gr.Markdown()

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(label="Enter Text", lines=5)
            
            with gr.Row():
                submit_button = gr.Button("Synthesize", variant="primary", scale=2)
            
            # Only show sample text dropdown if samples exist
            sample_files = [f for f in os.listdir(SAMPLE_TEXTS_DIR) if f.endswith(".txt")] if os.path.exists(SAMPLE_TEXTS_DIR) else []
            if sample_files:
                sample_text_dropdown = gr.Dropdown(
                    choices=sample_files,
                    label="Sample Text",
                )
                load_sample_button = gr.Button("Load Sample")

            with gr.Row():
                # Only show available services
                available_services = get_available_services()
                default_service = available_services[0] if available_services else None
                
                tts_service = gr.Radio(
                    choices=available_services,
                    value=default_service,
                    label="TTS Service",
                )

                english_voice_id = gr.Dropdown(
                    choices=AWS_POLLY_ENGLISH_VOICES if default_service == "aws_polly" else GOOGLE_CLOUD_ENGLISH_VOICES,
                    value=DEFAULT_ENGLISH_VOICE if default_service == "aws_polly" else GOOGLE_CLOUD_ENGLISH_VOICES[0],
                    label="English Voice",
                )

                japanese_voice_id = gr.Dropdown(
                    choices=AWS_POLLY_JAPANESE_VOICES if default_service == "aws_polly" else GOOGLE_CLOUD_JAPANESE_VOICES,
                    value=DEFAULT_JAPANESE_VOICE if default_service == "aws_polly" else GOOGLE_CLOUD_JAPANESE_VOICES[0],
                    label="Japanese Voice",
                )

            with gr.Row():
                audio_format = gr.Radio(
                    choices=AUDIO_FORMATS,
                    value=DEFAULT_AUDIO_FORMAT,
                    label="Audio Format",
                )

        with gr.Column():
            audio_output = gr.Audio(label="Audio Output")
            segmented_text = gr.Textbox(label="Segmented Text", lines=3)
            debug_output = gr.Textbox(label="Debug/Error Output", lines=3)

    # Add close button and status message at the bottom
    with gr.Row():
        cleanup_status = gr.Markdown("")
    with gr.Row():
        close_button = gr.Button("Exit Application", variant="stop")

    # Event handlers
    if sample_files:
        load_sample_button.click(
            load_sample_text,
            inputs=sample_text_dropdown,
            outputs=text_input
        )
    
    submit_button.click(
        synthesize_adapter,
        inputs=[text_input, tts_service, english_voice_id, japanese_voice_id, audio_format],
        outputs=[audio_output, segmented_text, debug_output],
    )

    # Update voice IDs when TTS service changes
    tts_service.change(
        update_voice_ids,
        inputs=[tts_service],
        outputs=[english_voice_id, japanese_voice_id, tts_service, error_output],
    )

    def cleanup_and_close():
        """Clean up temp files and close the application."""
        adapter.cleanup()
        # Return a message and use JavaScript to close after a delay
        return """
            <script>
            setTimeout(() => window.close(), 1500);
            </script>
            Cleaning up and closing... You can close this window.
            """

    # Handle close button click
    close_button.click(
        cleanup_and_close,
        inputs=[],
        outputs=cleanup_status,
    )

    # Cleanup on shutdown
    iface.close(adapter.cleanup)

# Launch the interface
iface.launch()
