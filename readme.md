# 🎙️ Empathy Engine — Emotion-Aware Text-to-Speech

##  Overview

The **Empathy Engine** is an AI-powered text-to-speech system that generates **emotionally expressive voice output** from plain text.

Unlike traditional TTS systems that produce flat and robotic speech, this project dynamically adjusts vocal characteristics such as **pitch and speech rate** based on the detected emotion of the input text. It also supports **multi-sentence emotional variation**, ensuring a more natural and human-like interaction.

---

##  Key Features

*  **Emotion Detection (NLP-based)**
  Uses a transformer-based model to classify text into emotions such as happy, sad, angry, calm, and excited.

*  **Hybrid Emotion System**
  Combines:

  * Rule-based keyword detection (fast and precise for strong emotions)
  * Transformer model (robust general understanding)

*  **Multi-Segment Emotion Handling**
  Splits input text into sentences and processes each segment independently.

*  **Emotion Smoothing**
  Avoids abrupt emotional jumps by inserting intermediate emotional states for natural transitions.

*  **Dynamic Voice Modulation**
  Adjusts:

  * Speech Rate
  * Pitch
    based on detected emotion.

*  **User-Selectable Voice (Male/Female)**
  Maintains speaker consistency while varying tone.

*  **Audio Merging with FFmpeg**
  Combines multiple generated audio segments into a single output file.

*  **Web Interface (Flask)**
  Simple UI to input text, select voice, and play generated audio.

---

##  Tech Stack

* **Language:** Python
* **Backend Framework:** Flask
* **NLP / Emotion Detection:** Hugging Face Transformers
* **TTS Engine:** edge-tts
* **Audio Processing:** FFmpeg (used for reliable concatenation of multiple TTS audio segments)
* **Frontend:** HTML + CSS

---

##  Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AjinkyaJoshi05/darwixAI-TTS.git
cd darwixAI-TTS
```

---

### 2️⃣ Install Dependencies

```bash
pip install flask edge-tts transformers torch
```

---

### 3️⃣ Install FFmpeg 

Download from: https://ffmpeg.org/download.html

### 🔧 Setting up FFmpeg (Important for Windows Users)

After downloading FFmpeg:

1. Extract the downloaded ZIP file  
2. Open the extracted folder → go to the `bin` directory  
3. Copy the full path (example):

```bash
C:\Users\YourName\Downloads\ffmpeg\bin
```
4. Add this path to Environment Variables:
- Search: **Environment Variables**
- Click **Edit the system environment variables**
- Click **Environment Variables**
- Under **User variables → Path → Edit**
- Click **New** and paste the copied path
- Click **OK**

5. Restart your terminal / VS Code

6. Verify installation:

```bash
ffmpeg -version
```

---

### 4️⃣ Run the Application

```bash
python app_flask.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

##  How It Works

1. **Input Processing**

   * User enters text via the web interface
   * Text is split into sentence-level segments

2. **Emotion Detection**

   * Each segment is analyzed using:

     * Keyword-based rules (for strong signals like "frustrated", "amazing")
     * Transformer model (general sentiment understanding)

3. **Emotion Smoothing**

   * Detects abrupt transitions (e.g., excited → sad)
   * Inserts intermediate states (e.g., calm or neutral) to improve flow

4. **Voice Parameter Mapping**

   * Each emotion is mapped to specific vocal parameters:

| Emotion | Rate Change | Pitch Change |
| ------- | ----------- | ------------ |
| Happy   | +30%        | +20Hz        |
| Excited | +50%        | +30Hz        |
| Sad     | -40%        | -25Hz        |
| Angry   | +10%        | +5Hz         |
| Calm    | -20%        | -5Hz         |
| Neutral | 0%          | 0Hz          |

5. **Speech Generation**

   * Each segment is converted to speech using edge-tts
   * A single consistent voice is maintained

6. **Audio Composition**

   * Each segment is generated as an individual audio file
   * These files are merged into a single output using FFmpeg
   * FFmpeg ensures efficient and accurate concatenation without re-encoding artifacts

---

##  Design Decisions

### 🔹 Hybrid Emotion Detection

* Pure ML models may misclassify strong emotions (e.g., "frustrated" → sad)
* Keyword overrides improve accuracy and interpretability

---

### 🔹 Single Voice Strategy

* Using multiple voices created unnatural speaker shifts
* A single voice is maintained while modulating pitch and rate

---

### 🔹 Emotion Smoothing

* Direct transitions like *excited → sad* felt abrupt
* Intermediate emotional states are introduced for smoother transitions

---

### 🔹 Segment-Based Processing

* Each sentence is processed independently instead of assigning a single emotion to the entire paragraph

---

### 🔹 Use of FFmpeg for Audio Merging

* Direct merging of compressed audio (MP3) is complex in Python
* FFmpeg was chosen as an industry-standard solution for reliable audio concatenation

---

### 🔹 Consideration of SSML (Speech Synthesis Markup Language)

* Explored the use of SSML for fine-grained control over speech (pauses, emphasis, prosody)
* Initial experiments were conducted using SSML tags such as `<prosody>` and `<break>`
* Due to limitations in the selected TTS engine (edge-tts), full SSML support was not feasible
* Instead, dynamic pitch and rate modulation was used to achieve expressive and stable results

---

##  Example Input

```
I am so excited! This is amazing.
But honestly, I feel a bit sad.
Still, I will stay calm.
```

 Output:

* Excited tone → Smooth transition → Sad tone → Calm tone
* Consistent voice with dynamic emotional variation

---

##  Future Improvements

* Emotion intensity scaling
* Real-time streaming TTS
* Multilingual support
* Full SSML integration using advanced TTS APIs
* Enhanced UI/UX

---

##  Author

**Ajinkya Joshi**

---

##  Final Note

This project demonstrates how combining **NLP, speech synthesis, and system design** can create emotionally intelligent AI interactions that go beyond basic text-to-speech systems.
