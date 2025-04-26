import streamlit as st
import cv2
import imutils
import numpy as np
import base64
st.balloons()

def process_image(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Threshold the image
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    
    # Draw contours and centers
    for c in contours:
        # Compute the center of the contour
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Draw the contour and center
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    return image

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
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():

    st.write(f"<span style='color:purple; font-size:50px;font-weight:bold;'>Tìm đường bao và điểm chính giữa shape</span>", unsafe_allow_html=True)
    with open("images/testduongbao.rar", "rb") as fp:
            btn = st.download_button(
                label="Download ảnh để test",
                data=fp,
                file_name="testduongbao.rar",
                mime="application/zip"
        )
    st.markdown("""
    <style>
        [data-testid=stSidebar] {{
            background-color: #efffc9;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Add background image
    add_bg_from_local(r'images\bgduongbaovadiemchinhgiua.jpg')  

    # Add title with smaller font size


    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
    col1, colmid,col2 = st.columns(3)

    if uploaded_file is not None:
        
        # Convert the file to an OpenCV image
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, 1)
        with col1:
            st.image(image, channels="BGR", caption="Original Image")
        # Process the image
        processed_image = process_image(image)
        
        # Display the processed image
        with colmid:
            st.image(r"images\muitendo.png", channels="BGR")
        with col2:
            st.image(processed_image, channels="BGR", caption="Processed Image")

if __name__ == "__main__":
    main()
