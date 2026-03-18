# 🚀 Smart Attendance System (Face + Voice Recognition)

## 🔍 Overview

This project is a **real-time Smart Attendance System** that automates attendance tracking using **Face Recognition and Voice Authentication**. It replaces traditional manual methods with a secure, contactless, and intelligent solution built using computer vision and audio processing.

---

## 🎯 Problem Statement

Traditional attendance systems are:

* Time-consuming
* Prone to proxy/fraud
* Not scalable

This system solves these issues by using **AI-based identity verification**.

---

## 💡 Solution

The system captures live video and audio input from users, verifies identity using:

* Face Recognition (visual authentication)
* Voice Recognition (secondary verification)

Once validated, attendance is automatically recorded and displayed in real-time.

---

## ✨ Key Features

* 👤 Real-time Face Detection & Recognition
* 🎤 Voice-based Authentication
* ⚡ Instant Attendance Marking
* 📊 Automatic Attendance Storage (CSV)
* 🌐 Web Interface for interaction
* 🔒 Multi-factor Authentication (Face + Voice)

---

## 🧠 Tech Stack

* **Backend:** Python, Flask
* **Computer Vision:** OpenCV
* **Audio Processing:** Speech Recognition
* **Frontend:** HTML, CSS, JavaScript
* **Data Storage:** CSV File

---

## 🏗️ System Workflow

```
User → Webcam & Microphone Input
     → Face Detection & Matching
     → Voice Verification
     → Attendance Marked
     → Stored in CSV & Displayed on UI
```

---

## 📂 Project Structure

```
smart-attendance-system/
│
├── static/              # CSS, JS, assets
├── templates/           # HTML pages
├── dataset/             # Stored face images
├── models/              # Trained models
├── app.py               # Main Flask server
├── detect.py            # Face recognition logic
├── voice.py             # Voice processing
├── attendance.csv       # Attendance data
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-attendance-system.git
cd smart-attendance-system
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```



## 📊 Results

* ✔️ Accurate identity recognition
* ✔️ Reduced manual workload
* ✔️ Faster attendance process
* ✔️ Improved security (no proxy attendance)

---

## 🔮 Future Enhancements

* Cloud database (Firebase / MongoDB)
* Mobile application support
* Deep learning models for higher accuracy
* Admin dashboard & analytics

---

## 🏆 Key Highlights for Recruiters

* Combines **Computer Vision + Audio Processing**
* Implements **real-time AI system**
* Solves a **real-world problem**
* Demonstrates **full-stack development skills**

---

## 👨‍💻 Author

**Parna Sree**


---

## ⭐ Support

If you found this project useful, give it a ⭐ on GitHub!
