from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import whisper
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = whisper.load_model("base")

@app.post("/transcribe")
async def transcribe_audio(audio_data: UploadFile = File(...)):
    tmp_path = None

    try:
        # Create a guaranteed unique, usable path
        tmp_path = Path.cwd() / f"temp_{uuid.uuid4().hex}.wav"
        content = await audio_data.read()

        # Save & flush file with manual sync to prevent OS caching weirdness
        with open(tmp_path, "wb") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        print(f"[INFO] File saved to: {tmp_path}")
        print(f"[INFO] Exists: {tmp_path.exists()} — Size: {tmp_path.stat().st_size} bytes")

        if not tmp_path.exists():
            raise FileNotFoundError("Audio file vanished before transcription")

        # Transcribe
        result = model.transcribe(str(tmp_path), fp16=False)
        return {"text": result.get("text", "").strip() or "No speech detected."}

    except Exception as e:
        print(f"[ERROR] Transcription failed: {e}")
        return {"text": f"Error during transcription: {str(e)}"}

    finally:
        if tmp_path and tmp_path.exists():
            try:
                os.remove(tmp_path)
                print(f"[INFO] Cleaned up file: {tmp_path}")
            except Exception as e:
                print(f"[WARNING] File cleanup failed: {e}")






