import cv2
import mediapipe as mp
import pyautogui

screenwidth, screenheight = pyautogui.size()
hand_detector = mp.solutions.hands.Hands()
cap = cv2.VideoCapture(0)
drawing = mp.solutions.drawing_utils
_, frame = cap.read()
frame = cv2.flip(frame, 1)
rgbframe = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imshow('Cursor', frame)

while True:
    _, frame = cap.read()
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

                    if id == 8:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                        index_x = x * screenwidth / frame_width
                        index_y = y * screenheight / frame_height
                        pyautogui.moveTo(index_x, index_y)

                    if id == 4:
                        cv2.circle(img=frame, center=(x, y), radius=10, color=(255, 0, 0))
                        thumbindex_x = x * screenwidth / frame_width
                        thumbindex_y = y * screenheight / frame_height
                        if abs(index_y - thumbindex_y) < 50:
                            try:
                                pyautogui.click(button='left', x=index_x, y=index_y, interval=0.1)
                                print("Click successful")
                            except Exception as e:
                                print(f"Click failed: {e}")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Cursor', frame)
