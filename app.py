import streamlit as st
import datetime
st.title("Doctor's visit")


with st.form("Patient form"):
   title = st.text_input('First name', '')
   title = st.text_input('Last name', '')
   title = st.text_input('NSS', '')
   d= st.date_input("Patient birthday",) 
   txt = st.text_area('What the patient feel?', '''
    ''')
   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
       st.write("The form was submitted")

