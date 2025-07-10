smart-interviewer-machine
# 🧠 AI Interviewer MVP – README

## 📌 Project Overview
The **AI Interviewer** is a smart, real-time application designed to simulate technical interviews using voice input and provide live feedback based on speaking metrics. The goal is to help job seekers improve their communication under timed pressure and prepare for interviews effectively.

> 🚀 Built with: **FastAPI**, **NiceGUI**, **OpenAI/Whisper**, and **WebSockets**

---

## 🎯 Core Flow Diagram

```
1. [User uploads resume]
     ↓
2. [Backend parses resume (optional GPT API)]
     ↓
3. [5 Interview questions generated]
     ↓
4. [User presses START]
     ↓
5. Timer + voice recorder start simultaneously
     ↓
6. Voice → /transcribe (stream or upload)
     ↓
7. Transcript → metrics service (filler %, WPM, length)
     ↓
8. Metrics → WebSocket → live UI updates
     ↓
9. Timer ends or user clicks STOP → audio closes
     ↓
10. Move to next question (repeat 5x)
     ↓
11. [Final Report]
      ├─ Avg WPM
      ├─ Avg Filler %
      ├─ Response Summary
      └─ Improvement suggestions
```

---

## 🧩 Subsystem Overview

### 1. 🎤 `Audio Recorder` (Frontend)
- Triggers mic input
- Sends audio file to backend

### 2. 📄 `Resume Parser & Question Generator`
- Parses uploaded resume (PDF/docx)
- Uses GPT or rule-based logic to extract 5 relevant interview questions

### 3. 🧠 `Transcription Service`
- Converts recorded audio to clean text using Whisper

### 4. 📊 `Metrics Service`
- Calculates:
  - Words per minute (WPM)
  - Filler word percentage
  - Total word count
  - AI latency (response time)

### 5. 🔁 `WebSocket Stream`
- Sends live metric updates to NiceGUI UI every 1–2 seconds

### 6. 📺 `NiceGUI UI`
- Uploads resume
- Displays interview questions
- Shows timer, live metrics, and final report

### 7. 📦 `Final Report Generator`
- Aggregates per-question metrics
- Summarizes strengths & weaknesses
- Provides improvement suggestions

---

## 📅 Completion Plan: 20-Hour Breakdown to 15 July

| Date | Focus | Goals |
|------|-------|-------|
| **July 10** | ✅ Metrics Service + UI | Finish metrics.py + connect WebSocket UI display |
| **July 11** | 🎙️ Audio Record + Transcribe | Audio input + Whisper transcription connected |
| **July 12** | 🧠 GPT Response | Build `/interview` endpoint and integrate GPT logic |
| **July 13** | 🔁 Multi-question flow | Implement question loop, transitions, timer logic |
| **July 14** | 📊 Final Report | Aggregate metrics, polish UI, generate summary |
| **July 15** | 🚀 Polish + Deploy + Demo | Final testing, deployment, README polish, record video demo |

---

## 🔧 How to Run the App (MVP)

```bash
# 1. Clone the repo
$ git clone https://github.com/yourname/ai-interviewer-app
$ cd ai-interviewer-app

# 2. Create virtual env and install deps
$ python -m venv venv
$ source venv/bin/activate  # or venv\Scripts\activate on Windows
$ pip install -r requirements.txt

# 3. Run the FastAPI backend
$ uvicorn app.main:app --reload

# 4. In a separate terminal, run the NiceGUI UI
$ python ui/interface.py
```

---

## 📚 Future Enhancements
- Speech-to-text accuracy improvements
- Store interaction data in a database
- Resume-based difficulty scaling
- AI-generated personalized feedback per question
- Chart-based metrics over time

---

## 👨‍💻 Author
**Tebogo Monamodi**  
Backend Python Developer | AI Explorer | FastAPI Engineer

---

Stay tuned. This project isn’t just an MVP — it’s your voice, your system, and your signature.

