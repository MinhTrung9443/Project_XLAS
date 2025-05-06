import base64
import streamlit as st
from PIL import Image
import cv2
import numpy as np

st.balloons()

# Thêm ảnh nền
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
        unsafe_allow_html=True
    )

add_bg_from_local(r"images\bg_dt.avif")

# CSS cho sidebar và văn bản
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #eac0f0;
    }
    .red-text {
        color: red;
    }
</style>
""", unsafe_allow_html=True)

# Tải danh sách lớp
classes = None
with open(r"pages\modeldoituong\modelobject\object_detection_classes_yolov4.txt", 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Tải mô hình YOLOv4
try:
    if st.session_state.get("LoadModel", False):
        print('Đã load model')
    else:
        st.session_state["LoadModel"] = True
        st.session_state["Net"] = cv2.dnn.readNet(r'pages\modeldoituong\modelobject\yolov4.weights', r"pages\modeldoituong\modelobject\yolov4.cfg")
        print('Load model lần đầu')
except Exception as e:
    st.error(f"Lỗi khi tải mô hình: {e}")
    st.stop()

# Cấu hình backend và target
st.session_state["Net"].setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
st.session_state["Net"].setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
outNames = st.session_state["Net"].getUnconnectedOutLayersNames()

# Ngưỡng
confThreshold = 0.5
nmsThreshold = 0.4

# Hàm xử lý sau khi suy luận
def postprocess(frame, outs):
    frame = frame.copy()
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    def drawPred(classId, conf, left, top, right, bottom):
        # Vẽ khung bao quanh đối tượng
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0))

        label = '%.2f' % conf
        if classes:
            assert(classId < len(classes))
            label = '%s: %s' % (classes[classId], label)

        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        top = max(top, labelSize[1])
        cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        return label

    layerNames = st.session_state["Net"].getLayerNames()
    lastLayerId = st.session_state["Net"].getLayerId(layerNames[-1])
    lastLayer = st.session_state["Net"].getLayer(lastLayerId)

    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Non-Maximum Suppression
    if len(outNames) > 1 or lastLayer.type == 'Region' and 0 != cv2.dnn.DNN_BACKEND_OPENCV:
        indices = []
        classIds = np.array(classIds)
        boxes = np.array(boxes)
        confidences = np.array(confidences)
        unique_classes = set(classIds)
        for cl in unique_classes:
            class_indices = np.where(classIds == cl)[0]
            conf = confidences[class_indices]
            box = boxes[class_indices].tolist()
            nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
            nms_indices = nms_indices[:] if len(nms_indices) else []
            indices.extend(class_indices[nms_indices])
    else:
        indices = np.arange(0, len(classIds))

    # Danh sách kết quả nhận dạng
    detected_objects = []
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        label = drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
        detected_objects.append(label)

    return frame, detected_objects

# Giao diện chính
image_file = st.file_uploader("Tải lên ảnh", type=["bmp", "png", "jpg", "jpeg"])
if image_file is not None:
    image = Image.open(image_file)
    st.image(image, caption="Ảnh đã tải lên")

    # Chuyển sang định dạng cv2
    frame = np.array(image)
    if frame.shape[-1] == 3:  # Đảm bảo ảnh là RGB
        frame = frame[:, :, [2, 1, 0]]  # RGB -> BGR

    if st.button('Dự đoán'):
        try:
            # Chuẩn bị ảnh đầu vào
            inpWidth = 416
            inpHeight = 416
            blob = cv2.dnn.blobFromImage(frame, scalefactor=1/255.0, size=(inpWidth, inpHeight), swapRB=True, crop=False)

            # Suy luận
            st.session_state["Net"].setInput(blob)
            outs = st.session_state["Net"].forward(outNames)

            # Xử lý kết quả
            img, detected_objects = postprocess(frame, outs)

            # Hiển thị ảnh với kết quả nhận dạng
            st.image(img, caption="Ảnh với kết quả nhận dạng", channels="BGR")

            # Hiển thị danh sách đối tượng nhận dạng
            if detected_objects:
                st.write("<span style='color:white; font-size:30px;'>Danh sách đối tượng nhận dạng:</span>", unsafe_allow_html=True)
                for i, obj in enumerate(detected_objects):
                    st.write(f"<span style='color:white; font-size:20px;'>Đối tượng {i+1}: {obj}</span>", unsafe_allow_html=True)
            else:
                st.write("<span style='color:white; font-size:20px;'>Không tìm thấy đối tượng nào.</span>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Lỗi khi xử lý ảnh: {e}")