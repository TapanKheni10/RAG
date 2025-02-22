import streamlit as st
import requests
import re

version = "0.1.0"

def upload_document():
    uploaded_file = st.file_uploader(label = "Choose a document", type = ['pdf', 'txt'])
    
    if uploaded_file:
        return_message = requests.post(f'http://localhost:8000/api/{version}/doc/upload', files = {'uploaded_file': uploaded_file})
        
        if return_message:    
            st.success('File uploaded successfully!')
    else:
        st.warning('Please upload a file first!')
        
def chat_with_document():
    user_question = st.chat_input('Ask a question to the document...')
    
    if user_question:
    
        response = requests.post(f'http://localhost:8000/api/{version}/doc/chat', json = {'question': user_question})
        
        if response.status_code == 200:
            response_text = response.content.decode('utf-8')
    
            response_text = response_text.replace('\\n\\n', '')
            response_text = response_text.replace('\\n', '')
            response_text = re.sub(r'<.*?>', '', response_text)
            
            with st.expander('Check the answer'):
                st.markdown(f"### Your Question: \n> {user_question}")
                st.markdown(f"### Answer: \n> {response_text}")
                
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    
    else:
        st.warning('Please ask a question first!')
        

st.header('RAG (Retrieval Augmented Generation)')

tab1, tab2 = st.tabs(['Upload a document', 'Ask questions'])

with tab1:
    upload_document()
with tab2:
    chat_with_document()