import base64

import streamlit as st
from streamlit import html
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Final Project",
    page_icon="👋",
)
html('''
     <!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<style>
    @import url("https://fonts.googleapis.com/css?family=Sacramento");


    .container {
    background: transparent
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
body .container div {
    background: linear-gradient(45deg, rgba(10, 230, 175, 0) 0%, rgb(14, 241, 139) 35%, rgba(0, 0, 0, 0.87) 100%);
    width: 10px;
    height: 250px;
    position: relative;
    margin: 0 30px;
    transform-origin: center top;
    animation: ani 4s linear infinite;
}

body .container div span {
    position:absolute;
    width: 60px;
    height: 60px;
    background:rgb(0,255,153);
    bottom:0px;
    left:50%;
    transform: translateX(-50%);
    border-radius: 50%;
    box-shadow: 0px 0px 20px rgb(0, 255, 153), 0px 0px 50px rgb(0, 255, 153), 0px 0px 80px rgb(0, 255, 153),0px 0px 100px rgb(0, 255, 153);

}

h1 {
    color: #fff6a9;
    font-size: 5em;
    text-shadow: 
        0 0 5px #ffa500,
        0 0 15px #ffa500,
        0 0 20px #ffa500,
        0 0 40px #ffa500,
        0 0 60px #ff0000,
        0 0 10px #ffa500,
        0 0 98px #ff0000;
    font-family: "Sacramento";
    text-align: center;
    animation: blink 7s infinite;
    position: absolute;
    display: grid;
}

@keyframes blink {
    0%, 20%, 40%, 60%, 80%, 100% {
        color: #fff6a9;
        text-shadow: 
            0 0 5px #ffa500,
            0 0 15px #ffa500,
            0 0 20px #ffa500,
            0 0 40px #ffa500,
            0 0 60px #ff0000,
            0 0 10px #ffa500,
            0 0 98px #ff0000;
    }
    10%,30%, 50%, 70%, 90% {
        color: #fff6a9;
        text-shadow: 0 0 1px #726a5c,
        0 0 2px #000000,
        0 0 6px #ffa500,
        0 0 10px #ffa500,
        0 0 12px #000000,
        0 0 2px #ffa500,
        0 0 18px #f500b4;
    }
}

@keyframes ani {
    0%{
        transform:rotate(0deg);
    }
    25% {
        transform: rotate(50deg);
        filter: hue-rotate(340deg);
    }

    50% {
        transform: rotate(0deg);

    }

    75% {
        transform: rotate(-50deg);
    }

    100% {
        transform: rotate(0deg);
    }
    
}
body div.div1 {
    animation-delay: 2s;

}

body div.div2 {
    animation-delay: 3s;
}
body div.div3 {
    animation-delay: 1.3s;
}

body div.div4 {
    animation-delay: 4s;
}

body div.div5 {
    animation-delay: 3.2s;
}

body div.div6 {
    animation-delay: 1.8s;
}

</style>

<body>
    <div class="container">
    <div class="div1">
        <span></span>
    </div>
    <div class="div2">
        <span></span>
    </div>
    <div class="div3">
        <span></span>
    </div>
    <div class="div4">
        <span></span>
    </div>
    <div class="div5">
        <span></span>
    </div>
    <div class="div6">
        <span></span>
    </div>

    <h1>Welcome to the website of our team!</h1>
    </div>
</body>

</html>
     ''',height=300,width=777)


# st.write("<h1 style='font-size: 50px;color:purple'>Welcome to the website of our team!</h1>",
#          unsafe_allow_html=True)
st.sidebar.success("You can choose one of my projects above.")

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


add_bg_from_local('images/Home.jpg')
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #eac7ff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .red-text {
        color: red;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.balloons()
st.balloons()
st.balloons()

st.markdown(
    """
        <div class="red-text">
        Wishing everyone an enjoyable time!
        This is the website created by our group during the Digital Image Processing course guided by Mr. Trần Tiến Đức.
        You and your friends can select items from the left sidebar to view the content on digital image processing.
        </div>
        <p><b style="font-size: 40px;">Group Members:</b></p>
        <div>
        <h3>Student 1:</h3>
        <h4>- Full name: </h4>
        <h4>- Student code: </h4>
        <h4>- School name: HCMC University of Technology and Education</h4>
        </div>
        <div>
        <h3>Student 2:</h3>
        <h4>- Full name: </h4>
        <h4>- Student code: </h4>
        <h4>- School name: HCMC University of Technology and Education</h4>
        </div>
        <p><b style="font-size: 40px;">Contact:</b></p>
        <div>
        <p><b style="font-size: 20px;">Student 1:</b></p>
        <p>- Github: <a style="color:green" href=""></a></p>
        <p>- Facebook:<a style="color:green" href=""> </a></p>
        <p>- Email: <a style="color:green" href=""> </a></p>
        <p>- Phone: <a style="color:green" href=""></a></p>
        </div>
        <div>
        <p><b style="font-size: 20px;">Student 2:</b></p>
        <p>- Github: <a style="color:green" href=""></a></p>
        <p>- Facebook:<a style="color:green" href=""> </a></p>
        <p>- Email: <a style="color:green" href=""> </a></p>
        <p>- Phone: <a style="color:green" href=""></a></p>
        </div>
        <div>
        <h1>Teacher: Tran Tien Duc</h1>
        <p>- Email:<a style="color:green" href="ductt@hcmute.edu.vn"> ductt@hcmute.edu.vn</a></p>
        <p>- Phone:<a style="color:green" href="ductt@hcmute.edu.vn"> 0919622862</a></p>
        <p>- Github: <a style="color:green" href="https://github.com/TranTienDuc">https://github.com/TranTienDuc</a><p>
	</div>
    """,
    unsafe_allow_html=True
)
