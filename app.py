import streamlit as st
from groq import Groq

# ---- KONFIGURACIJA STRANI ----
st.set_page_config(
    page_title="Plezalni Chatbot",
    page_icon="🧗",
    layout="centered"
)

# ---- NASLOV ----
st.title("🧗 Plezalni Chatbot")
st.write("Postavi vprašanje o plezanju, opremi, tehnikah, treningu ali izposoji opreme.")

# ---- Groq client ----
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---- INICIALIZACIJA SPOMINA (SESSION STATE) ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Si prijazen slovenski asistent, strokovnjak za plezanje. "
                "Odgovarjaš izključno v slovenščini. "
                "Če vprašanje ni povezano s plezanjem ali vsebino spletne strani, "
                "vljudno povej, da za to področje nimaš informacij. "
                "Ponujaj nasvete za plezalno opremo, tehnike, varnost, trening in tutoriale. "
                "Na spletni strani imaš naslednje vsebine: "
                "1. Plezalno središče: plezalci si lahko delijo nasvete, smeri in zgodbe, povezovanje z drugimi. "
                "2. Najnovejše plezalne teme: video tutoriali, deljenje slik in videov. "
                "3. Izposoja opreme: možnost izposoje vse plezalne opreme, ki jo potrebuješ."
            )
        }
    ]

# ---- PRIKAZ ZGODOVINE POGOVORA ----
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- VNOS UPORABNIKA ----
user_input = st.chat_input("Vprašaj nekaj o plezanju...")

if user_input:
    # Prikaži uporabnikov vnos
    with st.chat_message("user"):
        st.markdown(user_input)

    # Dodaj uporabnikov vnos v zgodovino
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # ---- KLIC GROQ API ----
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    # Prikaži odgovor
    with st.chat_message("Grip"):
        st.markdown(ai_reply)

    # Dodaj odgovor v zgodovino
    st.session_state.messages.append(
        {"role": "Grip", "content": ai_reply}
    )
