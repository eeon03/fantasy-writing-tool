import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage
import random

def add_language():
    print("\n--- Add New Language / Naming Culture ---")
    print("Define the rules and the generator learns from them.\n")
    
    language = {}
    
    # Identity
    language["name"] = input("Language name (e.g. Varenic, High Eldish, Kast Tongue): ")
    language["spoken_by"] = input("Spoken by (comma separated nations): ").split(",")
    language["sound_profile"] = input("Sound profile (e.g. harsh and guttural, flowing and soft, clicking): ")
    
    # Naming rules
    print("\n  --- NAMING RULES ---")
    print("  These are the rules the generator will follow.\n")
    
    print("  Male name rules — describe patterns e.g. 'ends in en, starts with consonant'")
    language["male_suffixes"] = input("  Male suffixes (comma separated e.g. en,an,or): ").split(",")
    language["male_prefixes"] = input("  Male prefixes (comma separated, press enter if none): ").split(",")
    
    print("\n  Female name rules")
    language["female_suffixes"] = input("  Female suffixes (comma separated e.g. na,ra,elle): ").split(",")
    language["female_prefixes"] = input("  Female prefixes (comma separated, press enter if none): ").split(",")
    
    print("\n  Place name rules")
    language["place_suffixes"] = input("  Place suffixes (comma separated e.g. vale,ford,heim): ").split(",")
    language["place_prefixes"] = input("  Place prefixes (comma separated, press enter if none): ").split(",")
    
    # Sound rules
    print("\n  --- SOUND RULES ---")
    language["forbidden_sounds"] = input("  Forbidden sounds/letters (comma separated e.g. x,z,ph): ").split(",")
    language["preferred_consonants"] = input("  Preferred consonants (comma separated e.g. r,v,th,dr): ").split(",")
    language["preferred_vowels"] = input("  Preferred vowels (comma separated e.g. a,e,ae,ie): ").split(",")
    language["syllable_range"] = input("  Syllable range (e.g. 2-3): ")
    
    # Examples — the generator learns from these
    print("\n  --- EXAMPLE NAMES ---")
    print("  Add names you've already created. The generator learns patterns from these.")
    language["example_male_names"] = input("  Example male names (comma separated): ").split(",")
    language["example_female_names"] = input("  Example female names (comma separated): ").split(",")
    language["example_place_names"] = input("  Example place names (comma separated): ").split(",")
    
    # Lexicon
    print("\n  --- MINI LEXICON ---")
    print("  Any words you've invented in this language.")
    print("  Format: word=meaning, word=meaning")
    raw_lexicon = input("  Words (comma separated, e.g. val=strength,keth=river): ")
    language["lexicon"] = {}
    if raw_lexicon.strip():
        for entry in raw_lexicon.split(","):
            if "=" in entry:
                word, meaning = entry.split("=", 1)
                language["lexicon"][word.strip()] = meaning.strip()
    
    language["notes"] = input("\nNotes: ")
    
    languages = storage.load("languages")
    languages[language["name"].lower()] = language
    storage.save("languages", languages)
    
    print(f"\n'{language['name']}' saved.")


