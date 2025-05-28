import cv2 as cv
import mediapipe as mp
from pynput.keyboard import Key, Controller

keyboard = Controller()

mp_draw = mp.solutions.drawing_utils 
mp_hand = mp.solutions.hands 
hands = mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

fingerTipIds = [4, 8, 12, 16, 20]  

video = cv.VideoCapture(0)

while True:
    success, image = video.read()
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

    landmarks_list = []

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[-1]
        h, w, c = image.shape

        for index, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmarks_list.append([index, cx, cy])

        mp_draw.draw_landmarks(image, hand_landmarks, mp_hand.HAND_CONNECTIONS)

    fingers_open = []

    if landmarks_list:
        for tipId in fingerTipIds:
            if tipId == 4:  
                if landmarks_list[tipId][1] > landmarks_list[tipId - 1][1]:
                    fingers_open.append(1)
                else:
                    fingers_open.append(0)
            else:
                if landmarks_list[tipId][2] < landmarks_list[tipId - 2][2]:
                    fingers_open.append(1)
                else:
                    fingers_open.append(0)

        count = fingers_open.count(1)

        if fingers_open == [0, 1, 0, 0, 0]: 
            cv.putText(image, "UP", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
            keyboard.press(Key.up)
            keyboard.release(Key.up)

        elif fingers_open == [0, 1, 1, 0, 0]:  
            cv.putText(image, "DOWN", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
            keyboard.press(Key.down)
            keyboard.release(Key.down)

        elif fingers_open == [1, 1, 1, 1, 1]:  
            cv.putText(image, "RIGHT", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
            keyboard.press(Key.right)
            keyboard.release(Key.right)

        elif fingers_open == [0, 0, 0, 0, 0]:
            cv.putText(image, "LEFT", (50, 100), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
            keyboard.press(Key.left)
            keyboard.release(Key.left)

    cv.imshow("Hand Gesture - 2048 Control", image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv.destroyAllWindows()
