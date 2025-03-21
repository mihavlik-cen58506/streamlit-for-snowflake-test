import streamlit as st

st.title("Hierarchical Data Viewer")
st.header("This is a header")


st.subheader("This is a subheader")
st.caption("This is a caption")

st.write("This is a write")
st.text("This is a text")
st.code("v = variable()\nanother_call()", "")
st.markdown("**This is a markdown text typed with bold**")
st.divider()
st.latex("...")

st.success("This is a success message")
st.info("This is an info message")
st.warning("This is a warning message")
st.error("This is an error message")

# st.balloons()
# st.snow()

st.button("Click me")
st.checkbox("Check me")
st.radio("Choose me", ["A", "B", "C"])
st.selectbox("Choose me", ["A", "B", "C"], index=None)
st.multiselect("Choose me", ["A", "B", "C"])
st.slider("Slide me", 0, 10)
st.spinner(text="Loading...")
