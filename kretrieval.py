import streamlit as st
from pathlib import Path
from model.vectrorialIndex import VectorialIndex
import matplotlib.pyplot as plt
from time import time
import os, platform, subprocess

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
        with st.expander(f"{i+1}   -  {files[i].name()}"):
            st.write(f"*Preview:*  {files[i].first_300()}")
            if st.button("open",key=i+1):
                if platform.system() == "Windows":
                    os.startfile(files[i].path())
                else:
                    opener = "open" if platform.system() == "Darwin" else "xdg-open"
                    subprocess.call([opener, files[i].path()])

def load_source():
    search = st.text_input('Enter the path of information', value=st.session_state.last_path)
    add, _ , stats, _, clean = st.columns([1,8,1,1,1])
    if add.button("Add"):
        if search == "":
            st.error("Path to load information is required")
        elif not Path.exists(Path(search)):
            st.error("No such directory")
        else:
            st.session_state.last_path = search
            N = st.session_state.index.add_source(search)
            st.success(f"{N} files have been indexed!!")
        clean_query_session_variables()
    if stats.button("Stats"):
        st.info("##### **Collection Statistics**")
        stats = st.session_state.index.get_stats()
        sources, docs, terms, time = st.columns(4)
        sources.metric("Total sources", stats['total sorces'])
        docs.metric("Indexed docs", stats['total docs'])
        terms.metric("Indexed terms", stats['total terms'])
        time.metric('Indexed time/Doc', f"{stats['indexed time/doc']} s")

        if stats['total sorces'] > 0:
            fig, ax = plt.subplots()
            ax.set_xlabel("Idf")
            fig.suptitle("Inversed document frequency", fontsize=15)
            plt.hist(stats['idfs'], color='b', bins=15)
            st.pyplot(fig)

        st.write(" ")
        st.write(f"Most present terms:")
        st.write(stats['most present terms'])


    if clean.button("Clean"):
        with st.spinner('Cleanning...'):
            st.session_state.index.clean()
            st.success("Index already empty!!")
            clean_query_session_variables()
            st.session_state.last_path = ""

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
                start= time()
                files = st.session_state.index.get_rank(search)
                end = time()
                search_time = round(end-start, 3)
                if len(files) > 0:
                    st.success(f"Retrieval done!  \n Search time: {search_time}s")
                    st.session_state.last_query = search
                    st.session_state.last_files_recovered = [d for d,_ in files]
                    show_files_paginator()
                else:
                    st.write(f"No Search results, please try again with different keywords. Search time:{search_time}s")   
    else:
        if st.session_state.last_query != "" or len(st.session_state.last_files_recovered) != 0:
            show_files_paginator()

if __name__ == '__main__':
    if 'index' not in st.session_state:
        st.session_state.index = VectorialIndex()
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
    
    st.set_page_config(
        page_title="K-retrieval")

    st.sidebar.header('K-retrieval, An information retrieval system')
    nav = st.sidebar.radio('',['Load data source', 'Search engine'])
    st.sidebar.markdown(""" \n \n""")

    st.sidebar.markdown(" ## [Source Code](https://github.com/abel1927/K-retrieval)", unsafe_allow_html=True,)
    st.sidebar.markdown(""" \n""")

    expander = st.sidebar.expander('Team')
    expander.markdown("### We are students of CS at the MATCOM faculty of Havana University.\n #### Claudia Puentes Hernández [ClauP99] (https://github.com/ClauP99)\n #### Abel Molina Sánchez [abel1927] (https://github.com/abel1927)", unsafe_allow_html=True,)
    
    title()
    if nav == 'Load data source':
        load_source()
    else:  
        search_engine()