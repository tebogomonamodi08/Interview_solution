'''
Name: Audio Transcriber Service
Takes blob/audio from a the UI and transcribes it into a text using the model from
faster whisper. Benchmarking and robust testing will be performed, note the timing
module imported to benchmark model loading, transcription and total time. This
is one of the components of the interviewer application

Author: Tebogo Monamodi (Not a bot🤖) 

```My goal is to write a clean, robust, and fast service that feels like magic.
'''
from faster_whisper import WhisperModel #import WhisperModel from the faster_whisper model
from fastapi import FastAPI, UploadFile, File
import os
import time

model_start_time = time.time() #benchmarking the model start time
model = WhisperModel('base',device='cpu',compute_type='int8') #load the model globally
model_loading_time = round(time.time()-model_start_time, 2) #model loading end
app = FastAPI() #main object

@app.post('/transcibe')
async def transcribe_audio(file: UploadFile = File(...)):
    start_time = time.time() # Transcription time start
    with open('temp.wav','wb') as f:
        data = await file.read() #read blob data
        f.write(data) #write data into the file
    
    segments, info = model.transcribe('temp.wav')
    transcription_time = round(time.time()-start_time,2)
    os.remove('temp.wav')
    text = [segment.text for segment in segments]
    total_time = round(time.time()-start_time,2)
    return {
        'transcribed' : ''.join(text),
        'model_load_time': model_loading_time,
        'transcription_time': transcription_time,
        'total_time': total_time 

    }
