import streamlit as st
import streamlit_authenticator as stauth
import database as db
import os
from twilio.rest import Client
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv




def percentage_maker(count, link_column):
    percentage = float(((count / len(link_column)) * 100))
    return percentage

def piechart(str):
    data = pd.read_excel(str)

    # extracting OS and Risk column's data as two separate list
    link_column = (data['ClickedTheLink'].tolist())
    credential_column = (data['UsedCredential'].tolist())

    # setting initial values zero for counting
    click_count, credential_count, ignore_count, link_credential_both = 0, 0, 0, 0

    # Determining operating systems with loop and if-else statements
    for i in range(len(link_column)):
        link_determiner = link_column[i]
        credential_determiner = credential_column[i]
        if link_determiner == "YES":
            click_count += 1
        if link_determiner == "IGNORED":
            ignore_count += 1
        if credential_determiner == "YES":
            credential_count += 1
        if link_determiner == "YES" and credential_determiner == "YES":
            link_credential_both += 1

    # Testing the program by printing and calculating total row number.
    # Note: Remove the docstring for testing.

    # Creating first chart
    plt.figure(0)
    topic = ['Clicked The Link', 'Ignored SMS', 'Entered Credential', 'Both']
    size = [percentage_maker(click_count, link_column), percentage_maker(ignore_count, link_column),
            percentage_maker(credential_count, link_column), percentage_maker(link_credential_both, link_column)]

    labels = list(topic)

    colors = ['gold', 'lightgreen', 'lightskyblue', 'lightcoral']
    plt.pie(size, explode=(0.05, 0.05, 0.05, 0.05), labels=labels, colors=colors, autopct='%1.1f%%', shadow=False,
            startangle=140)
    plt.axis('equal')
    plt.legend()
    plt.savefig('Chart.png')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(plt.show())











def number_list(str):
    data = pd.read_excel(str)
    name_column = (data['Name'].tolist())
    global number_column
    number_column = (data['PhoneNumber'].tolist())
    st.write("Here is the list of extracted data:")
    for i in range(len(number_column)):
        table = """<table style="width:100%, border:1px solid black;">
      <tr width="70%">
        <td width="70%">{}</td>
        <td width="70%">{}</td>
      </tr>
      </table>"""
        st.markdown(table.format(name_column[i],number_column[i]), unsafe_allow_html=True)


def send_message():
    account_sid = st.secrets["account_sid"]
    auth_token = st.secrets["auth_token"]
    client = Client(account_sid, auth_token)
    for i in range(len(number_column)):
        st.write(number_column[i])
        message = client.messages.create(
            body="This is from astia",
            from_=st.secrets["twilio_number"],
            to=number_column[i]
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

    name, authentication_status, username = authenticator.login("Login", "sidebar")

    if authentication_status == False:
        st.error("Username/password is incorrect")

    if authentication_status == None:
        with st.sidebar:
            st.warning("Please enter your username and password or SignUp")

    if authentication_status:
        with st.sidebar:
            st.success(f"Welcome {name}. You can select each tab below for upload data and launching smishing")
        tab1, tab2, tab3 = st.tabs(["Upload Data", "Launch Attack", "Analytics Report"])
        with tab1:
            left_column, right_column = st.columns(2)
            with left_column:
                uploaded_file = st.file_uploader("Select a file contains employees name and phone number")
                if uploaded_file is not None:
                    st.success("Data Uploaded Successfully.\nGo to the next tab to launch the attack.")
                else:
                    st.warning("Case Sensetive: First column heading must be 'Name' \nand second column must be 'PhoneNumber'")



        with tab2:
            left_column, right_column = st.columns(2)
            with left_column:
                if uploaded_file is not None:
                    st.success("Ready to launch the attack!? Click the button and boom!!!")
                    number_list(uploaded_file)
                else:
                    st.error("Before clicking 'Launch Smishing' button, upload a file containing emplyoee name and phone number to launch the Smishing.")
                st.write("##")
                st.write("##")
                if st.button("Launch Smishing"):
                    send_message()
        with tab3:
            left_column, right_column = st.columns(2)
            with left_column:
                uploaded_file = st.file_uploader("Choose a file to see the Analytical Data")
                if uploaded_file is not None:
                    piechart(uploaded_file)
            with right_column:
                right_column.metric("Enterted Link", "70", "5%")
                right_column.metric("Entered Credential", "30", "-8%")
                right_column.metric("Ignored SMS", "20", "-4%")

        authenticator.logout("Logout", "sidebar")

