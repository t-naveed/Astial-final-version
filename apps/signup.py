import streamlit as st
import streamlit_authenticator as stauth
import database as db


def app():
    st.write("##")
    st.subheader("Create an Account")
    names = []
    usernames = []
    passwords = []
    full_name = st.text_input('Full name')
    names.append(full_name)
    usr_name = st.text_input('Username')
    usernames.append(usr_name)
    set_passwd = st.text_input('Password', type='password')
    passwords.append(set_passwd)

    hashed_passwords = stauth.Hasher(passwords).generate()
    users = db.fetch_all_users()
    usernames_from_db = [user["key"] for user in users]
    if names[0] == "" or usernames[0] == "" or passwords[0] == "":
        st.warning("Must fill all the fields")
    for i in range(len(usernames_from_db)):
        if (usernames_from_db[i]) == (usernames[0]):
            st.error("Username already exist")

    st.write("##")
    if st.button('SignUp'):
        for (username, name, hashed_passwords) in zip(usernames, names, hashed_passwords):
            db.insert_user(username, name, hashed_passwords)
            st.success("You have successfully created an account.Go to the Login Menu to login")