def generate_names(language_name, name_type="male", count=5):
    languages = storage.load("languages")
    language = languages.get(language_name.lower())
    
    if not language:
        print(f"\nNo language found: '{language_name}'.")
        return
    
    print(f"\n--- Generating {count} {name_type} names ({language['name']}) ---\n")
    
    preferred_consonants = [
        c.strip() for c in language.get("preferred_consonants", []) 
        if c.strip()
    ]
    preferred_vowels = [
        v.strip() for v in language.get("preferred_vowels", []) 
        if v.strip()
    ]
    forbidden = [
        f.strip().lower() for f in language.get("forbidden_sounds", []) 
        if f.strip()
    ]
    
    # Fall back to generic sounds if none defined
    if not preferred_consonants:
        preferred_consonants = ["r","l","th","dr","str","v","k","m","n","s","t","b","d","f","g","h","j","w"]
    if not preferred_vowels:
        preferred_vowels = ["a","e","i","o","u","ae","ie","ei","ou"]
    
    # Get suffixes and prefixes for this name type
    if name_type == "male":
        suffixes = [s.strip() for s in language.get("male_suffixes", []) if s.strip()]
        prefixes = [p.strip() for p in language.get("male_prefixes", []) if p.strip()]
        examples = [n.strip() for n in language.get("example_male_names", []) if n.strip()]
    elif name_type == "female":
        suffixes = [s.strip() for s in language.get("female_suffixes", []) if s.strip()]
        prefixes = [p.strip() for p in language.get("female_prefixes", []) if p.strip()]
        examples = [n.strip() for n in language.get("example_female_names", []) if n.strip()]
    else:
        suffixes = [s.strip() for s in language.get("place_suffixes", []) if s.strip()]
        prefixes = [p.strip() for p in language.get("place_prefixes", []) if p.strip()]
        examples = [n.strip() for n in language.get("example_place_names", []) if n.strip()]
    
    if not suffixes:
        suffixes = [""]
    
    # Parse syllable range
    syllable_range = language.get("syllable_range", "2-3")
    try:
        parts = syllable_range.split("-")
        min_syl = int(parts[0].strip())
        max_syl = int(parts[1].strip()) if len(parts) > 1 else min_syl
    except (ValueError, IndexError):
        min_syl, max_syl = 2, 3
    
    generated = []
    attempts = 0
    
    while len(generated) < count and attempts < 200:
        attempts += 1
        
        # Build syllables
        num_syllables = random.randint(min_syl, max_syl)
        syllables = []
        
        for i in range(num_syllables):
            consonant = random.choice(preferred_consonants)
            vowel = random.choice(preferred_vowels)
            syllables.append(consonant + vowel)
        
        name = "".join(syllables)
        
        # Apply suffix
        suffix = random.choice(suffixes)
        if suffix and not name.endswith(suffix):
            # Remove trailing vowels before adding suffix if needed
            name = name.rstrip("aeiou") if suffix[0] in "aeiou" else name
            name = name + suffix
        
        # Apply prefix occasionally
        if prefixes and random.random() > 0.6:
            prefix = random.choice(prefixes)
            if prefix:
                name = prefix + name
        
        # Capitalise
        name = name.capitalize()
        
        # Check forbidden sounds
        name_lower = name.lower()
        if any(f in name_lower for f in forbidden if f):
            continue
        
        # Avoid duplicates and very short names
        if name not in generated and len(name) >= 3:
            generated.append(name)
    
    if generated:
        for name in generated:
            print(f"  {name}")
    else:
        print("  Could not generate names with current rules. Try adding more preferred consonants or vowels.")
    
    print(f"\nPress enter to regenerate, or type 'save' to save any of these to a character.")
    action = input("> ")
    
    if action.lower() != "save":
        return generated
    
    save_name = input("Which name to save, and to which character (name, character): ")
    if "," in save_name:
        chosen_name, character_name = save_name.split(",", 1)
        _save_name_to_character(chosen_name.strip(), character_name.strip())
    
    return generated


def _save_name_to_character(name, character_name):
    characters = storage.load("characters")
    character = characters.get(character_name.lower())
    
    if not character:
        print(f"\nNo character found: '{character_name}'.")
        return
    
    old_name = character.get("name", "")
    character["name"] = name
    
    del characters[character_name.lower()]
    characters[name.lower()] = character
    storage.save("characters", characters)
    
    print(f"\nCharacter renamed from '{old_name}' to '{name}'.")


def check_name(name, language_name, name_type="male"):
    languages = storage.load("languages")
    language = languages.get(language_name.lower())
    
    if not language:
        print(f"\nNo language found: '{language_name}'.")
        return
    
    print(f"\n--- Checking '{name}' against {language['name']} rules ---\n")
    
    name_lower = name.lower()
    issues = []
    passes = []
    
    # Check forbidden sounds
    forbidden = [f.strip().lower() for f in language.get("forbidden_sounds", []) if f.strip()]
    for f in forbidden:
        if f in name_lower:
            issues.append(f"Contains forbidden sound '{f}'")
    if not any(f in name_lower for f in forbidden if f):
        passes.append("No forbidden sounds")
    
    # Check suffix
    if name_type == "male":
        suffixes = [s.strip().lower() for s in language.get("male_suffixes", []) if s.strip()]
    elif name_type == "female":
        suffixes = [s.strip().lower() for s in language.get("female_suffixes", []) if s.strip()]
    else:
        suffixes = [s.strip().lower() for s in language.get("place_suffixes", []) if s.strip()]
    
    if suffixes:
        if any(name_lower.endswith(s) for s in suffixes):
            passes.append(f"Ends with correct suffix")
        else:
            issues.append(f"Doesn't end with expected suffix ({', '.join(suffixes)})")
    
    # Check preferred sounds present
    preferred_consonants = [c.strip() for c in language.get("preferred_consonants", []) if c.strip()]
    if preferred_consonants:
        if any(c in name_lower for c in preferred_consonants):
            passes.append("Contains preferred consonants")
        else:
            issues.append("Contains none of the preferred consonants")
    
    # Result
    if passes:
        print("  PASSES:")
        for p in passes:
            print(f"    + {p}")
    
    if issues:
        print("\n  ISSUES:")
        for issue in issues:
            print(f"    — {issue}")
        print(f"\n  '{name}' may not fit {language['name']} naming conventions.")
    else:
        print(f"\n  '{name}' fits {language['name']} naming conventions.")


