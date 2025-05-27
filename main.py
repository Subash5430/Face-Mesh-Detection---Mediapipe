import cv2
import numpy as np
import mediapipe as mp

mp_drawing=mp.solutions.drawing_utils
mp_faceMesh=mp.solutions.face_mesh

video=cv2.VideoCapture(0)

with mp_faceMesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_faces=3) as faceMesh:
    while True:
        ret,image=video.read()
        image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image.flags.writeable=False
        results=faceMesh.process(image)
        # print(results)
        image.flags.writeable=True
        image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mp_drawing.draw_landmarks(image, face_landmarks, mp_faceMesh.FACEMESH_TESSELATION,
                                          mp_drawing.DrawingSpec(color=(0, 0,255), thickness=1, circle_radius=1),
                                          mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1))
        cv2.imshow("Video", image)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()

