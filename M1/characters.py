import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

#add character
def add_character():
    print("\n--- Add a New Character ---")

    character = {}

    #identity
    print("\n--- Identity ---")
    character["name"] = input("Name: ")
    character["aliases"] = input("Aliases/titles/nicknames (comma-separated): ").split(",")
    character["age"] = input("Age: ")
    character["gender"] = input("Gender: ")
    character["species"] = input("Species: ")
    character["culture"] = input("Culture/people: ")
    character["occupation"] = input("Occupation: ")
    character["status"] = input("Status (alive, deceased, unknown): ")
    character["role"] = input("Role in the story (protagonist, antagonist, supporting, etc.): ")

    #physical
    print("\n--- Physical Description ---")
    character["appearance"] = input("Appearance: ")
    character["mannerisms"] = input("Mannerisms (comma-separated): ").split(",")
    character["voice"] = input("Voice and speech style:")
    character["clothing"] = input("Clothing style: ")

    #phsychology - pyramid model
    print("\n--- The Defining Event ---")
    character["defining event"] = input("What specific event event created their wound: ")
    character["the_lie"] = input("What lie did they draw from it (first person): ")
    character["the_truth"] = input("What truth do they need to learn by the end: ")

    print("\n--- Core Flaws (from the lie) ---")
    character["core_flaws"] = input("Core flaws resulting from the lie (comma-separated): ").split(",")
    
    print("\n--- Lesser Flaws (from core flaws) ---")
    character["lesser_flaws"] = input("Lesser flaws others actually see (comma-separated): ").split(",")

    print("\n--- Surface Behaviors ---")
    character["behaviors_and_quirks"] = input("Typical behaviors, habits, quirks (comma-separated): ").split(",")
    character["contradictions"] = input("Ways they contradict the lie - moments their real self leaks through: ").split(",")
    character["fears"] = input("Fears (comma-separated): ").split(",")
    character["desires"] = input("What they want - surface desire and deeper need: ").split(",")
    character["beliefs"] = input("Beliefs about themselves, others, and the world: ").split(",")

    #relationships
    print("\n--- Relationships ---")
    character["family"] = input("Family relationships: ")
    character["friends"] = input("Friendships: ")
    character["enemies"] = input("Enemies/rivals: ")
    character["romantic"] = input("Romantic relationships: ")

    #story
    print("\n--- Story Details ---")
    character["arc"] = input("Character arc: ")
    character["secrets"] = input("Secrets (comma-separated): ").split(",")
    character["skills"] = input("Skills (comma-separated): ").split(",")
    character["magical_abilities"] = input("Magical abilities (comma-separated): ").split(",")
    character["items"] = input("Items (comma-separated): ").split(",")

    #voice and extra
    print("\n--- Voice and Extra Details ---")
    character["voice_samples"] = []
    print("Enter up to 3 sample dialogue lines (press enter to skip): ")
    for i in range(3):
        sample = input(f" Line {i+1}: ")
        if sample:
            character["voice_samples"].append(sample)

    character["themes"] = input("Themes this character explores (comma-separated): ").split(",")
    character["notes"] = input("Additional notes: ")

    #save character
    characters = storage.load("characters")
    characters[character["name"].lower()] = character
    storage.save("characters", characters)

    print(f"\nCharacter '{character['name']}' saved successfully.")

#view character
def view_character(name):
    characters = storage.load("characters")
    character = characters.get(name.lower())

    if not character:
        print(f"\nCharacter '{name}' not found.")
        return
    
    print(f"\n{'='*40}")
    print(f"Character '{character['name']}':")
    print(f"{'='*40}")

    sections = {
        "Identity": ["name", "aliases", "age"],
        "Physical": ["appearance", "mannerisms", "voice", "clothing"],
        "Psychology": ["defining event", "the_lie", "the_truth", "core_flaws", "lesser_flaws"],
        "Behaviors": ["behaviors_and_quirks", "contradictions", "fears", "desires", "beliefs"],
        "Relationships": ["family", "friends", "enemies", "romantic"],
        "Story": ["arc", "secrets", "skills", "magical_abilities", "items"],
        "Voice & Extra": ["voice_samples", "themes", "notes"]
    }

    for section, fields in sections.items():
        print(f"\n--- {section} ---")
        for field in fields:
            value = character.get(field)
            if isinstance(value, list):
                value = ", ".join(v.strip() for v in value if v.strip())
            if value:
                print(f" {field.replace('_', ' ').capitalize()}: {value}")

