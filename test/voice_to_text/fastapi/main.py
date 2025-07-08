'''
This is the optimized backend using Faster-Whisper for high-speed transcription.
It handles audio uploads, transcribes them using a quantized model, and returns the result.

Author: Tebogo Monamodi
'''

# Dependencies
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from faster_whisper import WhisperModel
import tempfile
import uuid
import os

# --- FastAPI App Setup ---
app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load Faster-Whisper Model ---
# Use 'int8' for max speed on CPU; use 'float32' for better accuracy
model = WhisperModel("base", compute_type="int8", cpu_threads=4)  # Adjust threads as needed

# --- Transcription Endpoint ---
@app.post("/transcribe")
async def transcribe_audio(audio_data: UploadFile = File(...)):
    tmp_path = None

    try:
        # Create a unique temporary file path
        tmp_path = Path.cwd() / f"temp_{uuid.uuid4().hex}.wav"
        content = await audio_data.read()

        # Save uploaded audio to disk
        with open(tmp_path, "wb") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        print(f"[INFO] File saved to: {tmp_path}")
        print(f"[INFO] Exists: {tmp_path.exists()} — Size: {tmp_path.stat().st_size} bytes")

        if not tmp_path.exists():
            raise FileNotFoundError("Audio file vanished before transcription")

        # Transcribe using Faster-Whisper
        segments, info = model.transcribe(str(tmp_path), beam_size=1)  # beam_size=1 for speed
        text = " ".join([segment.text for segment in segments]).strip()

        return {"text": text or "No speech detected."}

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return {"text": f"Error during transcription: {str(e)}"}

    finally:
        # Clean up temporary file
        if tmp_path and tmp_path.exists():
            try:
                os.remove(tmp_path)
                print(f"[INFO] Cleaned up file: {tmp_path}")
            except Exception as e:
                print(f"[WARNING] File cleanup failed: {e}")







