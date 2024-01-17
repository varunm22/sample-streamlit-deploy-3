import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Streamlit Home")

st.sidebar.success("Select a demo above.")

st.write("Please select from one of the apps in the side bar to get started.")
