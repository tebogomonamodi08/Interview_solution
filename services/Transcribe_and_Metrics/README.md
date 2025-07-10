# 🎙️ Subsystem: Audio Transcriber (by Tebogo Monamodi)

> _“Passion, consistency, persistence, and Jesus Christ.”_

---

## 🎯 Purpose

This FastAPI subsystem takes audio (voice recordings) and transcribes it to **text** using the **Faster-Whisper** model. It is one of the core services in the **Interviewer App**, enabling voice-based input for intelligent feedback.

---

## 🧠 Reflections

Initially, I used OpenAI’s Whisper, but transcription was **very slow** — a 5-second clip took 20+ seconds on CPU, which was unacceptable for a real-time experience.

After research and benchmarking, I replaced it with **Faster-Whisper**, a CPU-optimized ASR solution. This README documents the journey, decisions, and future improvements.

---

## 🔍 Tech Stack

| Tool/Library      | Purpose                                |
|------------------ |----------------------------------------|
| FastAPI           | Async Python web framework             |
| Faster-Whisper    | Optimized ASR model                    |
| Python AsyncIO    | Non-blocking file I/O                  |
| UploadFile + File | Efficient blob upload & processing     |

---

## 🧠 System Flow

```mermaid
sequenceDiagram
    User->>UI: Records voice
    UI->>FastAPI: Uploads audio blob (MP3/WAV)
    FastAPI->>FasterWhisper: Transcribe audio
    FasterWhisper-->>FastAPI: Returns segments and metadata
    FastAPI-->>UI: Returns cleaned transcript

## 📈 Benchmarks

Base Model(faster whispher)(Accuracy fair)
|Time(s)| Model Load Time(s)| Transcription time(s)|Total Time(s)|
|10     | 9.22              |  5.16                |  8.66       |
|30     | 9.22              |  3.13                |  8.36       |
|60     | 9.22              |  3.2                 |  17.73      |

##Conlusion

-Sweet spot is 30–45 seconds per audio clip.
-Transcription happens in the background while users engage with other interview questions — improving perceived performance.
-If the user cancels mid-recording, future logic should clean up or discard partial audio already concatenated.