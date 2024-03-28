import hashlib
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def credentials():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    cred = ServiceAccountCredentials.from_json_keyfile_name('pbl2.json', scope)
    client = gspread.authorize(cred)
    sheet = client.open('2FA').worksheet("data")
    return sheet


def login(email, pwd, sheet):
    auth = pwd.encode()
    auth_hash = hashlib.md5(auth).hexdigest()
    records = sheet.get_all_records()
    for record in records:
        if record['Email'] == email and record['Password'] == auth_hash:
            st.success("Logged in Successfully!")
            return
    st.error("Login Failed!")

def gui():
    sheet1 = credentials()
    st.sidebar.title("Choose your Action")
    st.title("Enhancing Two Factor Authentication")
    st.header("Login Page")
    st.divider()
    email = st.text_input("ID or Email Address", key="email_login")
    pwd = st.text_input("Password", key="password_login", type="password")
    login_button = st.button("Login :sunglasses:", help="Walk into Creativity", use_container_width=True)
    if login_button:
        login(email, pwd, sheet1)
    # st.divider()
    # st.subheader("Don't have an account?")
    # st.button("Sign Up Now", key="signup_button", on_click = st.switch_page("Registration"))
        

# Run the GUI
gui()
