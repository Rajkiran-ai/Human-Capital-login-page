import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import io
import PyPDF2
from docx import Document
import re
import json
import csv
from openpyxl import Workbook


class Dashboard:
    def __init__(self):
        # Set up language selector in sidebar
        self.languages = {
            'English': 'eng',
            'Spanish': 'spa',
            'French': 'fra',
            'German': 'deu',
            'Chinese': 'chi_sim'
        }
        # Create a container for the language selector in the top right
        with st.container():
            col1, col2, col3 = st.columns([6, 2, 2])
            with col3:
                self.selected_lang = st.selectbox(
                    'Select Language',
                    list(self.languages.keys()),
                    index=0
                )

    def extract_text_from_pdf(self, file):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def extract_text_from_docx(self, file):
        doc = Document(io.BytesIO(file.read()))
        text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        return text

    def extract_text_from_image(self, file):
        image = Image.open(file)
        text = pytesseract.image_to_string(image, lang=self.languages[self.selected_lang])
        return text

    def parse_resume_text(self, text):
        data = {
            'name': '',
            'email': '',
            'phone': '',
            'skills': set(),
            'experience': [],
            'education': []
        }

        # Extract email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            data['email'] = email_match.group(0)

        # Extract phone number
        phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            data['phone'] = phone_match.group(0)

        # Extract name (assuming it's in the first two lines)
        lines = text.split('\n')
        for line in lines[:2]:
            if line.strip() and not re.search(email_pattern, line) and not re.search(phone_pattern, line):
                data['name'] = line.strip()
                break

        # Extract skills (common keywords)
        skills_keywords = ['python', 'java', 'javascript', 'html', 'css', 'sql', 'react', 'angular',
                          'node.js', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'agile', 'scrum']
        for skill in skills_keywords:
            if re.search(r'\b' + skill + r'\b', text.lower()):
                data['skills'].add(skill.title())

        # Extract experience (looking for date patterns)
        experience_pattern = r'\b\d{4}[-–]\d{4}|\d{4}[-–]present\b'
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if re.search(experience_pattern, line.lower()):
                if i < len(lines) - 1:
                    data['experience'].append(line.strip() + ' ' + lines[i+1].strip())

        # Extract education
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college']
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in education_keywords):
                data['education'].append(line.strip())

        return data

    def download_data(self, data):
        st.write('Download parsed data in your preferred format:')
        col1, col2, col3, col4 = st.columns(4)

        # JSON download
        with col1:
            json_str = json.dumps(data, default=lambda x: list(x) if isinstance(x, set) else x)
            st.download_button(
                label='JSON',
                data=json_str,
                file_name='resume_data.json',
                mime='application/json'
            )

        # CSV download
        with col2:
            csv_data = io.StringIO()
            writer = csv.writer(csv_data)
            writer.writerow(['Field', 'Value'])
            for key, value in data.items():
                if isinstance(value, (list, set)):
                    value = ', '.join(str(v) for v in value)
                writer.writerow([key, value])
            st.download_button(
                label='CSV',
                data=csv_data.getvalue(),
                file_name='resume_data.csv',
                mime='text/csv'
            )

        # Excel download
        with col3:
            wb = Workbook()
            ws = wb.active
            ws.append(['Field', 'Value'])
            for key, value in data.items():
                if isinstance(value, (list, set)):
                    value = ', '.join(str(v) for v in value)
                ws.append([key, value])
            excel_data = io.BytesIO()
            wb.save(excel_data)
            excel_data.seek(0)
            st.download_button(
                label='Excel',
                data=excel_data,
                file_name='resume_data.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        # TXT download
        with col4:
            txt_content = '\n'.join([f'{key}: {value}' for key, value in data.items()])
            st.download_button(
                label='TXT',
                data=txt_content,
                file_name='resume_data.txt',
                mime='text/plain'
            )

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

        # Language selector in the top right
        st.markdown(
            "<div style='position: fixed; top: 10px; right: 10px;'>"
            "<select style='padding: 5px; border-radius: 5px;'>"
            "<option value='en'>English</option>"
            "<option value='es'>Español</option>"
            "<option value='fr'>Français</option>"
            "<option value='de'>Deutsch</option>"
            "</select>"
            "</div>",
            unsafe_allow_html=True
        )

        st.markdown('<div class="header"><h1>Human Resource Management</h1></div>', unsafe_allow_html=True)

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
        
        # Add 10 second delay
        import time
        time.sleep(5)
        
        # Search bar and button in one row
        st.markdown(
            "<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 20px;'>"
            "<div style='flex: 1;'>"
            "<input type='text' placeholder='Enter your search query' style='width: 100%; padding: 8px; border-radius: 5px; border: 1px solid #ccc;'>"
            "</div>"
            "<button style='padding: 8px 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;'>"
            "Search"
            "</button>"
            "</div>",
            unsafe_allow_html=True
        )
        
        # File upload section for resume
        st.markdown("<h3>Upload Resume</h3>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload Resume",
            type=['pdf', 'docx', 'jpg', 'png']
        )

        if uploaded_file is not None:
            # Create a spinner while processing
            with st.spinner('Extracting data from resume...'):
                try:
                    # Process different file types
                    if uploaded_file.type == 'application/pdf':
                        text = self.extract_text_from_pdf(uploaded_file)
                    elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                        text = self.extract_text_from_docx(uploaded_file)
                    elif uploaded_file.type in ['image/jpeg', 'image/png']:
                        text = self.extract_text_from_image(uploaded_file)
                    else:
                        st.error('Unsupported file type')
                        return

                    # Extract and display information
                    extracted_data = self.parse_resume_text(text)
                    
                    # Display extracted information in a nice format
                    st.markdown("<h3>Extracted Information</h3>", unsafe_allow_html=True)
                    
                    # Create two columns for better layout
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Personal Information**")
                        if 'name' in extracted_data:
                            st.write(f"Name: {extracted_data['name']}")
                        if 'email' in extracted_data:
                            st.write(f"Email: {extracted_data['email']}")
                        if 'phone' in extracted_data:
                            st.write(f"Phone: {extracted_data['phone']}")
                    
                    with col2:
                        st.markdown("**Professional Summary**")
                        if 'skills' in extracted_data:
                            st.write("Skills:", ", ".join(extracted_data['skills']))
                    
                    # Experience section
                    if 'experience' in extracted_data:
                        st.markdown("**Work Experience**")
                        for exp in extracted_data['experience']:
                            st.markdown(f"- {exp}")
                    
                    # Education section
                    if 'education' in extracted_data:
                        st.markdown("**Education**")
                        for edu in extracted_data['education']:
                            st.markdown(f"- {edu}")

                except Exception as e:
                    st.error(f'Error processing file: {str(e)}')
        
        # Add some spacing
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        # Copyright notice at the bottom
        st.markdown(
            "<div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: #f0f2f6; padding: 10px; text-align: center;'>"
            "© 2025 Human Resource Management. All rights reserved."
            "</div>",
            unsafe_allow_html=True
        )

