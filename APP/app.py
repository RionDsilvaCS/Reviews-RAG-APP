import streamlit as st
from chain import ResponseChain

st.title('🦜🔗 Reviews App')

chat = ResponseChain()

def generate_response(input_text):
    st.info(chat.get_response(input_text))

with st.form('my_form'):
    text = st.text_area('Prompt below', 'Enter Here !!!')
    submitted = st.form_submit_button('Submit')
   
    if submitted:
        generate_response(text)
