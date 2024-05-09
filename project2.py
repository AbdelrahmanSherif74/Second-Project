import cv2
import mediapipe as mp

# تهيئة مكتبة Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# قاموس لترجمة حركات اليد إلى كلمات بسيطة باللغة الإنجليزية
sign_language_dict = {
    "بداية": "Start",
    "نهاية": "End",
    "سهل": "Easy",
    "صعب": "Hard",
    "مرحبا": "Hello",
    "هيا": "let'go",
    "كيف حالك": "How are you",
    "غير معروف": "Unknown"
}

# دالة لتحويل حركات اليد إلى كلمات بسيطة باللغة الإنجليزية
def translate_hand_gesture(hand_landmarks):
    # الحصول على مواقع الأصابع
    thumb_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
    thumb_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    index_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    index_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    middle_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
    middle_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ring_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x
    ring_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
    pinky_tip_x = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x
    pinky_tip_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y

    # حركة البداية: إذا كانت نهاية الإبهام تقع أعلى من نهاية السبابة وأعلى من نهاية السبابة الوسطى وأعلى من نهاية السبابة الرابعة وأعلى من نهاية الخنصر
    if thumb_tip_y < index_tip_y and thumb_tip_y < middle_tip_y and thumb_tip_y < ring_tip_y and thumb_tip_y < pinky_tip_y:
        return "بداية"

    # حركة النهاية: إذا كانت نهاية الإبهام تقع أقل من نهاية السبابة وأقل من نهاية السبابة الوسطى وأقل من نهاية السبابة الرابعة وأقل من نهاية الخنصر
    elif thumb_tip_y > index_tip_y and thumb_tip_y > middle_tip_y and thumb_tip_y > ring_tip_y and thumb_tip_y > pinky_tip_y:
        return "نهاية"

    # حركة السهل: إذا كانت نهاية السبابة تقع أعلى من نهاية الإبهام وأعلى من نهاية السبابة الوسطى وأعلى من نهاية السبابة الرابعة وأعلى من نهاية الخنصر
    elif index_tip_y < thumb_tip_y and index_tip_y < middle_tip_y and index_tip_y < ring_tip_y and index_tip_y < pinky_tip_y:
        return "سهل"

    # حركة الصعب: إذا كانت نهاية السبابة تقع أقل من نهاية الإبهام وأقل من نهاية السبابة الوسطى وأقل من نهاية السبابة الرابعة وأقل من نهاية الخنصر
    elif index_tip_y > thumb_tip_y and index_tip_y > middle_tip_y and index_tip_y > ring_tip_y and index_tip_y > pinky_tip_y:
        return "صعب"

    # حركة الوسطى: إذا كانت نهاية السبابة الوسطى أقل من نهاية السبابة وأقل من نهاية السبابة الوسطى وأقل من نهاية السبابة الرابعة وأقل من نهاية الخنصر
    elif middle_tip_y > index_tip_y and middle_tip_y > thumb_tip_y and middle_tip_y > ring_tip_y and middle_tip_y > pinky_tip_y:
        return "مرحبا"

    # حركة البينكي: إذا كانت نهاية البينكي أقل من نهاية السبابة ونهاية الإبهام ونهاية السبابة الوسطى ونهاية السبابة الرابعة
    elif pinky_tip_y > index_tip_y and pinky_tip_y > thumb_tip_y and pinky_tip_y > middle_tip_y and pinky_tip_y > ring_tip_y:
        return "هيا"

    # حركة الدلال: إذا كانت نهاية السبابة تقع تحت الإبهام وتحت السبابة الوسطى وتحت السبابة الرابعة وتحت الخنصر
    elif index_tip_y < thumb_tip_y and index_tip_y < middle_tip_y and index_tip_y < ring_tip_y and index_tip_y < pinky_tip_y:
        return "كيف حالك"
    # حركة غير معروفة
    else:
        return "غير معروف"

# الدالة الرئيسية
def main():
    # فتح الكاميرا
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        # قراءة الإطار
        ret, frame = cap.read()
        if not ret:
            break

        # تحويل الإطار إلى RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # تحليل اليد في الإطار
        results = hands.process(frame_rgb)

        # عرض نتائج التحليل
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # تحويل حركات اليد إلى كلمات بسيطة
                translated_text = translate_hand_gesture(hand_landmarks)
                # عرض الكلمة المترجمة
                cv2.putText(frame, sign_language_dict.get(translated_text, ""), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # عرض الإطار
        cv2.imshow('Hand Sign Language Translator', frame)

        # انتظار الضغط على مفتاح 'q' للخروج
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # تحرير الموارد
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
