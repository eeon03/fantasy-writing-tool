import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import anthropic
import storage
from config import ANTHROPIC_API_KEY

client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def build_world_context():
    context_parts = []

    characters = storage.load("characters")
    if characters:
        context_parts.append("CHARACTERS:")
        for character in characters.values():
            name = character.get("name", "")
            role = character.get("role", "")
            backstory = character.get("backstory", "")[:150]
            the_lie = character.get("the_lie", "")
            arc = character.get("arc", "")
            line = f"  - {name} ({role})"
            if backstory:
                line += f": {backstory}"
            if the_lie:
                line += f" | Lie: {the_lie}"
            if arc:
                line += f" | Arc: {arc}"
            context_parts.append(line)

    regions = storage.load("regions")
    if regions:
        context_parts.append("\nREGIONS:")
        for region in regions.values():
            name = region.get("name", "")
            atmosphere = region.get("atmosphere", "")
            context_parts.append(f"  - {name}: {atmosphere}")

    nations = storage.load("nations")
    if nations:
        context_parts.append("\nNATIONS:")
        for nation in nations.values():
            name = nation.get("name", "")
            government = nation.get("government", "")
            tensions = nation.get("internal_tensions", "")
            line = f"  - {name} ({government})"
            if tensions:
                line += f" | Tensions: {tensions}"
            context_parts.append(line)

    lore_data = storage.load("lore")
    if lore_data:
        context_parts.append("\nKEY LORE:")
        for entry in list(lore_data.values())[:5]:
            name = entry.get("name", "")
            summary = entry.get("summary", "")[:100]
            context_parts.append(f"  - {name}: {summary}")

    magic_data = storage.load("magic")
    if magic_data:
        context_parts.append("\nMAGIC SYSTEMS:")
        for magic in magic_data.values():
            name = magic.get("name", "")
            cost = magic.get("cost", "")
            hard_limits = magic.get("hard_limits", [])
            limits_str = ", ".join(
                h.strip() for h in hard_limits if h.strip()
            )[:100]
            line = f"  - {name}"
            if cost:
                line += f" | Cost: {cost}"
            if limits_str:
                line += f" | Hard limits: {limits_str}"
            context_parts.append(line)

    if not context_parts:
        return "The writer's world is still being built. No entries yet."

    return "\n".join(context_parts)


def build_focus_context(entry_type, entry_name):
    entry_type = entry_type.lower()
    data = storage.load(entry_type)

    if not data:
        return ""

    entry = data.get(entry_name.lower())

    if not entry:
        return ""

    lines = [f"FOCUS ENTRY — {entry_type.upper()}: {entry_name}\n"]

    for key, value in entry.items():
        if isinstance(value, list):
            value = ", ".join(v.strip() for v in value if v.strip())
        if value and str(value).strip():
            lines.append(f"  {key.replace('_', ' ').capitalize()}: {value}")

    return "\n".join(lines)


def send_spark(user_attempt, focus_context="", mode="general"):
    world_context = build_world_context()

    if mode == "focus" and focus_context:
        context_block = f"""You are a creative writing sparring partner for an epic fantasy writer.

Here is their world:
{world_context}

They are specifically focusing on this:
{focus_context}

Your job is to destabilise their thinking — not write for them.
Return ONLY a fragment. This means one of:
- A single probing question
- A tension or contradiction to consider
- 2-3 evocative words
- A what-if that subverts what they wrote

RULES:
- Maximum 3 lines total
- Never write scenes, dialogue, or narrative prose
- Never complete their idea — crack it open
- Be specific to their world, not generic
- No preamble, no explanation, just the fragment"""

    else:
        context_block = f"""You are a creative writing sparring partner for an epic fantasy writer.

Here is their world:
{world_context}

Your job is to destabilise their thinking — not write for them.
Return ONLY a fragment. This means one of:
- A single probing question
- A tension or contradiction to consider
- 2-3 evocative words
- A what-if that subverts what they wrote

RULES:
- Maximum 3 lines total
- Never write scenes, dialogue, or narrative prose
- Never complete their idea — crack it open
- Be specific to their world, not generic
- No preamble, no explanation, just the fragment"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=150,
            system=context_block,
            messages=[
                {
                    "role": "user",
                    "content": f"I am working on: {user_attempt}"
                }
            ]
        )

        response = message.content[0].text.strip()
        return response

    except anthropic.AuthenticationError:
        return "ERROR: Invalid API key. Check your config.py file."

    except anthropic.RateLimitError:
        return "ERROR: Rate limit hit. Wait a moment and try again."

    except anthropic.APIConnectionError:
        return "ERROR: Could not connect. Check your internet connection."

    except Exception as e:
        return f"ERROR: Something went wrong — {str(e)}"


def test_connection():
    print("\n--- Testing API connection ---")

    try:
        message = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=50,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly three words: connection is working"
                }
            ]
        )

        response = message.content[0].text.strip()
        print(f"Connection successful: '{response}'")
        return True

    except anthropic.AuthenticationError:
        print("FAILED: Invalid API key. Check config.py.")
        return False

    except anthropic.APIConnectionError:
        print("FAILED: Could not connect. Check internet.")
        return False

    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False