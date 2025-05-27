import cv2
import time
import mediapipe as mp
import pyttsx3
import threading

# Initialize mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak_text(text):
    threading.Thread(target=lambda: (engine.say(text), engine.runAndWait())).start()

# Gesture recognition function
def recognize_gesture(landmarks):
    thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]
    index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    index_pip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    middle_tip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    middle_pip = landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    ring_tip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
    ring_pip = landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP]
    pinky_tip = landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
    pinky_pip = landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP]
    
    # Thumb up
    if thumb_tip.y < thumb_ip.y and \
       index_tip.y > index_pip.y and \
       middle_tip.y > middle_pip.y and \
       ring_tip.y > ring_pip.y and \
       pinky_tip.y > pinky_pip.y:
        return "Thumb Up"
    
    # Open hand
    if (index_tip.y < index_pip.y and
        middle_tip.y < middle_pip.y and
        ring_tip.y < ring_pip.y and
        pinky_tip.y < pinky_pip.y and
        thumb_tip.x < index_tip.x):  # Thumb open to the side
        return "Open Hand"
    
    # Fist
    if (index_tip.y > index_pip.y and
        middle_tip.y > middle_pip.y and
        ring_tip.y > ring_pip.y and
        pinky_tip.y > pinky_pip.y):
        return "Fist"
    # "I Love You" Gesture (Thumb, Index, and Pinky up, others down)
    if (thumb_tip.y < thumb_ip.y and
        index_tip.y < index_pip.y and
        pinky_tip.y < pinky_pip.y and
        middle_tip.y > middle_pip.y and
        ring_tip.y > ring_pip.y):
        return "I Love You"
    
    # "No" Gesture (Thumb and index pinched together)
    if (abs(thumb_tip.x - index_tip.x) < 0.05 and
        abs(thumb_tip.y - index_tip.y) < 0.05):
        return "Fuck you"
    
     # "F*ck You" Gesture (only middle finger open)
    if (middle_tip.y < middle_pip.y and
        thumb_tip.y > thumb_ip.y and
        index_tip.y > index_pip.y and
        ring_tip.y > ring_pip.y and
        pinky_tip.y > pinky_pip.y):
        return "F*ck You"

    return None

# Start video
cap = cv2.VideoCapture(0)
previous_time = 0
last_spoken = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Ignoring empty frame.")
        continue

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            gesture = recognize_gesture(hand_landmarks)
            if gesture:
                current_time = time.time()
                if current_time - last_spoken > 2:
                    print(f"Recognized Gesture: {gesture}")
                    speak_text(gesture)
                    last_spoken = current_time
                
                cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time) if current_time != previous_time else 0
    previous_time = current_time
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
