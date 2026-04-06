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
            #print(hand_landmarks.landmark[8])
            #print(f"검지 끝 y: {hand_landmarks.landmark[8].y:.2f} | 검지 뿌리 y: {hand_landmarks.landmark[6].y:.2f}")
            #검지 끝과 뿌리의 y좌표를 비교하여 손가락이 펴졌는지 구부러졌는지 판단을 함 아주 유용 보기 간편하게 만든것임
            #검지 접히고 펴짐 확인하려고 사용한 코드 
            f_tip_y = hand_landmarks.landmark[8].y
            f_pip_y = hand_landmarks.landmark[6].y

            if f_tip_y < f_pip_y:
                print("펴짐")
            else:
                print("접힘")
    cv2.imshow("Hand Image", img)
    if cv2.waitKey(1) == ord('p'):
        break

cap.release() #웹캠 해제
cv2.destroyAllWindows()