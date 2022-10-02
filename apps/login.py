import streamlit as st
import streamlit_authenticator as stauth
import database as db
import os
from twilio.rest import Client
from dotenv import load_dotenv

def send_message():
    account_sid = st.secrets["account_sid"]
    auth_token = st.secrets["auth_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="This is from astia",
        from_=st.secrets["twilio_number"],
        to='+18622357825'
    )
    st.write(message.body)
def app():
    # --- USER AUTHENTICATION ---
    users = db.fetch_all_users()
    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]

    authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
                                        "sales_dashboard", "abcdef", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        st.warning("Please enter your username and password or SignUp")

    if authentication_status:
        st.subheader(f"Welcome {name}. You can select each tab below for upload data and launching smishing")
        tab1, tab2= st.tabs(["Upload Data", "Launch Attack"])
        with tab1:
            uploaded_file = st.file_uploader("Select a file contains employees name and phone number")


        with tab2:
            if st.button("Launch Smishing"):
                send_message()


        authenticator.logout("Logout", "main")

