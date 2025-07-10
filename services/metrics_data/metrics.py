# app/services/metrics_data/metrics.py

FILLERS = {"um", "uh", "like", "you know", "actually", "so"}

def calculate_filler_ratio(transcript: str) -> float:
    words = transcript.lower().split()
    if not words:
        return 0.0
    filler_count = sum(word in FILLERS for word in words)
    return round(filler_count / len(words), 2)

def words_per_minute(transcript: str, duration_seconds: float) -> int:
    words = len(transcript.split())
    return int((words / duration_seconds) * 60) if duration_seconds > 0 else 0

def process_metrics(transcript: str, duration: float, ai_latency: float = 0.0):
    return {
        "filler_ratio": calculate_filler_ratio(transcript),
        "words_per_minute": words_per_minute(transcript, duration),
        "total_words": len(transcript.split()),
        "ai_latency": round(ai_latency, 2)
    }
