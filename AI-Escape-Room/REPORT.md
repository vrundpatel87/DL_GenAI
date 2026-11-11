# AI-Powered Escape Room — Project Report

## 1. Introduction and objective

The objective of this project is to build an interactive escape-room application using a Large Language Model as a Game Master. The player wakes up inside a locked library and must investigate the desk, bookshelf, painting, locked drawer and exit door. The player communicates through natural-language messages, discovers clues, collects items and solves puzzles to escape.

The application is implemented in Python with Streamlit as the web interface and Google's Gemini API as the language model. The design is divided into two versions to demonstrate the improvement from a prompt-driven prototype to a more reliable application.

## 2. Version 1 — Interactive AI Escape Room

Version 1 uses Gemini as the primary Game Master. Streamlit provides a chat interface, and recent conversation messages are sent to Gemini along with the room setting and intended puzzle path. The model responds to player actions with descriptions and guidance. Conversation history is stored in Streamlit session state so the interaction can continue during the session.

The puzzle path is: inspect the bookshelf to discover the drawer combination, open the drawer to obtain the brass key, collect a UV lens from the desk, use the lens on the painting to reveal the exit code, and unlock the door with the key and code.

This approach is quick to implement and provides flexible natural-language interaction. However, the model may forget earlier events, invent objects, accept a player's false claim or describe an action as successful even when its prerequisites have not been met. The prompt alone cannot guarantee that the model always follows the puzzle rules.

## 3. Version 2 — Reliable AI Escape Room

Version 2 improves reliability by separating game logic from language generation. The complete game state is represented by a Python dictionary. It stores visited locations, inventory, drawer status, puzzle flags, door status, escape status and an action history.

A Python action-processing function interprets supported player commands and checks prerequisites before changing state. For example, the drawer opens only with the correct combination. The brass key is added to inventory only after the drawer opens. The painting's hidden clue can be revealed only after the UV lens has been collected. The exit requires both the brass key and the correct code.

Gemini no longer decides whether an action succeeds. It receives the already-approved event and outcome and is asked only to provide atmospheric narration. A deterministic Python message is used if Gemini is not configured or temporarily unavailable. Basic checks reject attempts to impersonate an administrator, override game rules, claim unsolved puzzles are complete or request secret solutions.

## 4. Testing and evaluation

The test suite checks the normal escape path and challenging inputs. It verifies that an incorrect drawer code does not open the drawer, a player without the key cannot escape, false claims do not update puzzle flags, administrator impersonation is blocked, secret-reveal requests are blocked, nonexistent objects are not collected and the UV lens cannot be used before it is obtained.

The automated tests are located in `tests/test_game_engine.py` and can be executed using `pytest -q`. The manual test plan in `TEST_PLAN.md` also asks the developer to compare the behaviour of both versions. Actual screenshots and observed results should be added after running the application.

## 5. Technologies and implementation decisions

- **Python:** implements state, action parsing and puzzle validation.
- **Streamlit:** provides the interactive web interface.
- **Google Gemini API:** generates Game Master dialogue and narration.
- **python-dotenv:** loads the API key from a local environment file.
- **pytest:** tests the deterministic game engine.

The API key is stored in `.env`, which is excluded from Git using `.gitignore`. `.env.example` documents the required configuration without containing a real credential. A local fallback makes the game playable even without a Gemini key.

## 6. Limitations and future improvements

Version 2 uses a rule-based natural-language parser, so some unusual phrasings may not be recognized. Its prompt-injection checks are basic and should not be treated as a complete security boundary. Game progress is stored in Streamlit session state rather than a permanent database. Future improvements could include a more capable intent classifier, persistent player profiles, multiple rooms, accessibility options, richer visual assets and expanded automated tests.

## 7. Conclusion

The project demonstrates how an LLM can make an interactive game more engaging and how deterministic application logic can make it more reliable. Version 1 demonstrates conversational AI integration, while Version 2 demonstrates structured state management, validation and separation of responsibilities. The key lesson is that an LLM should generate language, while the application should control important game rules and state transitions.
