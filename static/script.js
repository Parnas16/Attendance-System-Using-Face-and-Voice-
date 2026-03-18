const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const nameInput = document.getElementById("nameInput");
const status = document.getElementById("status");

let mediaRecorder;
let audioChunks = [];

// 🎥 Start webcam and mic
navigator.mediaDevices.getUserMedia({ video: true, audio: true })
  .then(stream => {
    video.srcObject = stream;
    video.play();
    console.log("Camera and mic access granted.");
  })
  .catch(err => {
    console.error("Webcam error:", err);
    alert("❌ Webcam/Microphone access denied. Please allow permissions in browser.");
  });

// 🎤 Start recording voice
function startRecording() {
  audioChunks = [];
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
      mediaRecorder.onstop = () => console.log("Recording stopped.");
      mediaRecorder.start();
      status.innerText = "🎙️ Voice recording started...";
    })
    .catch(err => {
      console.error("Voice recording error:", err);
      alert("Microphone permission denied.");
    });
}

// 🛑 Stop recording voice
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    status.innerText = "🛑 Voice recording stopped.";
  }
}

// 📸 Capture face from webcam
function captureImage() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0);
  return new Promise(resolve => canvas.toBlob(resolve, "image/jpeg"));
}

// 🔄 Convert blob to File
function blobToFile(blob, name) {
  return new File([blob], name, { type: blob.type });
}

// ✅ Register user
async function register() {
  const name = nameInput.value.trim();
  if (!name) return alert("⚠️ Enter your name first.");
  if (audioChunks.length === 0) return alert("⚠️ Please record your voice first.");

  const faceBlob = await captureImage();
  const voiceBlob = new Blob(audioChunks, { type: "audio/webm" });

  const formData = new FormData();
  formData.append("name", name);
  formData.append("face_image", blobToFile(faceBlob, "face.jpg"));
  formData.append("voice_file", blobToFile(voiceBlob, "voice.webm"));

  status.innerText = "📤 Registering...";
  try {
    const res = await fetch("/register", { method: "POST", body: formData });
    const data = await res.json();
    status.innerText = data.message || `❌ ${data.error}`;
    fetchAttendance();
  } catch (err) {
    console.error("Register error:", err);
    status.innerText = "❌ Registration failed.";
  }
}

// 🔍 Recognize user
async function recognize() {
  if (audioChunks.length === 0) return alert("⚠️ Please record your voice first.");
  const faceBlob = await captureImage();
  const voiceBlob = new Blob(audioChunks, { type: "audio/webm" });

  const formData = new FormData();
  formData.append("face_image", blobToFile(faceBlob, "face.jpg"));
  formData.append("voice_file", blobToFile(voiceBlob, "voice.webm"));

  status.innerText = "🔍 Recognizing...";
  try {
    const res = await fetch("/recognize", { method: "POST", body: formData });
    const data = await res.json();
    status.innerText = data.message || `❌ ${data.error}`;
    fetchAttendance();
  } catch (err) {
    console.error("Recognition error:", err);
    status.innerText = "❌ Recognition failed.";
  }
}

// 📋 Fetch attendance list
async function fetchAttendance() {
  try {
    const res = await fetch("/attendance");
    const data = await res.json();

    const tbody = document.querySelector("#attendanceTable tbody");
    tbody.innerHTML = "";
    data.forEach(row => {
      const tr = document.createElement("tr");
      tr.innerHTML = `<td>${row.name}</td><td>${row.time}</td>`;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Attendance fetch error:", err);
  }
}

// 🧠 Load attendance on page load
window.onload = fetchAttendance;
