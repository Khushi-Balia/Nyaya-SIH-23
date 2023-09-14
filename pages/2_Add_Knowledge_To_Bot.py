import streamlit as st
import requests

st.title("Message Store API")

user_input = st.text_area("Increase the knowledge of the bot by entering legal facts :")

url = "http://127.0.0.1:5000/message-store-api"

json_data = {"context": user_input}

def send_post_request(url, json_data):
    try:
        response = requests.post(url, json=json_data)
        if response.status_code == 200:
            st.success("POST request sent successfully!")
        else:
            st.error(f"Error sending POST request. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if st.button("Send POST Request"):
    if user_input:
        send_post_request(url, json_data)
    else:
        st.warning("Please enter text before sending the request.")

if user_input:
    st.subheader("JSON Data Sent:")
    st.json(json_data)


