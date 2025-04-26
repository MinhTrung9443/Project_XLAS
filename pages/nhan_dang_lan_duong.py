import base64
import cv2
import numpy as np
import streamlit as st
import tempfile
import os


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
add_bg_from_local(r'images/landuong.jpg')
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #efffc9;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='color: white;'>Nhận dạng làn đường</h1>", unsafe_allow_html=True)
# html textColor = white
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50,150)
    return canny

def region_of_interest(image):
    height = image.shape[0] 
    polygons = np.array([[(200, height), (1100,height), (550,250)]])
    mask = np.zeros_like(image) 
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2,y2), (255, 0, 0), 10)
    return line_image

def make_coordinates(image, line_parameters):
    if line_parameters is None:
        return None
    points = []
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.001,0
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    draw_points(image, points)
    return np.array([x1, y1, x2, y2])

def draw_points(image, points):
    for point in points:
        cv2.circle(image, (point[0], point[1]), 5, (0, 255, 0), cv2.FILLED)

def average_slope_intercept(image, lines):
    if lines is None:
        return None
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average = np.average(left_fit, axis = 0)
    right_fit_average = np.average(right_fit, axis = 0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])

video_file_buffer = st.file_uploader("Upload an video", type=["mov", "mp4"])
if video_file_buffer is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tfile:
        tfile.write(video_file_buffer.read())
        temp_file_name = tfile.name

    cap = cv2.VideoCapture(temp_file_name)

    if cap.isOpened():
        stframe = st.empty()
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                canny_image = canny(frame)
                cropped_image = region_of_interest(canny_image)
                lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
                averaged_lines = average_slope_intercept(frame, lines)
                if averaged_lines is not None:
                    line_image = display_lines(frame, averaged_lines)
                    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
                else:
                    combo_image = frame
                stframe.image(combo_image, channels="BGR")
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        os.remove(temp_file_name)