import cv2
import mediapipe as mp
import pyautogui
import time

# Get screen dimensions
screenwidth, screenheight = pyautogui.size()

# Initialize MediaPipe Hands module
hand_detector = mp.solutions.hands.Hands()
drawing = mp.solutions.drawing_utils

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Set the capture frame size to match the screen size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, screenwidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screenheight)

while cap.isOpened():
    _, frame = cap.read()
    '''
    if not _:
        continue
    '''

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    output = hand_detector.process(frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            for id, landmark in enumerate(landmarks):
                if id == 8:
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    index_x = x * screenwidth / frame_width
                    index_y = y * screenheight / frame_height

                    if id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 0, 0))
                        index_x = x * screenwidth / frame_width
                        index_y = y * screenheight / frame_height
                        pyautogui.moveTo(index_x, index_y)

                    if id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 0))
                        thumbindex_x = x * screenwidth / frame_width
                        thumbindex_y = y * screenheight / frame_height
                        print(abs(index_y - thumbindex_y))
                        if abs(index_y - thumbindex_y) > 50:
                            print("click")
                            pyautogui.click(index_x, index_y)
                            pyautogui.sleep(1)

    cv2.imshow('Cursor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
