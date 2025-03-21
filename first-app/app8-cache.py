import datetime
import urllib.parse
from io import StringIO

import streamlit as st

import pandas as pd


def getGraph(df):
    edges = ""
    for _, row in df.iterrows():
        if not pd.isna(row.iloc[1]):  # if the second column is not empty
            edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'  # create an edge between the first and second column
    return f"digraph {{\n{edges}}}"  # create the graph in DOT language


# st.cache_resource  # you use decorator cache_resource only for non-serializable data and it will not make a copy of the original data
@st.cache_data  # you use decorator cache_data only for serializable data and it will make a copy of the original data ( for static data like csv files, data frames, etc.)
def loadFile(
    filename,
):  # you can write _arg into the arguments of the function to exclude it from the cache key
    return pd.read_csv(filename, header=0).convert_dtypes()


@st.cache_data
def now():
    return datetime.datetime.now().strftime("%H:%M:%S - %#d.%#m.%Y")


st.title("Hierarchical Data Viewer")

filename = "data/employees.csv"

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", type="csv", accept_multiple_files=False
)
if uploaded_file is not None:
    filename = StringIO(uploaded_file.getvalue().decode("utf-8"))


df_orig = loadFile(filename)

tabs = st.tabs(["Source", "Graph", "Dot Code"])  # create tabs in streamlit
cols = list(df_orig.columns)  # get the column names

with st.sidebar:
    child = st.selectbox("Select the child column", cols, index=0)
    parent = st.selectbox("Select the parent column", cols, index=1)
    df = df_orig[
        [child, parent]
    ]  # Chart will filter based on chosen columns, returns a new data frame with only the selected columns
    if st.button("Show Current Time"):
        st.write(
            now()
        )  # will show time that was rendered first time, than it will show only cached value
        st.write(datetime.datetime.now().strftime("%H:%M:%S - %#d.%#m.%Y"))


tabs[0].dataframe(df_orig)  # show the dataframe in the first tab

with tabs[0]:
    slider = st.slider("Pick a number", 0, 100, 41)
    st.write(f"Selected value: {slider}")

chart = getGraph(df)
tabs[1].graphviz_chart(chart, use_container_width=True)

url = f"https://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(chart)}"  # create the URL to the Graphviz Visual Editor
tabs[2].link_button("Visualize Online", url)
tabs[2].code(chart)
