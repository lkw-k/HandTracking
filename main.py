import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)#웹캠 연결

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

while True:
    success, img = cap.read()
    if not success:
        print("카메라로부터 영상을 가져 올 수 없습니다.")
        break
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb) #손을 찾음

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)# mp_drawing = 미술 도구 상자, .draw_landmarks = 뼈대 그리는 친구
                                 # 어디에,무엇을,어떻게 이을까 핸드 커넥션은 점들끼리를 이어달라는 것임      
    cv2.imshow("Hand Image", img)
    if cv2.waitKey(1) == ord('p'):
        break

cap.release() #웹캠 해제
cv2.destroyAllWindows()