import streamlit as st
from groq import Groq

# Konfiguracija strani
st.set_page_config(
    page_title="Plezalni Chatbot",
    page_icon="🧗",
    layout="centered"
)

# Naslov
st.title("🧗 Chatbot: Plezanje")
st.write("Vprašaj me karkoli o plezanju.")

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Inicializacija spomina (samo za sejo)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Si prijazen slovenski asistent za plezanje. "
                "Pomagaš z informacijami o plezalnih tehnikah, treningu, "
                "varnosti in izposoji plezalne opreme. "
                "Če vprašanje ni povezano s plezanjem, "
                "vljudno poveš, da za to področje nimaš informacij."
            )
        }
    ]

# Prikaz zgodovine pogovora
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Vnos uporabnika
user_input = st.chat_input("Vprašaj nekaj o plezanju...")

if user_input:
    # Prikaži uporabnikov vnos
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Klic Groq API-ja
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    # Prikaži odgovor
    with st.chat_message("assistant"):
        st.markdown(ai_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )
