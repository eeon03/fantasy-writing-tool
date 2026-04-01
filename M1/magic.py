import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

def add_magic_system():
    print("\n--- Add New Magic System ---")
    print("Fields are organised around Sanderson's Three Laws.")
    print("Press enter to skip any field and fill it in later.\n")
    
    magic = {}
    
    # Foundation
    print("  --- FOUNDATION ---")
    magic["name"] = input("Name: ")
    magic["type"] = input("Type (hard/soft/blend): ")
    magic["source"] = input("Source — where the power comes from: ")
    magic["physical_form"] = input("Physical form — what it looks like when used: ")
    magic["history"] = input("History: ")
    
    # First Law — understanding
    print("\n  --- FIRST LAW: UNDERSTANDING ---")
    print("  The more the reader understands, the more you can use it to solve plot.")
    magic["what_it_can_do"] = input("What it can do (comma separated capabilities): ").split(",")
    magic["how_it_is_used"] = input("How it is used — the mechanics: ")
    magic["what_is_knowable"] = input("What is knowable — the hard magic elements: ")
    magic["what_is_mysterious"] = input("What remains mysterious — the soft magic elements: ")
    magic["plot_problems_it_can_solve"] = input("Plot problems it could solve (comma separated): ").split(",")
    magic["reader_knowledge_level"] = input("How much does the reader understand vs the characters: ")
    
    # Second Law — limitations
    print("\n  --- SECOND LAW: LIMITATIONS ---")
    print("  Limits are more interesting than powers. This is where drama lives.")
    magic["cost"] = input("Cost — what using it takes from the user: ")
    magic["hard_limits"] = input("Hard limits — what it CANNOT do (comma separated): ").split(",")
    magic["soft_limits"] = input("Soft limits — conditional or difficult things (comma separated): ").split(",")
    magic["failure_states"] = input("Failure states — what happens when it goes wrong (comma separated): ").split(",")
    magic["counters"] = input("Counters — how it can be blocked or negated (comma separated): ").split(",")
    magic["dramatic_tension"] = input("Which limits create the most story tension: ")
    
    # Third Law — complexity
    print("\n  --- THIRD LAW: COMPLEXITY ---")
    print("  Explore what you have before adding something new.")
    magic["unexplored_potential"] = input("Unexplored potential in the existing system (comma separated): ").split(",")
    magic["planned_additions"] = input("Planned additions — justify each one (comma separated): ").split(",")
    magic["interactions"] = input("Interactions with other magic systems in your world: ")
    
    # Access & world context
    print("\n  --- ACCESS & WORLD CONTEXT ---")
    magic["who_can_use_it"] = input("Who can use it and why: ")
    magic["how_access_is_gained"] = input("How access is gained: ")
    magic["social_implications"] = input("Social implications of having or not having magic: ")
    magic["world_perception"] = input("How the world views magic users: ")
    magic["known_users"] = input("Known users (comma separated): ").split(",")
    magic["related_nations"] = input("Related nations (comma separated): ").split(",")
    magic["related_religions"] = input("Related religions (comma separated): ").split(",")
    magic["misconceptions"] = input("Common misconceptions about it: ")
    magic["notes"] = input("Notes: ")
    
    magic_data = storage.load("magic")
    magic_data[magic["name"].lower()] = magic
    storage.save("magic", magic_data)
    
    print(f"\n'{magic['name']}' saved.")


