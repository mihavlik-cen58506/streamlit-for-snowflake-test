import streamlit as st

import pandas as pd

st.title("Hierarchical Data Viewer")


df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()
st.dataframe(df)  # display data table in streamlit

edges = ""
for _, row in df.iterrows():
    if not pd.isna(row.iloc[1]):  # if the second column is not empty
        edges += f'\t"{row.iloc[0]}" -> "{row.iloc[1]}";\n'  # create an edge between the first and second column

d = f"digraph {{\n{edges}}}"  # create the graph in DOT language
st.graphviz_chart(d)  # render the graph in Streamlit

# url = f"https://magjac.com/graphviz-visual-editor/?dot={urllib.parse.quote(d)}"  # create the URL to the Graphviz Visual Editor
# webbrowser.open(url)  # open the URL in the default web browser
