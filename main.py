import cv2
import mediapipe as mp
import pyautogui
import math

def is_finger_open(landmark, tip, pip):
    tip_y = landmark[tip].y
    pip_y = landmark[pip].y

    if tip_y < pip_y:
        return True
    else:
        return False

def get_distance(landmark, p1, p2):
    x1 = landmark[p1].x 
    y1 = landmark[p1].y
    x2 = landmark[p2].x
    y2 = landmark[p2].y
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


cap = cv2.VideoCapture(0)#웹캠 연결
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # 가로 해상도 낮춤
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240) # 세로 해상도 낮춤
cap.set(cv2.CAP_PROP_FPS, 120) #웹캠 프레임을 원하는 120까지 올림

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1)

screen_w, screen_h = pyautogui.size() #해상도 자동 조정

prev_x = 0
prev_y = 0
smoothing = 0.23 #마우스 움직임을 부드럽게 하기위함

while True:
    success, img = cap.read()
    if not success:
        print("카메라로부터 영상을 가져 올 수 없습니다.")
        break

    img = cv2.flip(img, 1) #화면 좌우 반전

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb) #손을 찾음

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
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

            if is_finger_open(hand_landmarks.landmark, 8, 6) and \
                not is_finger_open(hand_landmarks.landmark, 12, 10) and \
                not is_finger_open(hand_landmarks.landmark, 16, 14) and \
                not is_finger_open(hand_landmarks.landmark, 20, 18):
                    x = hand_landmarks.landmark[8].x * screen_w   #x픽셀/ 좌우반전,부드럽게
                    y = hand_landmarks.landmark[8].y * screen_h #y픽셀

                    curr_x = prev_x * (1- smoothing) + x* smoothing
                    curr_y = prev_y * (1- smoothing) + y* smoothing #스무딩 한거임 
                    

                    pyautogui.moveTo(curr_x, curr_y) #마우스 움직이는 친구

                    prev_x = curr_x
                    prev_y = curr_y

                    print("마우스 이동")

            elif all([is_finger_open(lm, tip, tip-2) for tip in [4, 8, 12, 16, 20]]):
                print("마우스 고정")

            distance = get_distance(hand_landmarks.landmark, 8, 12)
            if distance < 0.05:
                pyautogui.click()
                print("클릭!")
            
            
    cv2.imshow("Hand Image", img)
    if cv2.waitKey(1) == ord('p'):
        break

cap.release() #웹캠 해제
cv2.destroyAllWindows()