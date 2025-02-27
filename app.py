from dotenv import load_dotenv

load_dotenv()
import base64
import streamlit as st
import os
from PIL import Image 
import pymupdf
import google.generativeai as genai
import fitz
import docx2txt
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content,prompt])
    return response.text
def extract_text_from_pdf(uploaded_file):
    #extracting text from pdf
    with fitz.open(stream = uploaded_file.read()) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
        return text
def extract_text_from_docx(uploaded_file):
    text = ""
    text = docx2txt.process(uploaded_file)
    return text

#streamlit
st.header('ATS resume')
j_d= st.file_uploader(" Upload the job description in pdf or docs format", type=['pdf','docx'])
if j_d:
    text=''
    suffix = os.path.splitext(j_d.name)[1].lower()
    if suffix == ".pdf":
        text += extract_text_from_pdf(j_d) + "\n\n"
    elif suffix == ".docx":
        text += extract_text_from_docx(j_d) + "\n\n"
    else:
        st.warning(f"Unsupported file format: {j_d.name}")
    if text:
        uploaded_files= st.file_uploader(" Upload all the resume in pdf or docs format", type=['pdf','docx'], accept_multiple_files=True)
        complete_text=""
        if uploaded_files:
            for file in uploaded_files:
                resume_count=0
                suffix = os.path.splitext(file.name)[1].lower()
    
                if suffix == ".pdf":
                    complete_text += extract_text_from_pdf(file) + "\n\n"
                    resume_count += 1
                elif suffix == ".docx":
                    complete_text += extract_text_from_docx(file) + "\n\n"
                    resume_count += 1
                else:
                    st.warning(f"Unsupported file format: {file.name}")
    
            if resume_count>=1:
                input_prompt1 = """
                You are an experienced Technical Human Resource Manager,your task is to review the provided resumes against the job description. 
                Please share your professional evaluation on how much percent the candidate's profile aligns with the role. Only give the name of the canditate and their corresponding percentage as output in descending order. Give each result in seperate lines.
                """
                submit=st.button('Get info on the resumes')
                if submit:
                    output= get_gemini_response(input_prompt1, complete_text, text)
                    st.write(output)
            else:
                st.write('Please Upload the resume')