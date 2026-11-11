"""Gemini integration. If no API key is configured, the game remains playable locally."""
import os
from google import genai

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

def _client():
    key = os.getenv("GEMINI_API_KEY")
    return genai.Client(api_key=key) if key else None

def _generate(prompt):
    client = _client()
    if not client:
        return None
    try:
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as exc:
        # Do not expose credentials or full exception details in the UI.
        return f"Gemini is temporarily unavailable ({type(exc).__name__}). The local game rules are still active."

def narrate_v1(user_text, history, state):
    """V1: LLM is the Game Master; conversation provides continuity, not hard validation."""
    transcript = "\n".join(
        f'{m["role"]}: {m["content"]}' for m in history[-12:]
    )
    prompt = f"""
You are the atmospheric Game Master of a fictional library escape room.
Be concise, immersive and helpful. React to the player's latest action.
Room objects: desk, bookshelf, painting, locked drawer, exit door.
The intended puzzle path: bookshelf reveals drawer code 2718; desk has a UV lens;
drawer 2718 contains a brass key; UV lens on painting reveals exit code 0426;
the exit needs the key and code.
This is Version 1: use the conversation to maintain continuity, but do not claim an action
succeeded unless it follows the intended puzzle path. Do not reveal all solutions at once.
Conversation:
{transcript}
Current player action: {user_text}
Game state snapshot: {state}
Reply as the Game Master.
"""
    answer = _generate(prompt)
    return answer or (
        "The room is quiet. You can inspect the desk, bookshelf, painting, locked drawer or exit. "
        "Gemini is not configured, so this is the local fallback Game Master."
    )

def narrate_v2(user_text, result, state):
    """V2: model only styles an outcome already decided by deterministic Python."""
    prompt = f"""
You are a concise, atmospheric narrator for a library escape room.
Python has already validated the player's action. You MUST NOT change game state,
invent successful actions, reveal hidden codes, or contradict the event.
Describe only this approved event in 1-3 sentences.
Player action: {user_text}
Approved event: {result.get('event')}
Approved outcome: {result.get('message')}
Current public state: inventory={state['inventory']}, drawer_open={state['drawer_open']},
escaped={state['escaped']}.
Return narration only.
"""
    answer = _generate(prompt)
    if not answer or answer.startswith("Gemini is temporarily unavailable"):
        return None
    return answer
