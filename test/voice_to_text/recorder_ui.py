'''
Unified voice recorder app using NiceGUI for frontend and Faster-Whisper for backend transcription.
Runs on a single port with no CORS issues and includes waveform animation and robust error handling.

Author: Tebogo Monamodi
'''

from nicegui import ui
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
from faster_whisper import WhisperModel
import tempfile
import uuid
import os

# --- Load Faster-Whisper Model ---
model = WhisperModel("base", compute_type="int8", cpu_threads=4)  # Use "tiny" for faster dev

# --- FastAPI App for Transcription ---
fastapi_app = FastAPI()

@fastapi_app.post("/transcribe")
async def transcribe_audio(audio_data: UploadFile = File(...)):
    tmp_path = None
    try:
        tmp_path = Path.cwd() / f"temp_{uuid.uuid4().hex}.wav"
        content = await audio_data.read()
        with open(tmp_path, "wb") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        segments, info = model.transcribe(str(tmp_path), beam_size=1)
        text = " ".join([segment.text for segment in segments]).strip()
        return {"text": text or "No speech detected."}

    except Exception as e:
        return {"text": f"Error during transcription: {str(e)}"}

    finally:
        if tmp_path and tmp_path.exists():
            try:
                os.remove(tmp_path)
            except Exception:
                pass

# --- NiceGUI Frontend ---
ui.add_head_html('''
<style>
#voice-line {
    width: 100%;
    height: 6px;
    background: linear-gradient(to right, #3b82f6, #1e40af);
    border-radius: 3px;
    margin: 1rem 0;
    transition: height 0.2s ease, background 0.2s ease;
}
</style>

<script>
let mediaRecorder;
let audioChunks = [];
let audioContext, analyser, source, dataArray;

async function startRecording() {
    if (!navigator.mediaDevices) {
        alert("Your browser does not support audio recording.");
        return;
    }

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    const voiceLine = document.getElementById('voice-line');
    audioContext = new AudioContext();
    analyser = audioContext.createAnalyser();
    source = audioContext.createMediaStreamSource(stream);
    source.connect(analyser);
    dataArray = new Uint8Array(analyser.frequencyBinCount);

    function animate() {
        analyser.getByteTimeDomainData(dataArray);
        const max = Math.max(...dataArray);
        const normalized = Math.min(Math.max((max - 128) / 128, 0), 1);
        const newHeight = 6 + normalized * 24;
        voiceLine.style.height = `${newHeight}px`;
        requestAnimationFrame(animate);
    }

    animate();

    mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) {
            audioChunks.push(e.data);
        }
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recording.wav');

        const spinner = document.getElementById('spinner');
        spinner.style.display = 'inline-block';

        try {
            const response = await fetch('/transcribe', {
                method: 'POST',
                body: formData,
            });

            const contentType = response.headers.get('content-type');
            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server error: ${text}`);
            }

            if (contentType && contentType.includes('application/json')) {
                const result = await response.json();
                document.getElementById('output').innerText = result.text;
            } else {
                const text = await response.text();
                throw new Error(`Unexpected response: ${text}`);
            }
        } catch (err) {
            console.error("Fetch failed:", err);
            document.getElementById('output').innerText = 'Error: ' + err.message;
        }

        spinner.style.display = 'none';
        document.getElementById('startBtn').disabled = false;
    };

    mediaRecorder.start();
    document.getElementById('startBtn').disabled = true;
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
}
</script>
''')

# --- UI Layout ---
with ui.row().classes('items-center justify-center w-full h-screen bg-[#0f172a] text-white'):
    with ui.column().classes('p-6 gap-4 w-2/5 items-center'):
        ui.label('🎧 Minimal Voice Recorder').classes('text-2xl text-blue-400 font-bold')
        ui.html('<div id="voice-line"></div>')
        ui.button('🎙️ Start Recording', on_click=lambda: ui.run_javascript('startRecording()')) \
            .props('id="startBtn" outline color="primary"') \
            .classes('w-full')
        ui.button('⏹️ Stop Recording', on_click=lambda: ui.run_javascript('stopRecording()')) \
            .props('outline color="red"') \
            .classes('w-full')
        ui.spinner().classes('text-blue-500').style('display:none;').props('id="spinner"')
        ui.label('').props('id="output"').classes('text-white pt-4')

# --- Run Unified App ---
ui.run_with(fastapi_app)
ui.run(title='Waveform Recorder', dark=True, port=8080, reload=False, show=True)











