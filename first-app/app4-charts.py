import time

import plotly.graph_objects as go
import streamlit as st

import pandas as pd


# Functions
# Create a Treemap
def makeTreemap(labels, parents):
    data = go.Treemap(
        ids=labels,
        labels=labels,
        parents=parents,
        root_color="lightblue",
    )
    fig = go.Figure(data)
    return fig


# Create a Icicle
def makeIcicle(labels, parents):
    data = go.Icicle(
        ids=labels,
        labels=labels,
        parents=parents,
        root_color="lightgrey",
    )
    fig = go.Figure(data)
    return fig


# Create a Sunburst
def makeSunburst(labels, parents):
    data = go.Sunburst(
        ids=labels,
        labels=labels,
        parents=parents,
        insidetextorientation="horizontal",
    )
    fig = go.Figure(data)
    return fig


# Create a Sankey
def makeSankey(labels, parents):
    data = go.Sankey(
        node=dict(label=labels),
        link=dict(
            source=[list(labels).index(x) for x in labels],
            target=[-1 if pd.isna(x) else list(labels).index(x) for x in parents],
            label=labels,
            value=list(range(1, len(labels))),
        ),
    )
    fig = go.Figure(data)
    return fig


st.title(
    "Hierarchical Data Viewer",
)

df = pd.read_csv("data/employees.csv", header=0).convert_dtypes()

# Display the data as a table
st.dataframe(df)

# Extract the labels and parents from the data
labels, parents = df[df.columns[0]], df[df.columns[1]]


with st.expander("Playground"):
    with st.container():
        col1, col2, col3 = st.columns(
            [1, 2, 1],
            border=True,
        )  # Poměr velikosti sloupců (větší pro LaTeX)

        with col1:
            st.markdown("**Equations**")
            st.latex(r"""e^{i\pi} + 1 = 0""")  # Matematický vzorec
            st.latex(r"""\int_0^\infty x^2 dx""")  # Další matematický vzorec

        with col2:
            st.image("data/images/lion.jpg", caption="A lion")  # Obrázek s popiskem

        with col3:
            st.markdown("**Buttons**")
            st.link_button(
                "Graphviz Editor", "https://magjac.com/graphviz-visual-editor/"
            )  # Odkaz jako tlačítko

with st.expander("Fake-multi expand"):
    if st.checkbox("Fake expand"):
        st.write("Hello world")

cols = st.columns(2, border=True)
cols[0].write("This is column 0")
cols[1].write("This is column 1")


# st.empty() is a placeholder that can be updated with new content
# Placeholder for real-time data
real_time_data = st.empty()
# Simulate real-time data update
for i in range(10):
    time.sleep(1)  # Simulate data generation delay
    real_time_data.text(f"Latest sensor reading: {i}")


st.subheader(
    "Charts",
)
# Tabs
# First way to create tabs
tabs = st.tabs(["Treemap", "Icicle", "Sunburst", "Sankey"])

with tabs[0]:
    fig = makeTreemap(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    fig = makeIcicle(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    fig = makeSunburst(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    fig = makeSankey(labels, parents)
    st.plotly_chart(fig, use_container_width=True)

# Second way to create tabs
t1, t2, t3, t4 = st.tabs(["Treemap", "Icicle", "Sunburst", "Sankey"])

with t1:
    fig = makeTreemap(labels, parents)
    st.plotly_chart(fig, use_container_width=True, key="t1")

with t2:
    fig = makeIcicle(labels, parents)
    st.plotly_chart(fig, use_container_width=True, key="t2")

with t3:
    fig = makeSunburst(labels, parents)
    st.plotly_chart(fig, use_container_width=True, key="t3")

with t4:
    fig = makeSankey(labels, parents)
    st.plotly_chart(fig, use_container_width=True, key="t4")

with st.sidebar:
    st.write("This is a sidebar")
    st.selectbox("Select", ["A", "B", "C"])
    with st.spinner("Loading..."):
        time.sleep(3)
    st.success("Loading complete!")

    def get_user_name():
        return "John"

    with st.echo():  # Everything inside this block will be both printed to the screen and executed.

        def get_punctuation():
            return "!!!"

        greeting = "Hi there, "
        value = get_user_name()
        punctuation = get_punctuation()

        st.write(greeting, value, punctuation)

    # And now we're back to _not_ printing to the screen
    foo = "bar"
