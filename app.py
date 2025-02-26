import streamlit as st

# Title of the app
st.title("🚀 My First Streamlit App")

# User input
name = st.text_input("Enter your name:")

# Display greeting if the user enters a name
if name:
    st.write(f"Hello, **{name}**! Welcome to my Streamlit app. 😊\nThats' the first one but I'll make a new one soon ...")
