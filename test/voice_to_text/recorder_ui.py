from nicegui import ui

# Inject visual styles & waveform logic
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

button:hover {
    background-color: #1d4ed8 !important;
    color: #fff !important;
}

button:active {
    background-color: #1e3a8a !important;
    transform: scale(0.97);
}
</style>

<script>
let mediaRecorder;
let audioChunks = [];
let audioContext, analyser, source, dataArray;

async function startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    // Setup waveform animation
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
        const newHeight = 6 + normalized * 24;  // pulse height: 6px to ~30px
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
        const audioBlob = new Blob(audioChunks);
        const formData = new FormData();
        formData.append('audio_data', audioBlob, 'recording.wav');

        const spinner = document.getElementById('spinner');
        spinner.style.display = 'inline-block';

        try {
            const response = await fetch('http://localhost:8080/transcribe', {
                method: 'POST',
                body: formData,
            });
            const result = await response.json();
            document.getElementById('output').innerText = result.text;
        } catch (err) {
            document.getElementById('output').innerText = 'Error: ' + err;
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

# Layout using NiceGUI
with ui.row().classes('items-center justify-center w-full h-screen bg-[#0f172a] text-white'):
    with ui.column().classes('p-6 gap-4 w-2/5 items-center'):
        ui.label('🎧 Minimal Voice Recorder').classes('text-2xl text-blue-400 font-bold')
        ui.html('<div id="voice-line"></div>')
        ui.button('🎙️ Start Recording', on_click=lambda: ui.run_javascript('startRecording()')) \
            .props('id="startBtn" outline color="primary"') \
            .classes('w-full transition duration-150 ease-in-out')
        ui.button('⏹️ Stop Recording', on_click=lambda: ui.run_javascript('stopRecording()')) \
            .props('outline color="red"') \
            .classes('w-full transition duration-150 ease-in-out')
        ui.spinner().classes('text-blue-500').style('display:none;').props('id="spinner"')
        ui.label('').props('id="output"').classes('text-white pt-4')

ui.run(title='Waveform Recorder', dark=True, port=8000, reload=True)









