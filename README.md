# Face and Voice Based Attendance System

### A Dual Biometric Smart Attendance Solution

This project is a secure and intelligent attendance system that uses both **face recognition and voice recognition** to verify user identity. By combining two biometric factors, the system ensures higher accuracy and prevents proxy attendance.

---

## Problem Statement

Traditional attendance systems suffer from several limitations:

* Proxy attendance (fake marking)
* Time-consuming manual processes
* Lack of security in single-factor systems

Face-only systems can be spoofed, and manual systems are inefficient. Hence, there is a need for a **more secure and automated attendance solution**.

---

## Solution

This system introduces a **dual biometric authentication mechanism** that verifies users using both **facial features and voice patterns**.

The system ensures:

* Identity is confirmed through face recognition
* Additional verification using voice authentication
* Attendance is marked only when both match successfully

---

## How It Works

### 1. Registration Phase

* User registers their face using a webcam
* Voice samples are recorded and stored
* Data is saved in the system database

---

### 2. Face Recognition

* The system captures live video input
* Detects and encodes the face
* Matches with stored face data

---

### 3. Voice Verification

* User is prompted to speak
* Voice is recorded and processed
* Compared with stored voice features

---

### 4. Attendance Marking

* If both face and voice match:
  → Attendance is marked
* If either fails:
  → Access is denied

---

## Features

* Dual biometric authentication
* Real-time face detection
* Voice verification for added security
* Prevention of proxy attendance
* Automatic attendance logging
* Easy registration and update system

---

## Advantages

* High security compared to single biometric systems
* Accurate and reliable attendance tracking
* Reduces manual effort
* Scalable for classrooms and organizations

---

## Tech Stack

### Frontend

* Python GUI (Tkinter / Web Interface optional)

### Backend

* Python

### Computer Vision

* OpenCV
* face_recognition

### Voice Processing

* SpeechRecognition / Whisper
* Librosa (for audio features)

### Database

* SQLite / CSV

---

## How to Run

```bash id="x2k91a"
# Clone the repository
git clone https://github.com/your-username/face-voice-attendance.git

# Navigate to project directory
cd face-voice-attendance

# Install required libraries
pip install -r requirements.txt

# Run the system
python main.py
```

---

## Expected Output

* Recognizes user face via webcam
* Verifies voice input
* Marks attendance with timestamp
* Stores records in database

---

## Future Enhancements

* Mobile application integration
* Cloud-based storage
* Anti-spoofing techniques (liveness detection)
* Multi-user real-time tracking
* Integration with college ERP systems

---

## Author

J.Parna Sree

---

## Conclusion

This system provides a secure, efficient, and modern solution for attendance management by combining face and voice biometrics, making it highly suitable for academic institutions and organizations.

---
