"""Deterministic game rules for Version 2; never let the LLM mutate this state."""
import re

def new_game():
    return {
        "visited": [],
        "inventory": [],
        "drawer_open": False,
        "drawer_attempts": 0,
        "bookshelf_clue_found": False,
        "desk_examined": False,
        "uv_lens_taken": False,
        "painting_revealed": False,
        "door_unlocked": False,
        "escaped": False,
        "actions": [],
    }

def game_status(state):
    return {
        "inventory": list(state["inventory"]),
        "drawer_open": state["drawer_open"],
        "escaped": state["escaped"],
        "solved_count": sum([
            state["bookshelf_clue_found"],
            state["drawer_open"],
            state["painting_revealed"] and state["escaped"],
        ]),
    }

def process_v2_action(state, text):
    """Parse a player's natural-language action and apply only authorized state changes."""
    raw = text.strip()
    msg = raw.lower()
    result = {"success": False, "event": "invalid", "message": "I don't recognize that action. Try examining the desk, bookshelf or painting."}

    # Requests to override rules or reveal hidden solutions are not game actions.
    adversarial = [
        r"\b(ignore|bypass|override)\b.*\b(rule|instruction|game|system)\b",
        r"\b(administrator|admin|developer)\b",
        r"\b(reveal|tell|show|print)\b.*\b(secret|all (the )?(codes|answers|solutions)|solution)\b",
        r"\bpretend\b.*\b(solved|unlocked|collected)\b",
    ]
    if any(re.search(p, msg) for p in adversarial):
        result.update(event="blocked", message="The library's rules cannot be changed by claims or instructions. Explore the room and solve the puzzles to proceed.")
        state["actions"].append({"input": raw, "event": result["event"]})
        return result

    if state["escaped"]:
        result.update(event="complete", success=True, message="You have already escaped. Start a new game to play again.")
    elif any(k in msg for k in ["bookshelf", "books", "bookcase"]):
        state["visited"].append("bookshelf")
        if any(v in msg for v in ["examine", "inspect", "look", "read", "check"]):
            state["bookshelf_clue_found"] = True
            result.update(success=True, event="bookshelf_clue", message="Four unusual books are marked in a deliberate order. Their handwritten digits read 2-7-1-8. This is likely the locked drawer combination.")
        else:
            result.update(event="bookshelf", message="The bookshelf is packed with old volumes. Four books look out of place. Examine them closely.")
    elif "desk" in msg:
        state["visited"].append("desk")
        if any(v in msg for v in ["take", "pick up", "collect", "grab"]) and ("lens" in msg or "uv" in msg):
            state["desk_examined"] = True
            if "UV lens" not in state["inventory"]:
                state["inventory"].append("UV lens")
            state["uv_lens_taken"] = True
            result.update(success=True, event="item_collected", message="You collect a small UV lens from the desk. It may reveal something invisible to the naked eye.")
        else:
            state["desk_examined"] = True
            result.update(success=True, event="desk", message="A dusty desk holds a small UV lens and a note: “Some truths appear only under another light.” You can take the UV lens.")
    elif "drawer" in msg:
        state["visited"].append("drawer")
        digits = re.search(r"\b(\d{4})\b", msg)
        if any(v in msg for v in ["open", "unlock", "enter", "code", "try"]) and digits:
            state["drawer_attempts"] += 1
            if digits.group(1) == "2718":
                state["drawer_open"] = True
                if "brass key" not in state["inventory"]:
                    state["inventory"].append("brass key")
                result.update(success=True, event="drawer_opened", message="The drawer clicks open. Inside is a brass key with a tiny label: EXIT. You collect the key.")
            else:
                result.update(event="wrong_code", message="The drawer keypad flashes red. That combination is incorrect. Re-examine the bookshelf for the clue.")
        elif state["drawer_open"]:
            result.update(success=True, event="drawer_opened", message="The drawer is already open and empty except for its lining.")
        else:
            result.update(event="drawer_locked", message="The drawer is locked and has a four-digit keypad. Find its combination before trying again.")
    elif "painting" in msg or "portrait" in msg:
        state["visited"].append("painting")
        if any(v in msg for v in ["use", "shine", "look through", "uv"]) and ("UV lens" in msg or "lens" in msg):
            if "UV lens" not in state["inventory"]:
                result.update(event="missing_item", message="You do not have a UV lens. Examine the desk and collect it first.")
            else:
                state["painting_revealed"] = True
                result.update(success=True, event="painting_code", message="Through the UV lens, glowing marks appear on the painting: 0426. This is the exit keypad code.")
        else:
            result.update(event="painting", message="The painting shows a stern librarian. A faint shimmer runs across the frame, but you cannot make out its meaning.")
    elif any(k in msg for k in ["door", "exit", "escape"]):
        state["visited"].append("door")
        code_match = re.search(r"\b(\d{4})\b", msg)
        has_key = "brass key" in state["inventory"]
        if ("unlock" in msg or "open" in msg or "enter" in msg or "escape" in msg) and code_match:
            if not has_key:
                result.update(event="missing_key", message="The keypad accepts the code, but the door's mechanical lock still needs a physical key. Find the brass key in the drawer.")
            elif not state["painting_revealed"]:
                result.update(event="missing_clue", message="You have a key, but you have not discovered the exit code. Use the UV lens on the painting.")
            elif code_match.group(1) != "0426":
                result.update(event="wrong_code", message="The door keypad flashes red. The code is incorrect. Check the painting with the UV lens.")
            else:
                state["door_unlocked"] = True
                state["escaped"] = True
                result.update(success=True, event="escaped", message="The brass key turns and the keypad accepts 0426. The library door swings open. You escaped! 🎉")
        else:
            result.update(event="door_locked", message="The exit has a four-digit keypad and a separate key lock. You need both the correct code and the brass key.")
    else:
        result.update(event="unknown", message="That object or action is not available in this library. Try the desk, bookshelf, painting, drawer or door.")

    state["actions"].append({"input": raw, "event": result["event"]})
    return result
