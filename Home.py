import base64
import streamlit as st
from streamlit.components.v1 import html # Use this explicitly if needed, but st.html is often sufficient
st.set_page_config(
    page_title="Final Project",
    page_icon="✨",
    layout="wide" # Use wide layout for better spacing
)
try:
    st.sidebar.image("images/logo_hcmute.png", use_container_width=True)
except FileNotFoundError:
    st.sidebar.error("Không tìm thấy file logo. Vui lòng kiểm tra đường dẫn.")
except Exception as e:
    st.sidebar.error(f"Lỗi khi tải logo: {e}")

# --- START: Modified HTML/CSS Block (Kept mostly same as last version, added bottom margin) ---
html_content_new = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>
    <link href="https://fonts.googleapis.com/css2?family=Sacramento&display=swap" rel="stylesheet">
    <style>
        body {
            margin: 0;
            padding: 0;
        }

        .container {
            background: transparent;
            height: 300px; /* Fixed height to match st.html height */
            width: 95%; max-width: 777px;
            display: flex;
            justify-content: center; /* Center horizontally */
            align-items: center; /* Center vertically */
            flex-direction: row; /* Arrange children in a row */
            position: relative; /* Needed for absolute positioning of h1 */
            margin: 20px auto; /* Added top/bottom margin (20px) and auto left/right for centering */
            overflow: hidden; /* Hide anything spilling out */
        }

        .container div {
            background: rgba(255, 255, 255, 0.2);
            width: 2px;
            height: 150px;
            position: relative;
            margin: 0 10px;
            transform-origin: center bottom;
            animation: subtleSway 6s ease-in-out infinite;
            border-radius: 2px;
            z-index: 0;
        }

        .container div span {
            position: absolute;
            width: 10px;
            height: 10px;
            background: rgba(255, 255, 255, 0.8);
            bottom: 0px;
            left: 50%;
            transform: translateX(-50%);
            border-radius: 50%;
            box-shadow: none;
            animation: subtleFloat 6s ease-in-out infinite;
            animation-delay: inherit;
        }

        h1 {
            color: #333333;
            font-size: 3em;
            text-shadow:
                0 0 10px rgba(255, 255, 255, 0.5),
                0 0 20px rgba(255, 255, 255, 0.3);
            font-family: "Sacramento", cursive;
            text-align: center;
            animation: none;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            white-space: nowrap;
            z-index: 1;
             /* Adjust font size for smaller screens if needed */
            @media (max-width: 768px) {
                font-size: 2em;
                white-space: normal;
                width: 90%;
            }
             @media (max-width: 480px) {
                font-size: 1.5em;
            }
        }

        @keyframes subtleSway {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(2deg); }
        }

        @keyframes subtleFloat {
            0%, 100% { transform: translateX(-50%) translateY(0); }
            50% { transform: translateX(-50%) translateY(-10px); }
        }

        .container div.div1 { animation-delay: 0.5s; }
        .container div.div2 { animation-delay: 1.2s; }
        .container div.div3 { animation-delay: 0.8s; }
        .container div.div4 { animation-delay: 1.5s; }
        .container div.div5 { animation-delay: 1s; }
        .container div.div6 { animation-delay: 1.7s; }

    </style>
</head>
<body>
    <div class="container">
        <div class="div1"><span></span></div>
        <div class="div2"><span></span></div>
        <div class="div3"><span></span></div>
        <div class="div4"><span></span></div>
        <div class="div5"><span></span></div>
        <div class="div6"><span></span></div>
        <h1>Welcome to the website of our team!</h1>
    </div>
</body>
</html>
"""

# Display the HTML banner
html(html_content_new, height=340, width=777) # Increased height slightly to account for new margin


# Function to add background image
def add_bg_from_local(image_file):
    """Adds a background image from a local file."""
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
            f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Background image not found at '{image_file}'. Please check the path.")
    except Exception as e:
        st.error(f"An error occurred while setting the background image: {e}")


# Call the background function
add_bg_from_local('images/Home.jpg')

# Sidebar styling
st.sidebar.success("You can choose one of my projects above.") # Keep the sidebar success message
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #e0e7ef; /* Purple */
    }
    /* Optional: Style sidebar links/text color if needed */
    /*
    [data-testid=stSidebar] .st-emotion-cache-vk3up2 { /* Target the text container */
        color: #333; /* Darken sidebar text */
    }
    */
</style>
""", unsafe_allow_html=True)


