import pyttsx3
from textblob import TextBlob
import asyncio
import edge_tts
import re


def detect_emotion(text):
    text_lower = text.lower()

    # 🔥 CLEAN TEXT (VERY IMPORTANT)
    words = re.findall(r'\b\w+\b', text_lower)

    scores = {
        "angry": 0,
        "excited": 0,
        "calm": 0,
        "sad": 0,
        "happy": 0
    }

    angry_words = {"angry", "frustrated", "annoyed", "furious", "irritating", "irritated"}
    sad_words = {"sad", "depressed", "unhappy", "disappointed", "upset"}
    excited_words = {"excited", "thrilled", "amazing", "incredible", "awesome"}
    calm_words = {"calm", "relaxed", "peaceful", "quiet"}
    happy_words = {"happy", "glad", "joyful", "pleased"}

    for word in words:
        if word in angry_words:
            scores["angry"] += 3
        if word in sad_words:
            scores["sad"] += 1
        if word in excited_words:
            scores["excited"] += 2
        if word in calm_words:
            scores["calm"] += 2
        if word in happy_words:
            scores["happy"] += 1

    # punctuation boost
    if "!" in text:
        scores["excited"] += 1

    print("DEBUG words:", words)
    print("DEBUG scores:", scores)

    # fallback only if no keywords matched
    if all(score == 0 for score in scores.values()):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.4:
            return "happy"
        elif polarity < -0.4:
            return "sad"
        else:
            return "neutral"

    return max(scores, key=scores.get)

def get_voice_params(emotion, polarity):
    base_rate = 150
    base_volume = 0.9

    intensity = abs(polarity)

    if emotion == "happy":
        rate = base_rate + int(120 * intensity)  
        volume = 1.0
    elif emotion == "sad":
        rate = base_rate - int(100 * intensity)   
        volume = 0.5
    else:
        rate = base_rate
        volume = 0.8

    return rate, volume

async def generate_voice(text, emotion):

    if emotion == "happy":
        voice = "en-US-AriaNeural"
        rate = "+40%"
        pitch = "+25Hz"

    elif emotion == "excited":
        voice = "en-US-GuyNeural"
        rate = "+60%"
        pitch = "+40Hz"

    elif emotion == "sad":
        voice = "en-US-JennyNeural"
        rate = "-40%"
        pitch = "-25Hz"

    elif emotion == "angry":
        voice = "en-US-GuyNeural"
        rate = "+20%"
        pitch = "+10Hz"

    elif emotion == "calm":
        voice = "en-US-AriaNeural"
        rate = "-20%"
        pitch = "-5Hz"

    else:  # neutral
        voice = "en-US-AriaNeural"
        rate = "+0%"
        pitch = "+0Hz"

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )

    await communicate.save("static/output.mp3")


def main():
    print("\n🎙️ === Empathy Engine ===\n")
    
    text = input("Enter your text: ")

    print("INPUT TEXT:", text)
    emotion = detect_emotion(text)
    print("FINAL EMOTION:", emotion)
    emotion, polarity = detect_emotion(text)
    print("INPUT TEXT:", text)
    emotion = detect_emotion(text)
    print("FINAL EMOTION:", emotion)
    rate, volume = get_voice_params(emotion, polarity)

    print("\nAnalysis Result:")
    print(f"→ Detected Emotion : {emotion.upper()}")
    print(f"→ Polarity Score   : {polarity:.2f}")

    print("\nVoice Configuration:")
    print(f"→ Speech Rate : {rate}")
    print(f"→ Volume      : {volume}")

    asyncio.run(generate_voice(text, emotion))

    print("\nAudio generated successfully: output.wav")
    print("Try different emotional sentences to see variation!\n")


if __name__ == "__main__":
    main()
