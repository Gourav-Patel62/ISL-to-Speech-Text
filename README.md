Hand Gesture Recognition using MediaPipe and OpenCV
This project implements real-time hand gesture recognition using a webcam, leveraging MediaPipe, OpenCV, and pyttsx3 for gesture detection and audio feedback. It detects common hand gestures like "Thumb Up", "Open Hand", "Fist", "I Love You", and more, and speaks out the recognized gesture.

📦 Features
Real-time webcam hand gesture recognition

Audio feedback using text-to-speech (TTS)

Visual feedback using OpenCV overlays

Custom gesture detection using landmark analysis

Frame rate (FPS) display

🧠 Recognized Gestures
👍 Thumb Up

🖐️ Open Hand

✊ Fist

🤟 I Love You

❌ "No" (Thumb and Index Pinched)

🛠️ Requirements
Install the required packages using pip:

bash
Copy
Edit
pip install opencv-python mediapipe pyttsx3
▶️ How to Run
Connect your webcam.

Run the script:

bash
Copy
Edit
python isl3.py
Show hand gestures in front of the camera.

To exit, press q.

🧩 Code Structure
MediaPipe is used to detect hand landmarks.

Gesture logic is written in the recognize_gesture() function.

Text-to-speech is handled by pyttsx3 running on a separate thread.

OpenCV displays the camera feed, landmarks, gesture text, and FPS.

🔒 Notes
The script is configured for a single hand detection.

Gesture recognition is sensitive to hand position and lighting.

Make sure your webcam has clear visibility of the hand.
