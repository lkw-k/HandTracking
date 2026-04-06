import cv2
import mediapipe as mp

def is_finger_open(landmark, tip, pip):
    tip_y = landmark[tip].y
    pip_y = landmark[pip].y

    if tip_y < pip_y:
        return True
    else:
        return False

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
                                 
            if is_finger_open(hand_landmarks.landmark,4,2):
                print("엄지 펴짐")
            else:
                print("엄지 접힘")
            if is_finger_open(hand_landmarks.landmark,8,6):
                print("검지 펴짐")
            else:
                print("검지 접힘")
            if is_finger_open(hand_landmarks.landmark,12,10):
                print("중지 펴짐")
            else:
                print("중지 접힘")
            if is_finger_open(hand_landmarks.landmark,16,14):
                print("약지 펴짐")
            else:
                print("약지 접힘")
            if is_finger_open(hand_landmarks.landmark,20,18):
                print("소지 펴짐")
            else:
                print("소지 접힘")    
            
    cv2.imshow("Hand Image", img)
    if cv2.waitKey(1) == ord('p'):
        break

cap.release() #웹캠 해제
cv2.destroyAllWindows()