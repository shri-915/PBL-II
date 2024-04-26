import streamlit as st
import cv2
import hashlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode

class ScreenshotVideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        return frame

def credentials():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred = ServiceAccountCredentials.from_json_keyfile_name('pbl2.json', scope)
    client = gspread.authorize(cred)
    sheet = client.open('2FA').worksheet("data")
    return sheet

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return len(faces) > 0

def signup():
    sheet = credentials()
    st.header("Registration Page")
    first_name = st.text_input("First Name", key="fn_signup")
    last_name = st.text_input("Last Name", key="fn_signup")
    email = st.text_input("EmailID", key="email_signup", help="Your preferred email ID")
    phone = st.text_input("Phone Number", key="phone_signup")
    if len(phone) != 10:
        st.warning("Please enter a 10-digit phone number.")
    # Display the webcam and capture button
    webrtc_ctx = webrtc_streamer(
        key="screenshot",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=ScreenshotVideoTransformer,
        async_transform=True,
    )
    if webrtc_ctx.video_transformer:
        capture_button = st.button("Capture Photo")
        if capture_button:
            image_data = webrtc_ctx.video_transformer.frame
            image = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
            if detect_faces(image):
                st.success("Face detected!")
                pwd = st.text_input("Password", key="password_signup", type="password")
                conf_pwd = st.text_input("Confirm password:", key="confirm_password_signup", type="password")
                confirm_button = st.button("Confirm Password", use_container_width=True)
                if confirm_button:
                    if conf_pwd == pwd:
                        enc = conf_pwd.encode()
                        hash1 = hashlib.md5(enc).hexdigest()
                        st.success("You have registered successfully!")
                        row = [first_name, last_name, email, phone, hash1]
                        sheet.append_row(row)
                        st.divider()
                        st.link_button("Go Back to Login Page", "https://test2fa.streamlit.app/", use_container_width=True)
                    else:
                        st.warning("Password is not the same as above!")
            else:
                st.warning("No face detected!")

signup()