def view_magic(name):
    magic_data = storage.load("magic")
    magic = magic_data.get(name.lower())
    
    if not magic:
        print(f"\nNo magic system found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {magic['name'].upper()}")
    print(f"  Type: {magic.get('type', '')} | Source: {magic.get('source', '')}")
    print(f"{'='*40}")
    
    sections = {
        "Foundation": [
            ("Physical form", "physical_form"),
            ("History", "history"),
        ],
        "First Law — Understanding": [
            ("What it can do", "what_it_can_do"),
            ("How it is used", "how_it_is_used"),
            ("What is knowable", "what_is_knowable"),
            ("What is mysterious", "what_is_mysterious"),
            ("Plot problems it can solve", "plot_problems_it_can_solve"),
            ("Reader knowledge level", "reader_knowledge_level"),
        ],
        "Second Law — Limitations": [
            ("Cost", "cost"),
            ("Hard limits", "hard_limits"),
            ("Soft limits", "soft_limits"),
            ("Failure states", "failure_states"),
            ("Counters", "counters"),
            ("Dramatic tension", "dramatic_tension"),
        ],
        "Third Law — Complexity": [
            ("Unexplored potential", "unexplored_potential"),
            ("Planned additions", "planned_additions"),
            ("Interactions", "interactions"),
        ],
        "Access & World Context": [
            ("Who can use it", "who_can_use_it"),
            ("How access is gained", "how_access_is_gained"),
            ("Social implications", "social_implications"),
            ("World perception", "world_perception"),
            ("Known users", "known_users"),
            ("Related nations", "related_nations"),
            ("Related religions", "related_religions"),
            ("Misconceptions", "misconceptions"),
            ("Notes", "notes"),
        ]
    }
    
    for section, fields in sections.items():
        print(f"\n  {section.upper()}")
        for label, key in fields:
            value = magic.get(key, "")
            if isinstance(value, list):
                value = ", ".join(v.strip() for v in value if v.strip())
            if value:
                print(f"    {label}: {value}")


def list_magic():
    magic_data = storage.load("magic")
    
    if not magic_data:
        print("\nNo magic systems yet.")
        return
    
    print(f"\n--- Magic Systems ({len(magic_data)}) ---")
    for magic in magic_data.values():
        magic_type = magic.get("type", "")
        source = magic.get("source", "")
        print(f"  {magic['name']} — {magic_type} | source: {source}")


def edit_magic(name):
    magic_data = storage.load("magic")
    magic = magic_data.get(name.lower())
    
    if not magic:
        print(f"\nNo magic system found: '{name}'.")
        return
    
    print(f"\n--- Editing {magic['name']} ---")
    print("Press enter to keep current value.\n")
    
    fields = [
        ("name", "Name", False),
        ("type", "Type", False),
        ("source", "Source", False),
        ("physical_form", "Physical form", False),
        ("history", "History", False),
        ("what_it_can_do", "What it can do (comma separated)", True),
        ("how_it_is_used", "How it is used", False),
        ("what_is_knowable", "What is knowable", False),
        ("what_is_mysterious", "What is mysterious", False),
        ("plot_problems_it_can_solve", "Plot problems it can solve (comma separated)", True),
        ("reader_knowledge_level", "Reader knowledge level", False),
        ("cost", "Cost", False),
        ("hard_limits", "Hard limits (comma separated)", True),
        ("soft_limits", "Soft limits (comma separated)", True),
        ("failure_states", "Failure states (comma separated)", True),
        ("counters", "Counters (comma separated)", True),
        ("dramatic_tension", "Dramatic tension", False),
        ("unexplored_potential", "Unexplored potential (comma separated)", True),
        ("planned_additions", "Planned additions (comma separated)", True),
        ("interactions", "Interactions with other systems", False),
        ("who_can_use_it", "Who can use it", False),
        ("how_access_is_gained", "How access is gained", False),
        ("social_implications", "Social implications", False),
        ("world_perception", "World perception", False),
        ("known_users", "Known users (comma separated)", True),
        ("related_nations", "Related nations (comma separated)", True),
        ("related_religions", "Related religions (comma separated)", True),
        ("misconceptions", "Misconceptions", False),
        ("notes", "Notes", False),
    ]
    
    for key, label, is_list in fields:
        current = magic.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            magic[key] = new_value.split(",") if is_list else new_value
    
    magic_data[magic["name"].lower()] = magic
    storage.save("magic", magic_data)
    print(f"\n'{magic['name']}' updated.")


