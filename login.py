import streamlit as st

class LoginPage:
    def __init__(self):
        self.render()

    def render(self):
        st.title("SeekBytes")
        with st.form(key='login_form', clear_on_submit=True):
            st.markdown("<h3 style='text-align: center;'>Please Log In</h3>", unsafe_allow_html=True)

            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type='password', placeholder="Enter your password")
            submit_button = st.form_submit_button(label='Log In')

            if submit_button:
                if self.authenticate(username, password):
                    st.session_state.logged_in = True
                    st.rerun()  # ✅ Corrected here
                else:
                    st.error("Invalid credentials. Please try again.")

    def authenticate(self, username, password):
        return username == "admin" and password == "password123"
