import cv2
import mediapipe as mp
import serial
import time

# Cấu hình cổng serial (thay COM3 bằng cổng Arduino của bạn)
SERIAL_PORT = 'COM2'
BAUD_RATE = 9600

# Khởi tạo serial
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Đợi Arduino khởi động
except Exception as e:
    print(f"Không thể kết nối Arduino: {e}")
    ser = None

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        hand_open = False
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Kiểm tra ngón tay cái và các ngón còn lại
                finger_tips = [4, 8, 12, 16, 20]
                finger_open = []
                for tip in finger_tips:
                    if tip == 4:  # Ngón cái
                        finger_open.append(
                            hand_landmarks.landmark[tip].x < hand_landmarks.landmark[tip - 1].x
                        )
                    else:
                        finger_open.append(
                            hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y
                        )
                if sum(finger_open) >= 4:
                    hand_open = True
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        # Gửi tín hiệu đến Arduino
        if ser:
            if hand_open:
                ser.write(b'1')  # Bật đèn
                print("Send: 1")
            else:
                ser.write(b'0')  # Tắt đèn
                print("Send: 0")
        cv2.putText(frame, f"Hand open: {hand_open}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0) if hand_open else (0,0,255), 2)
        cv2.imshow('Hand Detection', frame)
        key = cv2.waitKey(1) & 0xFF
        # Nhấn ESC hoặc 'q' để dừng chương trình
        if key == 27 or key == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
