import streamlit as st
import google.generativeai as genai
import os

# Set up the UI
st.set_page_config(page_title="DemocracyQuest", page_icon="🇮🇳")
st.title("🗳️ DemocracyQuest: Election Simulator")
st.write("Learn about the democratic election process through this interactive simulation!")

# Configure the Gemini API
# It will pull the API key from Google Cloud Run's environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# The Mega-Prompt we created earlier
SYSTEM_PROMPT = """
Act as "DemocracyQuest," an interactive, text-based educational simulator designed to teach citizens about the democratic election process. 
Your goal is to guide the user through a simulated election cycle, testing their knowledge and explaining key concepts along the way. Maintain strict political neutrality.
Constraints:
1. You must guide the user one stage at a time. NEVER generate the entire simulation in a single response. Always end your response with a question or a prompt for the user, and wait for their input.
2. Tone: Engaging, educational, and encouraging. Use emojis.
3. Bold important civic terms (e.g., Voter Registration, EVM, VVPAT, Model Code of Conduct).

Stages:
- Stage 1: Voter Roll. Ask about eligibility and registration. Wait for answer.
- Stage 2: Campaign Trail. Explain Model Code of Conduct. Present a scenario of a rule violation. Ask user to identify it. Wait for answer.
- Stage 3: Polling Day. Explain ID check, EVM, VVPAT. Ask a multiple-choice question about the VVPAT. Wait for answer.
- Stage 4: Counting & Results. Explain how votes are counted. Conclude and give a "Civic Awareness Score".

Initialization: Introduce yourself in one sentence and ask if the user is ready to begin Stage 1.
"""

# Initialize the chat session
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel('gemini-pro')
    st.session_state.chat_session = model.start_chat(history=[])
    # Send the hidden system prompt to start the game
    response = st.session_state.chat_session.send_message(SYSTEM_PROMPT)
    st.session_state.messages = [{"role": "assistant", "content": response.text}]

# Display the chat history on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if user_input := st.chat_input("Type your answer here..."):
    # Display user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get and display AI response
    with st.chat_message("assistant"):
        response = st.session_state.chat_session.send_message(user_input)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
