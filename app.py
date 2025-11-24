import streamlit as st
from datetime import datetime
from chatbot import get_chatbot
from utils import load_rules
import time


st.set_page_config(
    page_title="Nutritionist Chatbot",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar info
st.sidebar.title("Quick Tips")
st.sidebar.info("""
- Ask anything about food, health, and wellness.
- I share helpful advice, but not a doctor’s prescription.
- For serious issues, always check with a healthcare expert.
- Example: "Best foods for energy?" or "How to control sugar cravings?"
""")

# Download chat as .txt
def download_chat():
    chat_text = ""
    for msg in st.session_state["messages"]:
        chat_text += f"{msg['role'].upper()} [{msg['time']}]: {msg['content']}\n\n"
    st.download_button(" Download Chat", chat_text, file_name="chat_history.txt")


st.title("🥗 Nutritionist Chatbot")
st.write("Ask me anything about diet, health, or nutrition.")

# Load chatbot + rules
qa = get_chatbot()
rules = load_rules()

# Condition-specific advice
condition_advice = {
    "pcos": "For PCOS, include whole grains, lean proteins, and anti-inflammatory foods like berries, fatty fish, and leafy greens. Avoid refined carbs and sugary snacks.",
    "anemia": "For anemia, eat iron-rich foods like spinach, lentils, red meat (if non-veg), and vitamin C foods like oranges for better absorption.",
    "kidney stones": "Drink plenty of water, reduce salt, limit spinach, nuts, chocolate, and include citrus foods.",
    "diabetes": "Eat whole grains, legumes, fiber-rich foods. Avoid sugary drinks, processed snacks, and white flour.",
    "hypertension": "Reduce sodium, avoid processed foods, eat bananas, sweet potatoes, and leafy greens.",
    "obesity": "Control portions, increase fiber, lean proteins, and healthy fats. Avoid sugary drinks.",
    "thyroid": "Eat selenium (brazil nuts), iodine (seaweed), lean proteins, avoid heavy processed foods.",
    "arthritis": "Eat anti-inflammatory foods like fatty fish, turmeric, berries. Avoid red meat and processed snacks.",
    "heart disease": "Eat omega-3 rich fish, whole grains, nuts. Limit saturated fats and sugar.",
    "digestive issues": "Use probiotics, fiber-rich foods, stay hydrated, avoid fried foods and excessive caffeine."
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Clear chat
if st.sidebar.button("🗑 Clear Chat"):
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    avatar = "🙂" if msg["role"] == "user" else "👩‍⚕"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        st.caption(msg["time"])


# Chat input form
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message...", 
                               placeholder="e.g., What should I eat for anemia?")
    send = st.form_submit_button("➤ Send")

# When user sends a message
if send and user_input:
    time_now = datetime.now().strftime("%I:%M %p")

    # Save user message
    st.session_state["messages"].append({
        "role": "user",
        "content": user_input,
        "time": time_now
    })

    # Show user message
    with st.chat_message("user", avatar="🙂"):
        st.markdown(user_input)
        st.caption(time_now)

    # Bot response
    with st.chat_message("assistant", avatar="👩‍⚕"):
        placeholder = st.empty()
        placeholder.markdown("Typing...")
        time.sleep(1)

        # --- NEW: Correct way to call LangChain Runnables ---
        if callable(qa):
            answer = qa(user_input)        # fallback mode (no vectordb)
        else:
            answer = qa.invoke(user_input) # modern chain

        # Condition-based special advice
        for condition, advice in condition_advice.items():
            if condition in user_input.lower():
                answer = advice
                break

        placeholder.markdown(answer)
        st.caption(datetime.now().strftime("%I:%M %p"))

    # Save bot message
    st.session_state["messages"].append({
        "role": "assistant",
        "content": answer,
        "time": datetime.now().strftime("%I:%M %p")
    })


# Download chat
download_chat()