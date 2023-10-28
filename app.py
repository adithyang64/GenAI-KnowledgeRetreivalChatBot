import streamlit as st
import docx
import os
import io
import sys
import atexit
from TestCaseGenerator import document_parse_loader, testcase_generator
from helperfns import cleanup_temp_files, cleanup_temp_video_files, generate_messages, initialize, qa_chatbot, save_embeddings, upload_docs_display, upload_video_display
from streamlit_chat import message

from video2txt import video_to_text


st.set_page_config(layout="wide", page_icon="💬", page_title="Chat-Bot 🤖")
#st.set_page_bg(image="bg-img.jpg")
# set_background('bg-img.jpg')


# Streamlit app title
st.title("Knowledge Retrieval Chatbot")

with st.sidebar:

    # Create tabs for uploading documents and videos
    selected_tab = st.radio("Select File Type:", ["Upload Documents (PDF, DOCX, TXT)", "Upload Videos"])

    if selected_tab == "Upload Documents (PDF, DOCX, TXT)":
        flag,temp_files=upload_docs_display("temp_documents")
    else:
        flag,temp_video_files=upload_video_display("temp_videos")

if flag==1:
    tab1, tab2 = st.tabs(["Ask Questions to Chatbot", "Get Assistance from the Bot"])
    with tab1:
        index = save_embeddings()
        qa_chatbot(index)
    with tab2:
        st.subheader("Get Assistance")
        user_input = st.text_area("Please Ask Your Question")
        if st.button("Submit"):
            document_content = document_parse_loader()
            answer_fr_user = testcase_generator(document_content,user_input)
            st.write(answer_fr_user)



# Cleanup functions to run when we exit
try:
    atexit.register(cleanup_temp_files(temp_files))
    atexit.register(cleanup_temp_video_files(temp_video_files))
except Exception as e:
    print("Exception caught in Deleting Files....")