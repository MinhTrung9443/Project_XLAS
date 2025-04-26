import cv2 as cv
import numpy as np
import streamlit as st
from tensorflow import keras
from keras.models import load_model

# Streamlit UI setup
st.subheader('Nhận dạng loại rác')
FRAME_WINDOW = st.image([])

# Initialize webcam
cap = cv.VideoCapture(0)

# Session state for stop button
if 'stop' not in st.session_state:
    st.session_state.stop = False

# Stop button
press = st.button('Stop')
if press:
    if st.session_state.stop == False:
        st.session_state.stop = True
        cap.release()
    else:
        st.session_state.stop = False

print('Trang thai nhan Stop', st.session_state.stop)

# Load stop image
if 'frame_stop' not in st.session_state:
    frame_stop = cv.imread('stop.jpg')
    st.session_state.frame_stop = frame_stop
    print('Đã load stop.jpg')

if st.session_state.stop == True:
    FRAME_WINDOW.image(st.session_state.frame_stop, channels='BGR')
    st.stop()

# WasteClassifier class
class WasteClassifier:
    def __init__(self, model_path='best_model.h5', class_indices_path='class_indices.npy'):
        self.model = load_model(model_path)
        self.class_indices = np.load(class_indices_path, allow_pickle=True).item()
        self.class_names = {v: k for k, v in self.class_indices.items()}
        self.input_size = (224, 224)
    
    def preprocess_image(self, img):
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        img = cv.resize(img, self.input_size)
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict_image(self, img):
        processed_img = self.preprocess_image(img)
        preds = self.model.predict(processed_img, verbose=0)
        pred_class = np.argmax(preds)
        class_name = self.class_names[pred_class]
        confidence = float(preds[0][pred_class])
        return class_name, confidence

# Visualization function
def visualize(input, class_name, confidence, fps, thickness=2):
    # Draw rectangle around the frame (optional, to highlight the detection area)
    cv.rectangle(input, (50, 50), (input.shape[1]-50, input.shape[0]-50), (0, 255, 0), thickness)
    # Display class name and confidence
    cv.putText(input, f"Class: {class_name}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv.putText(input, f"Confidence: {confidence:.2%}", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    # Display FPS
    cv.putText(input, f'FPS: {fps:.2f}', (10, input.shape[0]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

if __name__ == '__main__':
    # Initialize classifier
    classifier = WasteClassifier(model_path='best_model.h5', class_indices_path='class_indices.npy')

    # Initialize FPS counter
    tm = cv.TickMeter()

    while True:
        if st.session_state.stop:
            break

        hasFrame, frame = cap.read()
        if not hasFrame:
            print('No frames grabbed!')
            break

        # Start FPS timer
        tm.start()

        # Predict waste class
        class_name, confidence = classifier.predict_image(frame)

        # Stop FPS timer
        tm.stop()

        # Visualize results
        visualize(frame, class_name, confidence, tm.getFPS())

        # Display frame in Streamlit
        FRAME_WINDOW.image(frame, channels='BGR')

    # Cleanup
    cap.release()
    cv.destroyAllWindows()