# Custom CSS for text and spacing in the main content markdown
st.markdown(
    """
    <style>
    /* Style for the 'Wishing everyone...' text */
    .intro-text {
        /* color: red; /* Original red color */
        color: #333333; /* Example: Dark Purple */
        /* color: #006400; /* Example: Dark Green */
        font-weight: bold;
        margin-top: 30px; /* Add space above this text */
        margin-bottom: 20px; /* Add space below this text */
        font-size: 1.1em; /* Slightly larger font */
    }

    /* Add spacing around the headings and member boxes */
    .member-section h3 {
        margin-top: 15px; /* Space above member name */
        margin-bottom: 5px; /* Space below member name */
    }
    .member-section ul {
        margin-top: 5px; /* Space above list */
        padding-bottom: 0; /* Remove default bottom padding */
    }
    .member-section li {
        margin-bottom: 5px; /* Space between list items */
    }
    .teacher-section h3 {
         margin-top: 15px;
         margin-bottom: 5px;
    }
     .teacher-section ul {
        margin-top: 5px;
        padding-bottom: 0;
    }
     .teacher-section li {
        margin-bottom: 5px;
    }

    /* Target the main markdown container to add overall spacing */
    /* This class name might change in future Streamlit versions */
    /* Safer ways involve wrapping markdown content in st.container() or adding more specific CSS classes */
    .st-emotion-cache-uczq2p { /* Adjust padding-top if needed, depends on banner height */
       /* padding-top: 20px; */ /* Removed this as margin on .container and .intro-text handle spacing */
    }


    </style>
    """,
    unsafe_allow_html=True
)

# Balloons (reduced to 1 call for less clutter)
st.spinner()
# st.balloons() # Comment out or remove these two lines
# st.balloons()

# Markdown block with introduction and team information
# Added a class 'intro-text' to the wishing div for styling
st.markdown(
"""
<div class="intro-text">
Wishing everyone an enjoyable time!
This is the website created by our group during the Digital Image Processing course guided by Mr. Trần Tiến Đức.
You and your friends can select items from the left sidebar to view the content on digital image processing.
</div>

<p><b style="font-size: 40px;">Group Members:</b></p>

<div class="member-section" style="background-color:#f0f8ff; border-radius: 15px; padding: 20px; margin-bottom: 15px;">
<h3>Student 1: Phạm Minh Trung</h3>
<ul>
<li><b>Student code:</b> 22110446</li>
<li><b>School:</b> HCMC University of Technology and Education</li>
<li><b>GitHub:</b> <a style="color:green" href="https://github.com/MinhTrung9443" target="_blank">MinhTrung9443</a></li>
<li><b>Email:</b> <a style="color:green" href="mailto:minhtrungbttv@gmail.com">minhtrungbttv@gmail.com</a></li>
<li><b>Phone:</b> 0902137976</li>
</ul>
</div>

<div class="member-section" style="background-color:#f0f8ff; border-radius: 15px; padding: 20px; margin-bottom: 15px;">
<h3>Student 2: Nguyễn Thị Hồng Nhung</h3>
<ul>
<li><b>Student code:</b> 22110391</li>
<li><b>School:</b> HCMC University of Technology and Education</li>
<li><b>GitHub:</b> <a style="color:green" href="https://github.com/hnhung31" target="_blank">hnhung31</a></li>
<li><b>Email:</b> <a style="color:green" href="mailto:22110391@student.hcmute.edu.vn">22110391@student.hcmute.edu.vn</a></li>
<li><b>Phone:</b> 0325426186</li>
</ul>
</div>

<p><b style="font-size: 40px;">Teacher:</b></p>
<div class="teacher-section" style="background-color:#e0ffe0; border-radius: 15px; padding: 20px;">
<h3>Trần Tiến Đức</h3>
<ul>
<li><b>Email:</b> <a style="color:green" href="mailto:ductt@hcmute.edu.vn">ductt@hcmute.edu.vn</a></li>
<li><b>Phone:</b> 0919622862</li>
<li><b>GitHub:</b> <a style="color:green" href="https://github.com/TranTienDuc" target="_blank">TranTienDuc</a></li>
</ul>
</div>
""",
unsafe_allow_html=True
)