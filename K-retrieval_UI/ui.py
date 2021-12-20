
import streamlit as st

def title():
    st.markdown(
    "<h1 style='text-align: center; '>K-retrieval21</h1>",
    unsafe_allow_html=True,)

def load_source():
    search = st.text_input('Enter the path of information')
    if search:
        loads = True

def search_engine():
    pass

loads = False

if __name__ == '__main__':
    title()
    if loads:
        load_source()
    else:  
        search_engine()
