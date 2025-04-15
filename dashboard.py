import streamlit as st


class Dashboard:
    def __init__(self):
        self.render()

    def render(self):
        # Set up the layout with header and sidebar styles
        self.setup_layout()

        # Render the main content
        self.render_main_content()

    def setup_layout(self):
        # Header section (Title and welcome message)
        st.markdown("""
            <style>
            /* Header Styles */
            .header {
                background-color: #001f3f;
                padding: 20px;
                text-align: center;
                color: white;
                border-radius: 10px;
            }
            .header h1 {
                margin: 0;
            }

            /* Sidebar Styles */
            .css-1d391kg {
                background-color: #002b4c; /* Dark blue background */
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-family: 'Arial', sans-serif;
            }

            .css-1d391kg .stSidebar > div {
                padding: 10px;
            }

            .css-1d391kg .stButton > button {
                background-color: #4CAF50; /* Green button */
                color: white;
                border-radius: 5px;
                border: none;
                width: 100%;
                height: 40px;
                font-size: 16px;
            }

            .css-1d391kg .stButton > button:hover {
                background-color: #45a049; /* Darker green on hover */
            }

            .sidebar-title {
                color: #4CAF50;
                font-size: 24px;
                margin-top: 20px;
            }

            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="header"><h1> Dashboard</h1></div>', unsafe_allow_html=True)

        # Sidebar section (Navigation or controls)
        sidebar = st.sidebar
        sidebar.markdown("<div class='sidebar-title'>Navigation</div>", unsafe_allow_html=True)

        # Sidebar buttons
        sidebar.button("Home")
        sidebar.button("User Management")
        sidebar.button("Analytics")
        sidebar.button("Settings")

    def render_main_content(self):
        # Main section with content
        st.markdown("<h2>Welcome to your Dashboard!</h2>", unsafe_allow_html=True)

