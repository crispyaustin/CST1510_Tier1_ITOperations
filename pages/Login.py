# pages/Login.py
import streamlit as st
from auth import authenticate, register_user

def main():
    st.title("Login")

    if "user" not in st.session_state:
        st.session_state.user = None

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.success("Login successful!")
            else:
                st.error("Invalid credentials")

    with col2:
        st.subheader("Register (creates local DB user)")
        r_user = st.text_input("New username", key="reg_user")
        r_pass = st.text_input("New password", type="password", key="reg_pass")
        role = st.selectbox("Role", ["it_analyst", "it_manager"])
        if st.button("Register"):
            register_user(r_user, r_pass, role)
            st.success("User registered. You can now login.")

if __name__ == "__main__":
    main()
