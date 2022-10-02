import streamlit as st
import streamlit_authenticator as stauth
import database as db



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
        st.title(f"Welcome {name}")
        st.subheader("We need to set our smishing script here. User will upload employees phone number and click a button to launch attack.")
        authenticator.logout("Logout", "main")

