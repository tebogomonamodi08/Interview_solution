'''
This is the backend connected to the NiceGUI backend, it has a endpoint to handle a blob
from the frontend and transcribe it, I will probably set routes when this project becomes
bigger but for now it has one endpoint transcribe

Author: Tebogo Monamodi
'''

#Dependencies
from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import whisper

#main object instance
app = FastAPI()
model = whisper.load_model('base') #Initilize model once globally instead of inside the endpoint handler

#endpoint handler
@app.post('/transcribe')
async def transcribe_audio(audio_data : UploadFile = File(...)):
    
#open a file as 'wb'
    with open('temp_file.wav', 'wb') as file_object:
        data = await audio_data.read() #stop execution until data is read
        file_object.write(data) #write to the temporary file

    transcription = model.transcribe('temp_file.wav') #transribe data and store it in a variable
    Path('temp_file.wav').unlink() #delete temporary file
    #TODO: Review pathlib and learn some of the importent methods.

    return {'text': transcription['text']}

