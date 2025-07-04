from nicegui import ui

# --- Add JavaScript to the <head> ---
ui.add_head_html('''
<script>
let mediaRecorder;
let audioChunks = [];

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
            audioChunks.push(event.data);
        }
    };

    mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recording.wav');

        const spinner = document.getElementById('spinner');
        spinner.style.display = 'inline-block';

        try {
            const response = await fetch('http://localhost:8000/transcribe', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();
            const transcription = result.text;

            document.getElementById('output').innerText = transcription;
        } catch (error) {
            document.getElementById('output').innerText = 'Error: ' + error;
        }

        spinner.style.display = 'none';
    };

    mediaRecorder.start();
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
}
</script>
''')

# --- Page Layout ---
with ui.row().classes('items-center justify-center w-full h-screen bg-[#0f172a] text-white'):
    with ui.column().classes('p-6 gap-4 w-2/5'):
        ui.label('🎤 Smart Voice Recorder').classes('text-2xl text-blue-400 font-bold')
        
        ui.button('Start Recording', on_click=lambda: ui.run_javascript('startRecording()')) \
            .props('outline color="primary"') \
            .classes('w-full')

        ui.button('Stop Recording', on_click=lambda: ui.run_javascript('stopRecording()')) \
            .props('outline color="red"') \
            .classes('w-full')

        ui.spinner().classes('text-blue-500').style('display:none;').props('id="spinner"')

        ui.label('').props('id="output"').classes('text-base text-white pt-4')

ui.run(title='Smart Voice', dark=True)



