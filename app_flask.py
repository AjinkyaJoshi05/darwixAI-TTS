from flask import Flask, request, render_template
import asyncio
import edge_tts
import re
import subprocess
from transformers import pipeline

app = Flask(__name__)

#  Load Hugging Face model once
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

#  Keyword override (fast + accurate for strong emotions)
def keyword_based_detection(text):
    text_lower = text.lower()

    if any(w in text_lower for w in ["angry", "frustrated", "annoyed", "furious", "irritated"]):
        return "angry"

    if any(w in text_lower for w in ["excited", "thrilled", "amazing", "incredible", "awesome"]):
        return "excited"

    if any(w in text_lower for w in ["calm", "relaxed", "peaceful"]):
        return "calm"

    if any(w in text_lower for w in ["sad", "depressed", "unhappy", "disappointed"]):
        return "sad"

    return None


#  Hybrid Emotion Detection
def detect_emotion(text):

    # 1. keyword override
    keyword = keyword_based_detection(text)
    if keyword:
        return keyword

    results = emotion_classifier(text)

    #  HANDLE ALL POSSIBLE FORMATS

    # case 1: [[...]]
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], list):
        results = results[0]

    # case 2: single dict
    if isinstance(results, dict):
        results = [results]

    # case 3: ensure list of dicts
    if isinstance(results, list) and isinstance(results[0], dict):
        best = max(results, key=lambda x: x['score'])
        label = best['label']
    else:
        return "neutral"  # fallback safety

    mapping = {
        "joy": "happy",
        "anger": "angry",
        "sadness": "sad",
        "fear": "sad",
        "surprise": "excited",
        "neutral": "neutral"
    }

    return mapping.get(label, "neutral")


# Split text into segments
def split_text_into_segments(text):
    # handle newlines + paragraphs
    text = text.replace("\n", " ")

    # split properly into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    return [s.strip() for s in sentences if s.strip()]


# Segment-level emotion detection
def detect_segment_emotion(segment):
    segment_lower = segment.lower().strip()

    if segment_lower.startswith(("oh", "wow", "what", "no way")) and len(segment.split()) <= 5:
        return "surprised"

    if "!" in segment:
        return "excited"

    return detect_emotion(segment)


#  Generate audio for each segment
async def generate_voice(text,voice_choice):
    segments = split_text_into_segments(text)

    # STEP 1: detect emotions
    base_emotions = [detect_segment_emotion(seg) for seg in segments]

    # STEP 2: build aligned segments + emotions together
    final_segments = []
    final_emotions = []

    for i in range(len(segments)):
        final_segments.append(segments[i])
        final_emotions.append(base_emotions[i])

        #  check for big jump → insert transition
        if i < len(base_emotions) - 1:
            prev = base_emotions[i]
            curr = base_emotions[i+1]

            if (prev == "excited" and curr == "sad") or \
               (prev == "sad" and curr == "excited") or \
               (prev == "angry" and curr == "calm") or \
               (prev == "calm" and curr == "angry"):

                final_segments.append("uh...")     # pause
                final_emotions.append("neutral") # transition

    filenames = []
    tasks = []

    # STEP 3: generate audio
    for i, (segment, emotion) in enumerate(zip(final_segments, final_emotions)):

        segment = segment.strip() + " "
        if not segment or len(segment) < 3:
            segment = "..."

        segment = segment + " "

        filename = f"static/part_{i}.mp3"
        filenames.append(filename)

        if voice_choice == "male":
            voice = "en-US-GuyNeural"
        else:
            voice = "en-US-AriaNeural"

        if emotion == "excited":
            rate, pitch = "+50%", "+30Hz"

        elif emotion == "happy":
            rate, pitch = "+30%", "+20Hz"

        elif emotion == "angry":
            rate, pitch = "+10%", "+5Hz"

        elif emotion == "sad":
            rate, pitch = "-40%", "-25Hz"

        elif emotion == "calm":
            rate, pitch = "-20%", "-5Hz"

        elif emotion == "surprised":
            rate, pitch = "-10%", "+40Hz"

        else:
            rate, pitch = "+0%", "+0Hz"

        communicate = edge_tts.Communicate(
            text=segment,
            voice=voice,
            rate=rate,
            pitch=pitch
        )

        tasks.append(communicate.save(filename))

    await asyncio.gather(*tasks)

    return filenames


#  Merge audio using ffmpeg
import subprocess
import os

def merge_audio(files):

    #  ensure files exist
    files = [os.path.abspath(f) for f in files if os.path.exists(f)]

    if not files:
        print("No valid audio files to merge")
        return

    # create file list
    with open("file_list.txt", "w", encoding="utf-8") as f:
        for file in files:
            f.write(f"file '{file}'\n")

    # run ffmpeg safely
    subprocess.run([
        "ffmpeg",
        "-y",  #  auto overwrite (fix your prompt issue)
        "-f", "concat",
        "-safe", "0",
        "-i", "file_list.txt",
        "-c", "copy",
        "static/output.mp3"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#smoothing 
def smooth_emotions(emotions):
    smoothed = [emotions[0]]

    for i in range(1, len(emotions)):
        prev = smoothed[-1]
        curr = emotions[i]

        #  smart transitions
        if prev == "excited" and curr == "sad":
            smoothed.append("calm")

        elif prev == "sad" and curr == "excited":
            smoothed.append("calm")

        elif prev == "angry" and curr == "calm":
            smoothed.append("neutral")

        elif prev == "calm" and curr == "angry":
            smoothed.append("neutral")

        #  slight variation (important)
        elif prev != curr:
            smoothed.append("neutral")

        smoothed.append(curr)

    return smoothed

#  Flask route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["text"]
        voice_choice = request.form["voice"]

        filenames = asyncio.run(generate_voice(text,voice_choice))
        merge_audio(filenames)

        emotion = detect_emotion(text)

        return render_template("index.html", text=text, emotion=emotion)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)