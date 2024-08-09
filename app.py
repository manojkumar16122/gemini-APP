import os
import streamlit as st
import google.generativeai as genai
from PIL import Image
import time
# Configure the Gemini API using the environment variable
api_key = os.getenv("GEMINI_API_KEY")
if api_key is None:
    st.error("API key is not found. Please configure the GEMINI_API_KEY secret.")
else:
    genai.configure(api_key=api_key)
# Set up the generation config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "model",
            "parts": ["Welcome to the chat! I'm Ram, your friendly assistant. 😊 How can I assist you today?"],
        },
    ]

# Display the chat history
st.markdown("<h2 style='color: #4CAF50;'>Chat with Ram</h2>", unsafe_allow_html=True)
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"<p style='color: #1E88E5;'><strong>You:</strong> {chat['parts'][0]}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p style='color: #4CAF50;'><strong>Ram:</strong> {chat['parts'][0]}</p>", unsafe_allow_html=True)

# Input text box for user message
user_input = st.text_input("Your message:", "")

# Send the message when the user submits input
if st.button("Send") and user_input:
    # Add the user's input to the chat history
    st.session_state.chat_history.append({"role": "user", "parts": [user_input]})
    
    # Show a thinking GIF while waiting for the response
    with st.spinner('Ram is thinking...'):
        time.sleep(2)  # Simulate thinking time

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

        # Clear the input box after sending the message
        st.experimental_rerun()

# Include a footer or additional icons
st.markdown("<p style='text-align: center;'>💬 Enjoy your chat with Ram!</p>", unsafe_allow_html=True)
