import pandas as pd
import streamlit as st
from code_package.streamlit.util.google_oauth import oauth

oauth()

st.title("First streamlit app")
st.write(pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