def view_language(name):
    languages = storage.load("languages")
    language = languages.get(name.lower())
    
    if not language:
        print(f"\nNo language found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {language['name']}")
    print(f"{'='*40}")
    
    nations = ", ".join(v.strip() for v in language.get("spoken_by", []) if v.strip())
    print(f"\n  SPOKEN BY: {nations}")
    print(f"  SOUND PROFILE: {language.get('sound_profile', '')}")
    print(f"  SYLLABLE RANGE: {language.get('syllable_range', '')}")
    
    print(f"\n  NAMING RULES")
    
    male_suf = ", ".join(v.strip() for v in language.get("male_suffixes", []) if v.strip())
    female_suf = ", ".join(v.strip() for v in language.get("female_suffixes", []) if v.strip())
    place_suf = ", ".join(v.strip() for v in language.get("place_suffixes", []) if v.strip())
    forbidden = ", ".join(v.strip() for v in language.get("forbidden_sounds", []) if v.strip())
    
    if male_suf: print(f"    Male suffixes: {male_suf}")
    if female_suf: print(f"    Female suffixes: {female_suf}")
    if place_suf: print(f"    Place suffixes: {place_suf}")
    if forbidden: print(f"    Forbidden sounds: {forbidden}")
    
    print(f"\n  EXAMPLE NAMES")
    male_ex = ", ".join(v.strip() for v in language.get("example_male_names", []) if v.strip())
    female_ex = ", ".join(v.strip() for v in language.get("example_female_names", []) if v.strip())
    place_ex = ", ".join(v.strip() for v in language.get("example_place_names", []) if v.strip())
    
    if male_ex: print(f"    Male: {male_ex}")
    if female_ex: print(f"    Female: {female_ex}")
    if place_ex: print(f"    Places: {place_ex}")
    
    lexicon = language.get("lexicon", {})
    if lexicon:
        print(f"\n  LEXICON ({len(lexicon)} words)")
        for word, meaning in lexicon.items():
            print(f"    {word} = {meaning}")
    
    if language.get("notes"):
        print(f"\n  NOTES")
        print(f"    {language['notes']}")


def list_languages():
    languages = storage.load("languages")
    
    if not languages:
        print("\nNo languages yet.")
        return
    
    print(f"\n--- Languages ({len(languages)}) ---")
    for language in languages.values():
        nations = ", ".join(v.strip() for v in language.get("spoken_by", []) if v.strip())
        print(f"  {language['name']} — spoken by: {nations}")


def edit_language(name):
    languages = storage.load("languages")
    language = languages.get(name.lower())
    
    if not language:
        print(f"\nNo language found: '{name}'.")
        return
    
    print(f"\n--- Editing {language['name']} ---")
    print("Press enter to keep current value.\n")
    
    fields = [
        ("name", "Name", False),
        ("spoken_by", "Spoken by (comma separated)", True),
        ("sound_profile", "Sound profile", False),
        ("male_suffixes", "Male suffixes (comma separated)", True),
        ("male_prefixes", "Male prefixes (comma separated)", True),
        ("female_suffixes", "Female suffixes (comma separated)", True),
        ("female_prefixes", "Female prefixes (comma separated)", True),
        ("place_suffixes", "Place suffixes (comma separated)", True),
        ("place_prefixes", "Place prefixes (comma separated)", True),
        ("forbidden_sounds", "Forbidden sounds (comma separated)", True),
        ("preferred_consonants", "Preferred consonants (comma separated)", True),
        ("preferred_vowels", "Preferred vowels (comma separated)", True),
        ("syllable_range", "Syllable range (e.g. 2-3)", False),
        ("example_male_names", "Example male names (comma separated)", True),
        ("example_female_names", "Example female names (comma separated)", True),
        ("example_place_names", "Example place names (comma separated)", True),
        ("notes", "Notes", False),
    ]
    
    for key, label, is_list in fields:
        current = language.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            language[key] = new_value.split(",") if is_list else new_value
    
    languages[language["name"].lower()] = language
    storage.save("languages", languages)
    print(f"\n'{language['name']}' updated.")