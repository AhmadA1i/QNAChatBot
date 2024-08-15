from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
GOOGLE_API_KEY=st.secrets["API_KEY"]["KEY"]
genai.configure(api_key=os.getenv(GOOGLE_API_KEY))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

st.set_page_config(page_title="QNA ChatBot")
st.header("QNA ChatBot")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: Tell me your Question",key=input)
submit = st.button('Click to Chat')

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(('You',input))
    st.subheader('The Response is')
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Bot',chunk.text))
st.subheader('The Chat history is')

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
