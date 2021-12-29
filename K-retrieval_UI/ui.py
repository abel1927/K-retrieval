import streamlit as st
from pathlib import Path
from utils import temp_load, temp_query

def title():
    st.markdown(
    "<h1 style='text-align: center; '>K-retrieval</h1>",
    unsafe_allow_html=True,)

def clean_query_session_variables():
    st.session_state.page_number = 0
    st.session_state.last_query = ""
    st.session_state.last_files_recovered = []

def show_files_paginator():
    N = 10 # Number of entries per screen
    files = st.session_state.last_files_recovered
    st.write(f'Showing {len(files)} results :')
    st.write("")
    # Add a next button and a previous button
    prev, _ ,next = st.columns([1, 10, 1])
    last_page = len(files) // N
    if next.button("Next"):
        if st.session_state.page_number + 1 > last_page:
            st.session_state.page_number = 0
        else:
            st.session_state.page_number += 1
    if prev.button("Previous"):
        if st.session_state.page_number - 1 < 0:
            st.session_state.page_number = last_page
        else:
            st.session_state.page_number -= 1
    # Get start and end indices of the next page of the files
    start_idx = st.session_state.page_number * N 
    end_idx = (1 + st.session_state.page_number) * N
    for i in range(start_idx,min(end_idx, len(files))):
        st.markdown(
        f"<h4>{i+1} -  {files[i]}</h3>",
        unsafe_allow_html=True,)

def load_source():
    search = st.text_input('Enter the path of information', value=st.session_state.last_path)
    if st.button('Load'):
        if search == "":
            st.error("Path to load information is required")
        elif not Path.exists(Path(search)):
            st.error("No such directory")
        else:
            st.session_state.last_path = search
            files = temp_load(search)
            st.success(f"{len(files)} files were found!!")
            st.write(files)
        clean_query_session_variables()

def search_engine():
    search = st.text_input('Enter the query', value=st.session_state.last_query)
    if st.button('Search'):
        clean_query_session_variables()
        if search == "":
            st.warning("Query is required")
        elif st.session_state.last_path == "":
            st.error("Is necesary load information source first")
        else:
            with st.spinner('Wait for it...'):
                files = temp_query(search, st.session_state.last_path)
                if len(files) > 0:
                    st.success("Retrieval done!")
                    st.session_state.last_query = search
                    st.session_state.last_files_recovered = files
                    show_files_paginator()
                else:
                    st.write(f"No Search results, please try again with different keywords")   
    else:
        if st.session_state.last_query != "" or len(st.session_state.last_files_recovered) != 0:
            show_files_paginator()


if __name__ == '__main__':
    if 'load' not in st.session_state:
        st.session_state.load = False
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    if "last_path" not in st.session_state:
        st.session_state.last_path = ""
    if 'last_query' not in st.session_state:
        st.session_state.last_query = ""
    if 'last_files_recovered' not in st.session_state:
        st.session_state.last_files_recovered = []
    
    st.sidebar.header('K-retrieval, A information retrieval system')
    nav = st.sidebar.radio('',['Load data source', 'Query phase'])
    st.sidebar.write('')
    st.sidebar.write('')
    title()
    if nav == 'Load data source':
        load_source()
    else:  
        search_engine()