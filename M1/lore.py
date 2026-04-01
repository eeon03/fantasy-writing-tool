import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

LORE_TYPES = [
    "Faction",
    "Historical Event",
    "Prophecy",
    "Mythology",
    "Cultural Tradition",
    "Artifact",
    "Organization",
    "Concept",
    "Other"
]

#add lore
def add_lore():
    print("\n--- Add New Lore Entry ---")
    print("\nLore types:")
    for i, t in enumerate(LORE_TYPES, 1):
        print(f"  {i}. {t}")
    
    type_choice = input("\nChoose type (number or type it out): ")
    
    try:
        lore_type = LORE_TYPES[int(type_choice) - 1]
    except (ValueError, IndexError):
        lore_type = type_choice.lower()
    
    lore = {}
    lore["name"] = input("\nName: ")
    lore["type"] = lore_type
    lore["summary"] = input("Summary (one or two sentences): ")
    lore["full_detail"] = input("Full detail: ")
    lore["related_nations"] = input("Related nations (comma separated): ").split(",")
    lore["related_characters"] = input("Related characters (comma separated): ").split(",")
    lore["related_locations"] = input("Related locations (comma separated): ").split(",")
    lore["tags"] = input("Tags for searching (comma separated — e.g. war, magic, religion): ").split(",")
    lore["notes"] = input("Notes: ")
    
    lore_data = storage.load("lore")
    lore_data[lore["name"].lower()] = lore
    storage.save("lore", lore_data)
    
    print(f"\n'{lore['name']}' saved.")

#view lore
def view_lore(name):
    lore_data = storage.load("lore")
    entry = lore_data.get(name.lower())
    
    if not entry:
        print(f"\nNo lore entry found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {entry['name']}")
    print(f"  Type: {entry.get('type', '').upper()}")
    print(f"{'='*40}")
    
    fields = [
        ("Summary", "summary"),
        ("Full detail", "full_detail"),
        ("Related nations", "related_nations"),
        ("Related characters", "related_characters"),
        ("Related locations", "related_locations"),
        ("Tags", "tags"),
        ("Notes", "notes"),
    ]
    
    for label, key in fields:
        value = entry.get(key, "")
        if isinstance(value, list):
            value = ", ".join(v.strip() for v in value if v.strip())
        if value:
            print(f"\n  {label.upper()}")
            print(f"    {value}")


def list_lore(filter_type=None):
    lore_data = storage.load("lore")
    
    if not lore_data:
        print("\nNo lore entries yet.")
        return
    
    entries = lore_data.values()
    
    if filter_type:
        entries = [e for e in entries 
                   if e.get("type", "").lower() == filter_type.lower()]
    
    if not entries:
        print(f"\nNo lore entries of type '{filter_type}'.")
        return
    
    label = f"({filter_type})" if filter_type else ""
    print(f"\n--- Lore Entries {label} ({len(list(entries))}) ---")
    
    entries = lore_data.values() if not filter_type else [
        e for e in lore_data.values() 
        if e.get("type", "").lower() == filter_type.lower()
    ]
    
    for entry in entries:
        print(f"  {entry['name']} — {entry.get('type', '')} | {entry.get('summary', '')[:60]}...")

#search lore
def search_lore(query):
    lore_data = storage.load("lore")
    query = query.lower()
    results = []
    
    for entry in lore_data.values():
        tags = " ".join(entry.get("tags", []))
        searchable = " ".join([
            entry.get("name", ""),
            entry.get("type", ""),
            entry.get("summary", ""),
            entry.get("full_detail", ""),
            entry.get("related_nations", [""])[0],
            entry.get("related_characters", [""])[0],
            tags,
        ]).lower()
        
        if query in searchable:
            results.append(entry)
    
    if not results:
        print(f"\nNo lore found matching '{query}'.")
        return
    
    print(f"\n--- Lore results for '{query}' ---")
    for entry in results:
        print(f"  {entry['name']} — {entry.get('type', '')}")
        print(f"    {entry.get('summary', '')[:80]}...")

#list lore by type
def list_by_type():
    lore_data = storage.load("lore")
    
    if not lore_data:
        print("\nNo lore entries yet.")
        return
    
    grouped = {}
    for entry in lore_data.values():
        t = entry.get("type", "other")
        if t not in grouped:
            grouped[t] = []
        grouped[t].append(entry["name"])
    
    print("\n--- Lore by Type ---")
    for lore_type, names in sorted(grouped.items()):
        print(f"\n  {lore_type.upper()} ({len(names)})")
        for name in names:
            print(f"    — {name}")

#edit lore
def edit_lore(name):
    lore_data = storage.load("lore")
    entry = lore_data.get(name.lower())
    
    if not entry:
        print(f"\nNo lore entry found: '{name}'.")
        return
    
    print(f"\n--- Editing {entry['name']} ---")
    print("Press enter to keep current value.\n")
    
    fields = [
        ("name", "Name", False),
        ("type", "Type", False),
        ("summary", "Summary", False),
        ("full_detail", "Full detail", False),
        ("related_nations", "Related nations (comma separated)", True),
        ("related_characters", "Related characters (comma separated)", True),
        ("related_locations", "Related locations (comma separated)", True),
        ("tags", "Tags (comma separated)", True),
        ("notes", "Notes", False),
    ]
    
    for key, label, is_list in fields:
        current = entry.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            entry[key] = new_value.split(",") if is_list else new_value
    
    lore_data[entry["name"].lower()] = entry
    storage.save("lore", lore_data)
    print(f"\n'{entry['name']}' updated.")

#delete lore
def delete_lore(name):
    lore_data = storage.load("lore")
    entry = lore_data.get(name.lower())
    
    if not entry:
        print(f"\nNo lore entry found: '{name}'.")
        return
    
    confirm = input(f"Are you sure you want to delete '{entry['name']}'? (y/n): ")
    if confirm.lower() == "y":
        del lore_data[name.lower()]
        storage.save("lore", lore_data)
        print(f"\n'{entry['name']}' deleted.")