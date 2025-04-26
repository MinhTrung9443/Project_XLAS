import base64
import streamlit as st
from cvzone.HandTrackingModule import HandDetector
import cv2 as cv
import mediapipe as mp
st.subheader('Nhận dạng ban tay')
st.balloons()
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


# add_bg_from_local(r"images\bg_ban_tay.jpg")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #eac123;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .red-text {
        color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)








FRAME_WINDOW = st.image([])
cap = cv.VideoCapture(0)
if 'stop' not in st.session_state:
    st.session_state.stop = False
    stop = False

press = st.button('Stop')
if press:
    if st.session_state.stop == False:
        st.session_state.stop = True
        cap.release()
    else:
        st.session_state.stop = False

print('Trang thai nhan Stop', st.session_state.stop)


if 'frame_stop' not in st.session_state:
    frame_stop = cv.imread(r"pages\model\stop.jpg")
    st.session_state.frame_stop = frame_stop
    print('Đã load stop.jpg')

    

if st.session_state.stop == True:
    FRAME_WINDOW.image(st.session_state.frame_stop, channels='BGR')


if __name__ == '__main__':
    detector = HandDetector(maxHands=1, detectionCon=0.8)
    while True:
        if st.session_state.stop == True:
            st.session_state.frame_stop = cv.imread(r'pages\model\stop.jpg')
            break
        success, img = cap.read()
        hands, img = detector.findHands(img)
        FRAME_WINDOW.image(img, channels='BGR')
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()
    