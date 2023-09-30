import io
import streamlit as st
from streamlit_chat import message
import docx
import os
import sys
import atexit

def prompt_form(self):
    """
    Displays the prompt form
    """
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area(
            "Query:",
            placeholder="Ask me anything about the document...",
            key="input",
            label_visibility="collapsed",
        )
        submit_button = st.form_submit_button(label="Send")
        
        is_ready = submit_button and user_input
    return is_ready, user_input

def initialize():
    if "assistant" not in st.session_state:
        st.session_state["assistant"] = "Hey, How can I Help You !! 👋"
    if "user" not in st.session_state:
        st.session_state["user"] = "Hello Mr.Bot !!"

# def generate_messages(container):
#     if st.session_state["assistant"]:
#         with container:
#             for i in range(len(st.session_state["assistant"])):
#                 message(
#                     st.session_state["user"][i],
#                     is_user=True,
#                     key=f"history_{i}_user",
#                     avatar_style="big-smile",
#                 )
#                 message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")

def generate_messages(container):
    if st.session_state["chat_history"]:
        with container:
            for i in range(len(st.session_state["chat_history"])):
                message(
                    st.session_state["chat_history"][i],
                    is_user=True if i % 2 == 0 else False,
                    key=f"history_{i}_user",
                    avatar_style="big-smile" if i % 2 == 0 else "thumbs",
                )

def qa_chatbot():
    # Create a text box and a submit button
    st.subheader("Let's Chat....")
    # user_input = st.text_area("Please Ask Your Question")

    response_container, prompt_container = st.container(), st.container()

    # Initialize the chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

        # Add the initial greeting messages to the chat history
        st.session_state["chat_history"].append("Hello Mr.Bot !!")
        st.session_state["chat_history"].append("Hey, How can I Help You !! 👋")

    with prompt_container:
        # Display the prompt form
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="Ask me anything about the document...",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input

        # Generate the AI response
        if is_ready:
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()

            output = "Output from AI"

            sys.stdout = old_stdout

            # Add the user input and AI output to the chat history
            st.session_state["chat_history"].append(user_input)
            st.session_state["chat_history"].append(output)

        # Display the chat history
    generate_messages(response_container)   

    #if st.button("Submit"):
    #document_content = document_parse_loader()
    #answer_fr_user = testcase_generator(document_content,user_input)
    #st.write(answer_fr_user)
