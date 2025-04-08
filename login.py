import streamlit as st
import sqlite3
import hashlib


conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)''')
conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def check_login(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
    return c.fetchone() is not None


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("👤 User Login")

if not st.session_state.logged_in:
    menu = st.selectbox("Menu", ["Login", "Create Account"])

    if menu == "Create Account":
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        if st.button("Sign Up"):
            if new_user and new_pass:
                if register_user(new_user, new_pass):
                    st.success("Account created successfully!")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Please fill in both fields.")

    elif menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_login(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

else:
    st.switch_page("pages/app.py")
