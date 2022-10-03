import os
from deta import Deta
from dotenv import load_dotenv



DETA_KEY = st.secrets["key"]

deta = Deta(DETA_KEY)

db = deta.Base("user_db")

def insert_user(username, name, password):
    return db.put({"key": username, "name": name, "password": password})
#insert_user("naveed", "tasin naveed", "xxx")

def fetch_all_users():
    res = db.fetch()
    return res.items



def get_user(username):
    return db.get(username)

