//I am not a JavaScript guy, I prefer python, but this had to be done
//[getUserMedia]->[MediaRecord]->[empty array]->[blob]

const stream = await navigator.mediaDevices.getUserMedia({ audio: true}) //create a pipeline and get permission
const mediaRecorder = new MediaRecorder(stream); //controller for the audio stream
const chunks = [];

const socket = new WebSocket('ws://localhost:transcribe')
mediaRecorder.ondataavailable = function(event) {
  if (event.data.size > 0) {
    socket.send(event.data); //send chunk to the backend
  }
};

mediaRecorder.onstop = function() {
  const blob = new Blob(chunks, { type: 'audio/wav' });
  audio.controls = true;
  document.body.appendChild(audio); // append the audio element to the body
  audio.play(); // play the audio
}