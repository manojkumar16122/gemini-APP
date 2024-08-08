import os
import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key="AIzaSyAqWpn4z2Z19OKHkH53HsIl78ZvKVhyZCI")

# Set up the generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "user",
            "parts": ["hello ram"],
        },
        
        {
            "role": "model",
            "parts": ["My name is Ram! 😊 I'm here to help you with any questions you might have. \n"],
        },
    ]

# Display the chat history
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.write(f"**You:** {chat['parts'][0]}")
    else:
        st.write(f"**Ram:** {chat['parts'][0]}")

# Input text box for user message
user_input = st.text_input("Your message:", "")

# Send the message when the user submits input
if st.button("Send") and user_input:
    # Add the user's input to the chat history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

    # Create the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction="You are a friendly assistant answer the queries only if you know the answer, your name is Ram",
    )

    # Start a chat session with the current history
    chat_session = model.start_chat(history=st.session_state.chat_history)

    # Get the model's response
    response = chat_session.send_message(user_input)
    
    # Add the model's response to the chat history
    st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

    # Refresh the page to show the new message
    st.experimental_rerun()
