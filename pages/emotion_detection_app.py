import streamlit as st
import cv2
import numpy as np
from tensorflow import keras
from keras.models import load_model
from PIL import Image

# Cấu hình trang
st.set_page_config(
    page_title="Emotion Detection",
    page_icon="😊",
    layout="wide"
)

# Load model và các thành phần cần thiết
@st.cache_resource
def load_emotion_model():
    model = load_model(r'pages\modelEmotion\best_model.h5')  # Thay bằng đường dẫn đến model của bạn
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
    return model, face_cascade, emotion_labels

model, face_cascade, emotion_labels = load_emotion_model()

# Hàm nhận diện cảm xúc
def detect_emotion(img):
    # Chuyển đổi ảnh sang grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Phát hiện khuôn mặt
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    results = []
    for (x, y, w, h) in faces:
        # Cắt vùng khuôn mặt
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)
        
        if np.sum([roi_gray]) != 0:
            # Chuẩn bị ảnh để dự đoán
            roi = roi_gray.astype('float')/255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)
            
            # Dự đoán cảm xúc
            preds = model.predict(roi)[0]
            emotion_idx = np.argmax(preds)
            emotion = emotion_labels[emotion_idx]
            confidence = preds[emotion_idx]
            
            # Vẽ kết quả lên ảnh
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            label = f"{emotion} ({confidence:.2f})"
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            results.append({
                "emotion": emotion,
                "confidence": float(confidence),
                "box": [int(x), int(y), int(w), int(h)]
            })
    
    return img, results

# Giao diện chính
def main():
    st.title("🎭 Nhận diện Cảm xúc Khuôn mặt")
    st.markdown("---")
    
    option = st.radio("Chọn chế độ:", ("Webcam", "Tải ảnh lên"))
    
    if option == "Webcam":
        st.subheader("Nhận diện từ Webcam")
        st.write("Nhấn nút bên dưới để bắt đầu sử dụng webcam")
        
        run = st.checkbox("Bật Webcam")
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0)
        
        while run:
            _, frame = camera.read()
            if frame is None:
                continue
                
            # Chuyển đổi màu và nhận diện
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            processed_frame, _ = detect_emotion(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Hiển thị ảnh
            FRAME_WINDOW.image(processed_frame)
        
        camera.release()
        
    else:
        st.subheader("Nhận diện từ ảnh tải lên")
        uploaded_file = st.file_uploader("Chọn một ảnh...", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            # Đọc ảnh
            image = Image.open(uploaded_file)
            img_array = np.array(image)
            
            # Nhận diện cảm xúc
            processed_img, results = detect_emotion(cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
            
            # Hiển thị kết quả
            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Ảnh gốc", use_column_width=True)
            with col2:
                st.image(processed_img, caption="Ảnh đã xử lý", use_column_width=True)
            
            if results:
                st.subheader("Kết quả nhận diện")
                for i, result in enumerate(results, 1):
                    st.write(f"**Khuôn mặt {i}:**")
                    st.write(f"- Cảm xúc: {result['emotion']}")
                    st.write(f"- Độ chính xác: {result['confidence']:.2%}")
                    st.write(f"- Vị trí: (x={result['box'][0]}, y={result['box'][1]}, w={result['box'][2]}, h={result['box'][3]})")
            else:
                st.warning("Không tìm thấy khuôn mặt trong ảnh!")

if __name__ == "__main__":
    main()