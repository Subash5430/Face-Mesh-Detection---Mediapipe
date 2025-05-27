import cv2
import mediapipe as mp

mp_drawing=mp.solutions.drawing_utils
mp_hand=mp.solutions.hands
video=cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=5) as hands:

    while True:
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=hands.process(image)
        image.flags.writeable=True
        image=cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image,hand_landmarks, mp_hand.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2))
        cv2.imshow("Video", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()