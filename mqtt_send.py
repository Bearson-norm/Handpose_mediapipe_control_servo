import cv2
import mediapipe as mp
import numpy as np
import paho.mqtt.client as mqtt

# MQTT broker information
broker = "dimasalifta.tech"
port = 1883
topic = "handpose/keypoints"

# Mediapipe initialization
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# MQTT client setup
client = mqtt.Client("HandPosePublisher")
client.connect(broker, port, keepalive=60)

def on_publish(client, userdata, result):
    print("Data published successfully")

# Function to process frame and publish keypoints
def process_frame(frame):
    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Extracting landmarks
                keypoints = np.zeros((21, 3))
                for i, landmark in enumerate(hand_landmarks.landmark):
                    keypoints[i] = [landmark.x, landmark.y, landmark.z if landmark.z else 0]

                # Publishing keypoints via MQTT
                client.publish(topic, str(keypoints.tolist()))

        # Drawing landmarks on the frame (optional)
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        return frame

# Main function to capture video and process frames
def main():
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        processed_frame = process_frame(frame)

        cv2.imshow('Hand Pose Detection', processed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    client.on_publish = on_publish
    main()