#list characters
def list_characters():
    characters = storage.load("characters")

    if not characters:
        print("\nNo characters yet.")
        return
    
    print(f"\n--- All Characters ({len(characters)}) ---")
    for key, character in characters.items():
        status = character.get("status", "unknown")
        role = character.get("role", "")
        print(f"   {character['name']} - {role} ({status})")

#search characters
def search_characters(query):
    characters = storage.load("characters")
    query = query.lower()
    results = []

    for character in characters.values():
        searchable = " ".join([
            character.get("name", ""),
            " ".join(character.get("aliases", [])),
            character.get("role", ""),
            character.get("species", ""),
            character.get("culture", ""),
            character.get("background", ""),
            character.get("personality", ""),
            character.get("skills", ""),
        ]).lower()

        if query in searchable:
            results.append(character)

    if not results:
        print(f"\nNo characters found matching '{query}'.")
        return
    
    print(f"\n--- Results for '{query}' ---")
    for character in results:
        print(f" {character['name']} - {character.get('role', '')}")

#edit character
def edit_character(name):
    characters = storage.load("characters")
    character = characters.get(name.lower())
    
    if not character:
        print(f"\nNo character found: '{name}'.")
        return
    
    print(f"\n--- Editing {character['name']} ---")
    print("Press enter to keep current value. Type new value to change it.\n")
    
    fields = [
        ("name", "Name"),
        ("aliases", "Aliases (comma separated)"),
        ("age", "Age"),
        ("gender", "Gender"),
        ("culture", "Culture"),
        ("status", "Status"),
        ("role", "Role"),
        ("appearance", "Appearance"),
        ("mannerisms", "Mannerisms (comma separated)"),
        ("voice", "Voice"),
        ("defining_event", "Defining event"),
        ("the_lie", "The lie they believe"),
        ("the_truth", "The truth they need to learn"),
        ("core_flaws", "Core flaws (comma separated)"),
        ("lesser_flaws", "Lesser flaws (comma separated)"),
        ("behaviours_and_quirks", "Behaviours and quirks (comma separated)"),
        ("contradictions", "Contradictions (comma separated)"),
        ("fears", "Fears (comma separated)"),
        ("desires", "Desires (comma separated)"),
        ("beliefs", "Beliefs"),
        ("arc", "Arc"),
        ("secrets", "Secrets (comma separated)"),
        ("skills", "Skills (comma separated)"),
        ("magic_ability", "Magic ability"),
        ("themes", "Themes (comma separated)"),
        ("notes", "Notes"),
    ]
    
    list_fields = {
        "aliases", "mannerisms", "core_flaws", "lesser_flaws",
        "behaviours_and_quirks", "contradictions", "fears",
        "desires", "secrets", "skills", "themes"
    }
    
    for key, label in fields:
        current = character.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            if key in list_fields:
                character[key] = new_value.split(",")
            else:
                character[key] = new_value
    
    # Handle voice samples separately
    print(f"\nVoice samples [{'; '.join(character.get('voice_samples', []))}]")
    update_samples = input("Update voice samples? (y/n): ")
    if update_samples.lower() == "y":
        character["voice_samples"] = []
        for i in range(3):
            sample = input(f"  Line {i+1}: ")
            if sample:
                character["voice_samples"].append(sample)
    
    characters[character["name"].lower()] = character
    storage.save("characters", characters)
    print(f"\n{character['name']} updated.")


#delete character
def delete_character(name):
    characters = storage.load("characters")
    character = characters.get(name.lower())
    
    if not character:
        print(f"\nNo character found: '{name}'.")
        return
    
    confirm = input(f"Are you sure you want to delete {character['name']}? (y/n): ")
    if confirm.lower() == "y":
        del characters[name.lower()]
        storage.save("characters", characters)
        print(f"\n{character['name']} deleted.")