import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(layout="wide")

st.title(
    "Hierarchical Data Viewer",
)

st.markdown(
    "<h1 style='text-align: center;'>Hierarchical Data Viewer</h1>",
    unsafe_allow_html=True,
)

st.divider()

with st.container():
    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )  # Poměr velikosti sloupců (větší pro LaTeX)

    with col1:
        st.latex(r"""e^{i\pi} + 1 = 0""")  # Matematický vzorec

    with col2:
        st.image("data/images/lion.jpg", caption="A lion")  # Obrázek s popiskem

    with col3:
        st.link_button(
            "Graphviz Editor", "https://magjac.com/graphviz-visual-editor/"
        )  # Odkaz jako tlačítko

st.divider()

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()

# Display the data as a table
st.dataframe(df)


# Extract the labels and parents
labels = df[df.columns[0]]
parents = df[df.columns[1]]

# Create a Treemap
data = go.Treemap(
    ids=labels,
    labels=labels,
    parents=parents,
    root_color="lightblue",
)
# Create a figure
fig = go.Figure(data)
# Display the figure
st.plotly_chart(fig, use_container_width=True)


# Create a Icicle
data = go.Icicle(
    ids=labels,
    labels=labels,
    parents=parents,
    root_color="lightblue",
)
# Create a figure
fig = go.Figure(data)
# Display the figure
st.plotly_chart(fig, use_container_width=True)


# Create a Sunburst
data = go.Sunburst(
    ids=labels,
    labels=labels,
    parents=parents,
    insidetextorientation="horizontal",
)
# Create a figure
fig = go.Figure(data)
# Display the figure
st.plotly_chart(fig, use_container_width=True)


# Create a Sankey
data = go.Sankey(
    node=dict(label=labels),
    link=dict(
        source=[list(labels).index(x) for x in labels],
        target=[-1 if pd.isna(x) else list(labels).index(x) for x in parents],
        label=labels,
        value=list(range(1, len(labels))),
    ),
)
# Create a figure
fig = go.Figure(data)
# Display the figure
st.plotly_chart(fig, use_container_width=True)
