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

def signup():
    sheet = credentials()
    st.header("Registration Page")
    email = st.text_input("ID or Email Address", key="email_signup", help="Your preferred Username")
    phone = st.text_input("Phone Number", key="phone_signup")
    if len(phone) != 10:
        st.warning("Please enter a 10-digit phone number.")
    pwd = st.text_input("Password", key="password_signup", type="password")
    conf_pwd = st.text_input("Confirm password:", key="confirm_password_signup", type="password")
    confirm_button = st.button("Confirm Password", use_container_width=True)
    if confirm_button:
        if conf_pwd == pwd:
            enc = conf_pwd.encode()
            hash1 = hashlib.md5(enc).hexdigest()
            st.success("You have registered successfully!")
            row = [email, hash1, phone]
            sheet.append_row(row)
        else:
            st.warning("Password is not the same as above!")


signup()