import streamlit as st
from dotenv import load_dotenv
from game_engine import new_game, process_v2_action, game_status
from gemini_client import narrate_v1, narrate_v2

load_dotenv()
st.set_page_config(page_title="AI Escape Room", page_icon="🗝️", layout="wide")

st.title("🗝️ AI-Powered Escape Room")
st.caption("A library mystery powered by Python, Streamlit and Google Gemini")

with st.sidebar:
    st.header("Game settings")
    version = st.radio("Choose implementation", ["Version 1 — Interactive AI", "Version 2 — Reliable AI"])
    st.markdown("---")
    st.markdown("**Objective**")
    st.write("Explore the library, solve its puzzles and escape through the four-digit door.")
    if st.button("🔄 Restart game", use_container_width=True):
        st.session_state.game = new_game()
        st.session_state.chat = []
        st.rerun()
    st.markdown("---")
    st.caption("Tip: try natural-language actions such as “examine the bookshelf” or “enter 2718 into the drawer”.")

if "game" not in st.session_state:
    st.session_state.game = new_game()
if "chat" not in st.session_state:
    st.session_state.chat = []

v2 = version.startswith("Version 2")
st.info("Version 2 validates every game-changing action in Python. Gemini is used only to narrate approved outcomes." if v2 else "Version 1 uses Gemini as the Game Master and keeps a conversation history. It is intentionally less restrictive.")

left, right = st.columns([2, 1])
with right:
    st.subheader("Room status")
    status = game_status(st.session_state.game)
    st.write(f"**Door:** {'Unlocked' if status['escaped'] else 'Locked'}")
    st.write(f"**Drawer:** {'Open' if status['drawer_open'] else 'Locked'}")
    st.write("**Inventory**")
    if status["inventory"]:
        for item in status["inventory"]:
            st.write(f"• {item}")
    else:
        st.caption("Nothing collected yet")
    if v2:
        st.write("**Solved puzzles**")
        st.write(f"{status['solved_count']} / 3")

with left:
    st.subheader("Game conversation")
    if not st.session_state.chat:
        st.session_state.chat.append({"role": "assistant", "content": "You wake in a silent old library. A heavy oak door is secured by a four-digit keypad. Around you are a desk, a bookshelf, a painting, a locked drawer and the exit door. Type what you want to do. Try examining objects first."})
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("What would you like to do?")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if v2:
            result = process_v2_action(st.session_state.game, prompt)
            narration = narrate_v2(prompt, result, st.session_state.game)
            reply = narration or result["message"]
            if result.get("message") and narration:
                reply += "\n\n" + result["message"]
        else:
            reply = narrate_v1(prompt, st.session_state.chat, st.session_state.game)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.rerun()

st.markdown("---")
with st.expander("How to play / puzzle hints"):
    st.markdown("""
    - **Bookshelf:** inspect the unusual books to discover the drawer combination.
    - **Drawer:** enter the four-digit combination to retrieve the brass key.
    - **Desk:** take the small UV lens.
    - **Painting:** use the UV lens to reveal the exit code.
    - **Exit:** use the brass key and enter the revealed four-digit code.

    In Version 2, use clear commands such as `examine bookshelf`, `enter 2718 in drawer`,
    `take UV lens`, `use UV lens on painting`, and `unlock door with key and code 0426`.
    """)
st.caption("Educational prototype. Game rules and secrets are intentionally stored in Python for Version 2.")
