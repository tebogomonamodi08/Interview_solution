'''
Name: Audio Transcriber Service

Overview: Takes blob/audio from a the UI and transcribes it into a text using the model from
faster whisper. Benchmarking and robust testing will be performed please note the timing
module imported to benchmark model loading, transcription and total time. This
is one of the components of the interviewer application

Author: Tebogo Monamodi (Not a bot🤖) 

My goal is to write a clean, robust, and fast services that feel like magic.
'''

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from faster_whisper import WhisperModel
from fastapi import FastAPI, UploadFile, File, HTTPException
import time
import logging
from services.metrics_data.metrics import process_metrics

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === FastAPI App ===
app = FastAPI()

# === Global Latest Metrics ===
latest_metrics = {}

# === Load Whisper Model Once Globally ===
model_start_time = time.time()
try:
    model = WhisperModel("base", device="cpu", compute_type="int8")
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.exception("Failed to load Whisper model.")
    raise RuntimeError("Model could not be loaded.")
model_loading_time = round(time.time() - model_start_time, 2)

# === Transcription Endpoint ===
@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    start_time = time.time()
    temp_filename = "temp_audio.wav"

    try:
        # 1. Read Audio Bytes
        data = await file.read()

        if not data or len(data) < 1000:
            raise HTTPException(status_code=400, detail="Audio too short or empty. Please try again.")

        # 2. Write to Temp File
        with open(temp_filename, "wb") as f:
            f.write(data)

        # 3. Transcribe with Whisper
        try:
            segments, info = model.transcribe(temp_filename)
        except Exception as e:
            logger.exception("Transcription failed.")
            raise HTTPException(status_code=500, detail="Transcription engine crashed.")

        # 4. Extract Text
        transcript = ''.join([segment.text for segment in segments]).strip()
        transcription_time = round(time.time() - start_time, 2)
        total_time = round(time.time() - start_time, 2)

        # 5. Clean Up Temp File
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

        if not transcript:
            raise HTTPException(status_code=422, detail="Could not understand audio. Try speaking clearly.")

        # 6. Process Metrics
        metrics = process_metrics(transcript, transcription_time)
        global latest_metrics
        latest_metrics = metrics

        # 7. Return Result
        return {
            "transcribed": transcript,
            "model_load_time": model_loading_time,
            "transcription_time": transcription_time,
            "total_time": total_time,
            "metrics": metrics
        }

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.exception("Unexpected server error.")
        raise HTTPException(status_code=500, detail="Unexpected error during transcription.")

    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)