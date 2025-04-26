import streamlit as st
import numpy as np
from PIL import Image
import cv2
import base64

import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator

st.balloons()
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
        }}
        .title-text {{
            font-size: 24px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #efffc9;
    }
</style>
""", unsafe_allow_html=True)

# Add background image
add_bg_from_local(r'images\NhanDangTraiCay.jpg')  

st.markdown("<h1 class='title-text'>Nhận dạng trái cây</h1>", unsafe_allow_html=True)
model = YOLO(r"pages\modeltraicay\best.onnx", task='detect')
try:
    if st.session_state["LoadModel"] == True:
        print('Đã load model rồi')
except:
    st.session_state["LoadModel"] = True
    st.session_state["Net"] = cv2.dnn.readNet(r"pages\modeltraicay\best.onnx")
    print(st.session_state["LoadModel"])
    print('Load model lần đầu') 

# Constants.
INPUT_WIDTH = 640
INPUT_HEIGHT = 640
SCORE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.45
CONFIDENCE_THRESHOLD = 0.45

# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
THICKNESS = 1

# Colors.
BLACK = (0, 0, 0)
BLUE = (255, 178, 50)
YELLOW = (0, 255, 255)

def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim, baseline = text_size[0], text_size[1]
    cv2.rectangle(im, (x, y), (x + dim[0], y + dim[1] + baseline), BLACK, cv2.FILLED)
    cv2.putText(im, label, (x, y + dim[1]), FONT_FACE, FONT_SCALE, YELLOW, THICKNESS, cv2.LINE_AA)

def pre_process(input_image, net):
    blob = cv2.dnn.blobFromImage(input_image, 1/255, (INPUT_WIDTH, INPUT_HEIGHT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    outputs = net.forward(net.getUnconnectedOutLayersNames())
    return outputs

def post_process(input_image, outputs):
    names = model.names
    outputs = input_image.copy()
    annotator = Annotator(outputs)
    results  = model.predict(input_image, conf = 0.5, verbose=False)

    boxes = results[0].boxes.xyxy.cpu()
    clss = results[0].boxes.cls.cpu().tolist()
    confs = results[0].boxes.conf.tolist()
    for box, cls, conf in zip(boxes, clss, confs):
        annotator.box_label(box,label = names[int(cls)] + ' %4.2f' % conf , txt_color=(255,0,0), color=(255,255,255))
    return outputs

img_file_buffer = st.file_uploader("Upload an image", type=["bmp", "png", "jpg", "jpeg"])
col1,colmid,col2 = st.columns(3)
if img_file_buffer is not None:
    image = Image.open(img_file_buffer)
    st.image(image)
    # Chuyển sang cv2 để dùng sau này
    frame = np.array(image)
    frame = frame[:, :, [2, 1, 0]] # BGR -> RGB    
    if st.button('Predict'):
        # Process image.
        detections = pre_process(frame, st.session_state["Net"])
        img = post_process(frame.copy(), detections)
        st.image(img, channels="BGR")

