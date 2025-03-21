import json
import uuid
from io import StringIO

import auth
import modules.animated as animated
import modules.charts as charts
import modules.formats as formats
import modules.graphs as graphs
import modules.utils as utils
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("Hierarchical Data Viewer")
st.caption("Display your hierarchical data with charts and graphs.")

# auth.check_password()
# auth.check_user_and_password()


def getSessionId():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]


@st.cache_data(show_spinner="Loading the CSV file...")
def loadFile(session_id, filename):
    return pd.read_csv(filename).convert_dtypes()


with st.sidebar:
    uploaded_file = st.file_uploader(
        "Upload a CSV file", type=["csv"], accept_multiple_files=False
    )

    filename = utils.getFullPath("data/employees.csv")
    if uploaded_file is not None:
        filename = StringIO(uploaded_file.getvalue().decode("utf-8"))

    df_orig = loadFile(getSessionId(), filename)
    cols = list(df_orig.columns)

    child = st.selectbox("Child Column Name", cols, index=0)
    parent = st.selectbox("Parent Column Name", cols, index=1)
    # based on choosen values from selectboxes create a new dataframe
    df = df_orig[[child, parent]]

    # st.sidebar.markdown(f"User: {st.experimental_user.email}")

tabSource, tabFormat, tabGraph, tabChart, tabAnim = st.tabs(
    ["Source", "Format", "Graph", "Chart", "Animated"]
)

with tabSource:
    st.dataframe(df_orig, use_container_width=True)

# show in another data format
with tabFormat:
    sel = st.selectbox(
        "Select a data format:", ["JSON", "XML", "YAML", "JSON Path", "JSON Tree"]
    )

    root = formats.getJson(df)
    if sel == "JSON":
        jsn = json.dumps(root, indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "XML":
        xml = formats.getXml(root)
        st.code(xml, language="xml", line_numbers=True)
    elif sel == "YAML":
        yaml = formats.getYaml(root)
        st.code(yaml, language="yaml", line_numbers=True)
    elif sel == "JSON Path":
        jsn = json.dumps(formats.getPath(root, []), indent=2)
        st.code(jsn, language="json", line_numbers=True)
    elif sel == "JSON Tree":
        st.json(root)

with tabGraph:
    graph = graphs.getEdges(df)
    url = graphs.getUrl(graph)
    st.link_button("Visualize Online", url)
    st.graphviz_chart(graph)

# show as Plotly chart
with tabChart:
    labels = df[df.columns[0]]
    parents = df[df.columns[1]]

    sel = st.selectbox(
        "Select a chart type:", ["Treemap", "Icicle", "Sunburst", "Sankey"]
    )
    if sel == "Treemap":
        fig = charts.makeTreemap(labels, parents)
    elif sel == "Icicle":
        fig = charts.makeIcicle(labels, parents)
    elif sel == "Sunburst":
        fig = charts.makeSunburst(labels, parents)
    elif sel == "Sankey":
        fig = charts.makeSankey(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

# show as D3 animated chart
with tabAnim:
    sel = st.selectbox(
        "Select a D3 chart type:",
        ["Collapsible Tree", "Linear Dendrogram", "Radial Dendrogram", "Network Graph"],
    )
    if sel == "Collapsible Tree":
        filename = animated.makeCollapsibleTree(df)
    elif sel == "Linear Dendrogram":
        filename = animated.makeLinearDendrogram(df)
    elif sel == "Radial Dendrogram":
        filename = animated.makeRadialDendrogram(df)
    elif sel == "Network Graph":
        filename = animated.makeNetworkGraph(df)

    with open(filename, "r", encoding="utf-8") as f:
        components.html(f.read(), height=2200, width=1000)

if st.toggle("Read documentation"):
    st.write(
        """
This Streamlit application provides a hierarchical data viewer with various visualization options.

Modules:
- json: For handling JSON data.
- uuid: For generating unique session IDs.
- StringIO: For handling in-memory file objects.
- auth: Custom module for authentication (commented out).
- modules.animated: Custom module for animated visualizations.
- modules.charts: Custom module for chart visualizations.
- modules.formats: Custom module for data format conversions.
- modules.graphs: Custom module for graph visualizations.
- modules.utils: Custom utility functions.
- pandas: For data manipulation and analysis.
- streamlit: For creating the web application.
- streamlit.components.v1: For embedding custom HTML components.

Functions:
- getSessionId(): Generates and returns a unique session ID.
- loadFile(session_id, filename): Loads a CSV file and converts its data types.

Streamlit Components:
- st.set_page_config(): Sets the page layout to wide.
- st.title(): Sets the title of the application.
- st.caption(): Sets a caption for the application.
- st.sidebar: Contains file uploader and column selection widgets.
- st.tabs(): Creates tabs for different views (Source, Format, Graph, Chart, Animated).
- st.dataframe(): Displays the original dataframe.
- st.selectbox(): Creates dropdown menus for selecting data formats and chart types.
- st.code(): Displays code snippets in various formats (JSON, XML, YAML).
- st.json(): Displays JSON data.
- st.link_button(): Creates a button linking to an online graph visualization.
- st.graphviz_chart(): Displays a Graphviz chart.
- st.plotly_chart(): Displays a Plotly chart.
- components.html(): Embeds custom HTML content.

Usage:
1. Upload a CSV file via the sidebar.
2. Select the child and parent columns for hierarchical data.
3. View the data in different formats and visualizations using the tabs.
"""
    )