def check_violation(scene_text, system_name):
    magic_data = storage.load("magic")
    magic = magic_data.get(system_name.lower())
    
    if not magic:
        print(f"\nNo magic system found: '{system_name}'.")
        return
    
    hard_limits = [r.strip().lower() for r in magic.get("hard_limits", []) if r.strip()]
    
    if not hard_limits:
        print(f"\nNo hard limits defined for '{system_name}' yet.")
        return
    
    print(f"\n--- Checking scene against {magic['name']} hard limits ---\n")
    
    flags = []
    scene_lower = scene_text.lower()
    
    for limit in hard_limits:
        keywords = [w for w in limit.split() if len(w) > 4]
        for keyword in keywords:
            if keyword in scene_lower:
                flags.append(limit)
                break
    
    if flags:
        print("  POTENTIAL VIOLATIONS:")
        for flag in flags:
            print(f"  — '{flag}'")
        print("\n  Review your scene against these limits manually.")
    else:
        print("  No obvious violations detected.")
        print("  Always review manually — this is a guide not a guarantee.")


def sanderson_audit(name):
    magic_data = storage.load("magic")
    magic = magic_data.get(name.lower())
    
    if not magic:
        print(f"\nNo magic system found: '{name}'.")
        return
    
    print(f"\n--- Sanderson Audit: {magic['name']} ---")
    print("Checking your system against the Three Laws.\n")
    
    issues = []
    strengths = []
    
    # First Law check
    if magic.get("what_it_can_do") and any(v.strip() for v in magic["what_it_can_do"]):
        strengths.append("First Law: capabilities defined")
    else:
        issues.append("First Law: no capabilities defined — reader can't understand what it does")
    
    if magic.get("what_is_mysterious"):
        strengths.append("First Law: soft magic boundary defined")
    else:
        issues.append("First Law: soft magic boundary undefined — consider what should stay mysterious")
    
    if magic.get("plot_problems_it_can_solve") and any(v.strip() for v in magic["plot_problems_it_can_solve"]):
        strengths.append("First Law: plot utility mapped out")
    else:
        issues.append("First Law: no plot problems mapped — how will you use this magic to resolve story tension?")
    
    # Second Law check
    if magic.get("cost"):
        strengths.append("Second Law: cost defined")
    else:
        issues.append("Second Law: no cost defined — magic without cost creates no tension")
    
    if magic.get("hard_limits") and any(v.strip() for v in magic["hard_limits"]):
        strengths.append("Second Law: hard limits defined")
    else:
        issues.append("Second Law: no hard limits — what can it absolutely not do?")
    
    if magic.get("failure_states") and any(v.strip() for v in magic["failure_states"]):
        strengths.append("Second Law: failure states defined")
    else:
        issues.append("Second Law: no failure states — what happens when it goes wrong?")
    
    if magic.get("counters") and any(v.strip() for v in magic["counters"]):
        strengths.append("Second Law: counters defined")
    else:
        issues.append("Second Law: no counters — can anything stop it?")
    
    # Third Law check
    if magic.get("unexplored_potential") and any(v.strip() for v in magic["unexplored_potential"]):
        strengths.append("Third Law: unexplored potential logged")
    else:
        issues.append("Third Law: no unexplored potential listed — are you sure you've fully used what exists?")
    
    # Social check
    if magic.get("social_implications"):
        strengths.append("World context: social implications defined")
    else:
        issues.append("World context: no social implications — how does magic shape your world's power structures?")
    
    print("  STRENGTHS:")
    if strengths:
        for s in strengths:
            print(f"    + {s}")
    else:
        print("    None yet — keep building.")
    
    print("\n  GAPS TO ADDRESS:")
    if issues:
        for issue in issues:
            print(f"    — {issue}")
    else:
        print("    None — your system is structurally solid.")
    
    score = len(strengths)
    total = len(strengths) + len(issues)
    print(f"\n  Score: {score}/{total} criteria met.")