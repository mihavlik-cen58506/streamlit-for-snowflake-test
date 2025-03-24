import urllib.parse
from io import StringIO

import pandas as pd
import streamlit as st

# DYNAMIC FILTERING OF GRAPH


def getGraph(df):
    edges = ""
    for _, row in df.iterrows():
        if not pd.isna(row.iloc[1]):  # if the second column is not empty
            edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'  # create an edge between the first and second column
    return f"digraph {{\n{edges}}}"  # create the graph in DOT language


st.title("Hierarchical Data Viewer")

filename = "data/employees.csv"

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file", type="csv", accept_multiple_files=False
)
if uploaded_file is not None:
    filename = StringIO(uploaded_file.getvalue().decode("utf-8"))


df_orig = pd.read_csv(filename, header=0).convert_dtypes()

tabs = st.tabs(["Source", "Graph", "Dot Code"])  # create tabs in streamlit

cols = list(df_orig.columns)  # get the column names

child = st.sidebar.selectbox("Select the child column", cols, index=0)
parent = st.sidebar.selectbox("Select the parent column", cols, index=1)
df = df_orig[[child, parent]]  # Chart will filter based on choosen columns

tabs[0].dataframe(df_orig)  # show the dataframe in the first tab
slider = st.slider("Pick a number", 0, 10, 5)
tabs[0].write(f"Selected value: {slider}")

# Create the graph and show it in the second tab using filtered data frame from the sidebar select boxes
chart = getGraph(df)
tabs[1].graphviz_chart(chart, use_container_width=True)

url = f"https://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(chart)}"  # create the URL to the Graphviz Visual Editor
tabs[2].link_button("Visualize Online", url)
tabs[2].code(chart)
