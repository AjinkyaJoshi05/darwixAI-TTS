# Empathy Engine 🎙️

## 🚀 Overview
The Empathy Engine is a Python-based system that converts text into emotionally expressive speech. It analyzes the sentiment of input text and dynamically adjusts vocal characteristics such as rate and pitch to generate human-like audio output.

This project aims to bridge the gap between textual sentiment and vocal expression, making AI interactions more natural and engaging.

---

## ✨ Features
- Emotion Detection (Happy, Sad, Neutral)
- Dynamic Voice Modulation (Rate + Pitch)
- Intensity Scaling based on sentiment strength
- High-quality speech synthesis using Edge TTS
- Audio output generation (.mp3)

---

## 🧠 How It Works

1. **Input Text** is provided by the user.
2. **Sentiment Analysis** is performed using TextBlob.
3. The system classifies emotion into:
   - Positive → Happy
   - Negative → Sad
   - Neutral → Neutral
4. **Voice parameters are adjusted dynamically:**
   - Happy → Faster rate, higher pitch
   - Sad → Slower rate, lower pitch
   - Neutral → Default settings
5. **Speech is generated** using Edge TTS and saved as an audio file.

---

## ⚙️ Tech Stack
- Python
- TextBlob (Sentiment Analysis)
- Edge-TTS (Speech Synthesis)

---

## 🛠️ Setup Instructions

```bash
pip install -r requirements.txt
python -m textblob.download_corpora
python app.py
```
# 📊 Design Decisions

- TextBlob was chosen for quick and efficient sentiment detection.
- Edge-TTS was used to overcome limitations of offline TTS engines and enable pitch control.
- Intensity scaling enhances realism by adjusting speech based on sentiment strength.

# 🔥 Example

**Input:**

```text
I am extremely happy today!
```

**Output:**

- Emotion: Happy
- Speech: Faster, higher pitch, energetic tone

# 🚧 Future Improvements

- Support for more granular emotions (angry, excited, concerned)
- Web-based interface (Flask/FastAPI)
- Multi-language support
- Real-time speech generation API

