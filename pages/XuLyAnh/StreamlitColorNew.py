import streamlit as st
import cv2
import numpy as np
import Chuong3 as c3
import os
import base64
def main_Color():
    global file_uploaded
    st.subheader("Chương 3")
    file_uploaded = st.file_uploader("Open an Color Image", type=["jpg", "tif", "bmp", "gif", "png"])

    if file_uploaded is not None:
        # imgin = cv2.imdecode(np.fromstring(file_uploaded.read(), np.uint8), cv2.IMREAD_COLOR)
        # st.image(imgin, channels="BGR", caption="Input Image")

        # image = cv2.imdecode(np.fromstring(file_uploaded.read(), np.uint8), cv2.IMREAD_COLOR)
        # st.session_state.imgin(image, channels="BGR", caption="Input Image")

        # st.session_state.imgin = cv2.imdecode(np.fromstring(file_uploaded.read(), np.uint8), cv2.IMREAD_COLOR)
        # st.image(st.session_state.imgin, channels="BGR", caption="Input Image")
        imgin = cv2.imdecode(np.fromstring(file_uploaded.read(), np.uint8), cv2.IMREAD_COLOR)
        #st.image(imgin, channels="BGR", caption="Input Image")

        col1, col2= st.columns([3, 3])
        with col1:
            st.subheader("Input Image")
            st.image(imgin, channels="BGR", use_column_width=True)
        with col2:
            st.subheader("Output Image")

        st.subheader("Buttons")
        buttons_layout = st.columns(4)

        if buttons_layout[0].button("HistEqualColor"):
            st.session_state.imgout = c3.HistEqualColor(imgin)
            st.session_state.caption= "HistEqualColor Image"
            display_image_color(col2, st.session_state.imgout, "HistEqualColor Image")

        if buttons_layout[1].button("BoxFilter"):
            st.session_state.imgout = c3.BoxFilter(imgin)
            st.session_state.caption= "BoxFilter Image"
            display_image_color(col2, st.session_state.imgout, "BoxFilter Image")

        if buttons_layout[2].button("MyBoxFilter"):
            st.session_state.imgout = cv2.boxFilter(imgin, cv2.CV_8UC1, (21,21))
            st.session_state.caption= "BoxFilter Image"
            display_image_color(col2, st.session_state.imgout, "MyBoxFilter Image")
        if buttons_layout[0].button("Threshold"):
            st.session_state.imgout = c3.Threshold(imgin)
            st.session_state.caption= "Threshold Image"
            display_image_color(col2, st.session_state.imgout, "Threshold Image")

        if buttons_layout[1].button("MedianFilter"):
            st.session_state.imgout = cv2.medianBlur(imgin, 7)
            st.session_state.caption= "MedianFilter Image"
            display_image_color(col2, st.session_state.imgout, "MedianFilter Image")

        if buttons_layout[2].button("Sharpen"):
            st.session_state.imgout = c3.Sharpen(imgin)
            st.session_state.caption= "Sharpen Image"
            display_image_color(col2, st.session_state.imgout, "Sharpen Image")

        if buttons_layout[3].button("Gradient"):
            st.session_state.imgout = c3.Gradient(imgin)
            st.session_state.caption= "Gradient Image"
            display_image_color(col2, st.session_state.imgout, "Gradient Image")

    if st.sidebar.button("Download Image"):
        if st.session_state.imgout is not None:
            download(st.session_state.imgout,file_uploaded)
        else:
            st.sidebar.warning("Không có ảnh đầu ra để tải xuống.")

def download(image,file_uploaded):
    _, encoded_image = cv2.imencode('.jpg', image)
    image_bytes=encoded_image.tobytes()

    download_data = base64.b64encode(image_bytes).decode()
    input_filename = os.path.basename(file_uploaded.name)
    output_filename = f"{st.session_state.caption}"+"_"+os.path.splitext(input_filename)[0] +".jpg"
    href = f'<a href="data:image/jpeg;base64,{download_data}" download="{output_filename}">Tải xuống ảnh</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
def display_image_color(column, img, caption):
    column.image(img, caption, use_column_width=True,channels="BGR")
    
   
