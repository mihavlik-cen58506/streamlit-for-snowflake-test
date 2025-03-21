from io import StringIO

import streamlit as st

import pandas as pd


# st.cache_resource  # you use decorator cache_resource only for non-serializable data and it will not make a copy of the original data
@st.cache_data  # you use decorator cache_data only for serializable data and it will make a copy of the original data ( for static data like csv files, data frames, etc.)
def loadFile(
    filename,
):  # you can write _arg into the arguments of the function to exclude it from the cache key
    return pd.read_csv(filename, header=0).convert_dtypes()


# Pokud se mezi filenames nachazi kriticky soubor ktery je v argumentu volaní funkce (on_click), tak se zastavi a vypise chybu, v tomto pripade to je portfolio.csv
def OnShowList(filename):
    if "names" in st.session_state:
        filenames = st.session_state["names"]
        if filename in filenames:
            st.error("Critical file found!")
            st.stop()


st.title("Hierarchical Data Viewer")

# session state it self is a dictionary of values that are stored in the session, like a useState in React, unlike useState, you can store any type of data in the session state

# pokud už mám něco uložené v global variable "names" tak to načtu, pokud ne tak se mi tam po inicializaci přidá jeden soubor "employees.csv" + případně další filenames, které se načtou z file_uploaderu
if "names" in st.session_state:
    filenames = st.session_state["names"]
else:
    filenames = ["employees.csv"]
    filenames = st.session_state["names"] = filenames


filename = "data/employees.csv"


uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", type="csv", accept_multiple_files=False
)
if uploaded_file is not None:
    filename = StringIO(uploaded_file.getvalue().decode("utf-8"))
    file = uploaded_file.name
    if file not in filenames:
        filenames.append(file)


btn = st.sidebar.button("Show List", on_click=OnShowList, args=("portfolio.csv",))
if btn:
    for f in filenames:
        st.sidebar.write(f)


tabs = st.tabs(["Source"])

df_orig = loadFile(filename)

tabs[0].dataframe(df_orig)  # show the original data frame
