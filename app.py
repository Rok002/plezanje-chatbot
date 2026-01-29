import streamlit as st
from groq import Groq

# ---- KONFIGURACIJA ----
st.set_page_config(page_title="Plezalni Chatbot", page_icon="🧗")

# API ključ iz Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MAX_MESSAGES = 10

# ---- SESSION STATE (SPOMIN) ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Si prijazen chatbot, strokovnjak za plezanje. "
                "Odgovarjaš izključno v slovenščini. "
                "Če vprašanje ni povezano s plezanjem ali športom, "
                "vljudno povej, da za to področje nimaš informacij. "
                "Ponujaj nasvete za plezalno opremo, tehnike, varnost, trening in tutoriale. "
                "Poleg tega svetuj uporabnikom glede izposoje opreme. "
                "Na spletni strani imaš naslednje vsebine: "
                "1. Plezalno središče: plezalci si lahko delijo nasvete, smeri in zgodbe, povezovanje z drugimi. "
                "2. Najnovejše plezalne teme: video tutoriali, deljenje slik in videov. "
                "3. Izposoja opreme: možnost izposoje vse plezalne opreme, ki jo potrebuješ."
            )
        }
    ]

def omeji_zgodovino():
    while len(st.session_state.messages) > MAX_MESSAGES:
        st.session_state.messages.pop(1)

# ---- NASLOV ----
st.title("🧗 Plezalni Chatbot")
st.write("Postavi vprašanje o plezanju, opremi, tehnikah, treningu ali izposoji opreme.")

# ---- PRIKAZ ZGODOVINE ----
for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"**Vi:** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

# ---- VNOS UPORABNIKA ----
user_input = st.text_input(
    "Vaše vprašanje:",
    value="",              # vedno prazno na začetku
    key="user_input"       # unikatni key
)

if st.button("Pošlji") and user_input:
    # Dodaj uporabniško sporočilo
    st.session_state.messages.append({"role": "user", "content": user_input})
    omeji_zgodovino()

    try:
        # Pošlji v Groq model
        odgovor = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = odgovor.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": ai_text})
        omeji_zgodovino()

        # Pošlji novo vprašanje – počisti vnosno polje
        st.session_state.user_input = ""  # zdaj varno, ker imamo unikatni key

    except Exception as e:
        st.error(f"Napaka: {e}")
