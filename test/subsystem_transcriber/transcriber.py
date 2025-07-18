'''
Name: Audio Transcriber Service

Overview: Takes blob/audio from a the UI and transcribes it into a text using the model from
faster whisper. Benchmarking and robust testing will be performed please note the timing
module imported to benchmark model loading, transcription and total time. This
is one of the components of the interviewer application

Author: Tebogo Monamodi (Not a bot🤖) 

My goal is to write a clean, robust, and fast services that feel like magic.
'''


from faster_whisper import WhisperModel
from fastapi import FastAPI, UploadFile, File, HTTPException
import os
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Load Whisper model once globally ===
model_start_time = time.time()
try:
    model = WhisperModel("base", device="cpu", compute_type="int8")
except Exception as e:
    logger.exception("Failed to load Whisper model.")
    raise RuntimeError("Model could not be loaded.")
model_loading_time = round(time.time() - model_start_time, 2)

# === FastAPI app setup ===
app = FastAPI()

# === Endpoint ===
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    start_time = time.time()
    temp_filename = "temp.wav"

    try:
        # Read audio blob
        data = await file.read()

        # Check if audio is too short or empty
        if not data or len(data) < 1000:
            raise HTTPException(status_code=400, detail="Audio too short or empty. Please try again.")

        # Save temp file
        with open(temp_filename, "wb") as f:
            f.write(data)

        # Transcribe
        try:
            segments, info = model.transcribe(temp_filename)
        except Exception as e:
            logger.exception("Transcription failed.")
            raise HTTPException(status_code=500, detail="Transcription engine crashed.")

        # Remove temp file
        os.remove(temp_filename)

        # Convert segments to text
        text = ''.join([segment.text for segment in segments])
        transcription_time = round(time.time() - start_time, 2)
        total_time = round(time.time() - start_time, 2)

        # Validate transcription quality
        if not text.strip():
            raise HTTPException(status_code=422, detail="Could not understand audio. Try speaking clearly.")

        return {
            "transcribed": text,
            "model_load_time": model_loading_time,
            "transcription_time": transcription_time,
            "total_time": total_time
        }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.exception("Unexpected server error.")
        raise HTTPException(status_code=500, detail="Unexpected error during transcription.")

    finally:
        # Clean up in case of errors
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

