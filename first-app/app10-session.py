import streamlit as st

st.title("Session State Example")

st.write("session_state", st.session_state)


# The key you passed to the control will be used to store the value in session state as key value pair with boolean value

# Each time you assign a specific key value to the input control, the state of this control will be stored in the session state

# button will not conserve state, after you rerender page by for example changing the value of the session_state, the button will be reset to the default value
if st.button("Button", key="my-button", type="primary", use_container_width=True):
    st.write("You licked!")

if st.toggle("Toggle", key="my-toggle"):
    st.write("You toggled!")

if st.checkbox("Checkbox", key="my-checkbox"):
    st.write("You checked!")


st.write("session_state", st.session_state)

"""
{
"my-button":false
"my-toggle":false
"my-checkbox":false
}
"""
