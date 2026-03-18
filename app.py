import os
import cv2
import csv
import datetime
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import face_recognition
from resemblyzer import VoiceEncoder, preprocess_wav
import soundfile as sf

# Initialize app
app = Flask(__name__)
CORS(app)

# Directories
FACE_DIR = "face_data"
VOICE_DIR = "voice_data"
EMBED_DIR = "embeddings"
UPLOAD_DIR = "uploads"
ATTENDANCE_FILE = "attendance.csv"

os.makedirs(FACE_DIR, exist_ok=True)
os.makedirs(VOICE_DIR, exist_ok=True)
os.makedirs(EMBED_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

encoder = VoiceEncoder()

# 🔍 Helper functions

def save_embedding(path, embedding):
    np.save(path, embedding)

def load_embedding(path):
    return np.load(path)

def get_all_embeddings():
    embeddings = []
    names = []
    for file in os.listdir(EMBED_DIR):
        if file.endswith("_face.npy"):
            name = file.replace("_face.npy", "")
            face_emb = load_embedding(os.path.join(EMBED_DIR, file))
            voice_file = os.path.join(EMBED_DIR, f"{name}_voice.npy")
            if os.path.exists(voice_file):
                voice_emb = load_embedding(voice_file)
                embeddings.append((name, face_emb, voice_emb))
                names.append(name)
    return embeddings

def mark_attendance(name):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "time"])
    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([name, now])

def convert_webm_to_wav(webm_path, wav_path):
    os.system(f"ffmpeg -y -i \"{webm_path}\" \"{wav_path}\"")

# 📝 Routes

@app.route("/register", methods=["POST"])
def register():
    try:
        name = request.form["name"]
        face_file = request.files["face_image"]
        voice_file = request.files["voice_file"]

        # Save face
        face_path = os.path.join(FACE_DIR, f"{name}.jpg")
        face_file.save(face_path)

        # Save voice (webm → wav)
        raw_path = os.path.join(UPLOAD_DIR, f"{name}.webm")
        wav_path = os.path.join(VOICE_DIR, f"{name}.wav")
        voice_file.save(raw_path)
        convert_webm_to_wav(raw_path, wav_path)

        # Face embedding
        image = face_recognition.load_image_file(face_path)
        image = np.ascontiguousarray(image)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return jsonify({"error": "No face found."}), 400
        face_embedding = encodings[0]
        save_embedding(os.path.join(EMBED_DIR, f"{name}_face.npy"), face_embedding)

        # Voice embedding
        wav, sr = sf.read(wav_path)
        wav_preprocessed = preprocess_wav(wav, source_sr=sr)
        voice_embedding = encoder.embed_utterance(wav_preprocessed)
        save_embedding(os.path.join(EMBED_DIR, f"{name}_voice.npy"), voice_embedding)

        return jsonify({"message": "Registration successful!"})
    except Exception as e:
        print("Registration failed:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/recognize", methods=["POST"])
def recognize():
    try:
        face_file = request.files["face_image"]
        voice_file = request.files["voice_file"]

        # Save temp files
        temp_face = os.path.join(UPLOAD_DIR, "temp.jpg")
        temp_webm = os.path.join(UPLOAD_DIR, "temp.webm")
        temp_wav = os.path.join(UPLOAD_DIR, "temp.wav")
        face_file.save(temp_face)
        voice_file.save(temp_webm)
        convert_webm_to_wav(temp_webm, temp_wav)

        # Face encoding
        image = face_recognition.load_image_file(temp_face)
        image = np.ascontiguousarray(image)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            return jsonify({"error": "No face found."}), 400
        face_embedding = encodings[0]

        # Voice encoding
        wav, sr = sf.read(temp_wav)
        wav_preprocessed = preprocess_wav(wav, source_sr=sr)
        voice_embedding = encoder.embed_utterance(wav_preprocessed)

        # Compare with saved embeddings
        all_embeddings = get_all_embeddings()
        best_match = None
        for name, saved_face, saved_voice in all_embeddings:
            face_dist = np.linalg.norm(saved_face - face_embedding)
            voice_sim = 1 - np.dot(saved_voice, voice_embedding) / (np.linalg.norm(saved_voice) * np.linalg.norm(voice_embedding))
            if face_dist < 0.5 and voice_sim < 0.35:  # tune thresholds
                best_match = name
                break

        if best_match:
            mark_attendance(best_match)
            return jsonify({"message": f"Recognized: {best_match}"})
        else:
            return jsonify({"error": "No match found"}), 404

    except Exception as e:
        print("Recognition failed:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/attendance", methods=["GET"])
def attendance():
    rows = []
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append({"name": row["name"], "time": row["time"]})
    return jsonify(rows)

# Optional: serve HTML locally if testing
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

# Run
if __name__ == "__main__":
    print("Loaded the voice encoder model on cpu.")
    app.run(debug=True)
