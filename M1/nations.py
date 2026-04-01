import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

#add nation
def add_nation():
    print("\n--- Add New Nation ---")
    
    nation = {}
    
    nation["name"] = input("Name: ")
    nation["region"] = input("Region it sits within: ")
    nation["capital"] = input("Capital city (add the city later in cities.py): ")
    nation["government"] = input("Government type: ")
    nation["current_ruler"] = input("Current ruler (character name): ")
    nation["culture"] = input("Culture and customs: ")
    nation["military"] = input("Military strength and notes: ")
    nation["economy"] = input("Economy — what they produce and trade: ")
    nation["religion"] = input("Dominant religion: ")
    nation["allies"] = input("Allied nations (comma separated): ").split(",")
    nation["enemies"] = input("Enemy nations (comma separated): ").split(",")
    nation["internal_tensions"] = input("Internal tensions: ")
    nation["history"] = input("History: ")
    nation["secrets"] = input("Secrets (comma separated): ").split(",")
    nation["naming_language"] = input("Naming language/culture: ")
    nation["notes"] = input("Notes: ")
    
    nations = storage.load("nations")
    nations[nation["name"].lower()] = nation
    storage.save("nations", nations)
    
    print(f"\n{nation['name']} saved.")

#view nation
def view_nation(name):
    nations = storage.load("nations")
    nation = nations.get(name.lower())
    
    if not nation:
        print(f"\nNo nation found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {nation['name']}")
    print(f"{'='*40}")
    
    fields = [
        ("Region", "region"),
        ("Government", "government"),
        ("Current ruler", "current_ruler"),
        ("Culture", "culture"),
        ("Military", "military"),
        ("Economy", "economy"),
        ("Religion", "religion"),
        ("Allies", "allies"),
        ("Enemies", "enemies"),
        ("Internal tensions", "internal_tensions"),
        ("History", "history"),
        ("Secrets", "secrets"),
        ("Naming language", "naming_language"),
        ("Notes", "notes"),
    ]
    
    for label, key in fields:
        value = nation.get(key, "")
        if isinstance(value, list):
            value = ", ".join(v.strip() for v in value if v.strip())
        if value:
            print(f"\n  {label.upper()}")
            print(f"    {value}")
    
    # Show child cities
    cities = storage.load("cities")
    children = [c for c in cities.values()
                if c.get("nation", "").lower() == name.lower()]
    
    if children:
        print(f"\n  CITIES & VILLAGES")
        for city in children:
            city_type = city.get("type", "")
            population = city.get("population", "")
            print(f"    → {city['name']} ({city_type}, {population})")
    else:
        print(f"\n  CITIES & VILLAGES")
        print(f"    None added yet.")

#list nations
def list_nations():
    nations = storage.load("nations")
    
    if not nations:
        print("\nNo nations yet.")
        return
    
    print(f"\n--- Nations ({len(nations)}) ---")
    for nation in nations.values():
        region = nation.get("region", "no region set")
        government = nation.get("government", "")
        print(f"  {nation['name']} — {government} ({region})")

#search nations
def search_nations(query):
    nations = storage.load("nations")
    query = query.lower()
    results = []
    
    for nation in nations.values():
        searchable = " ".join([
            nation.get("name", ""),
            nation.get("region", ""),
            nation.get("government", ""),
            nation.get("culture", ""),
            nation.get("history", ""),
            nation.get("economy", ""),
        ]).lower()
        
        if query in searchable:
            results.append(nation)
    
    if not results:
        print(f"\nNo nations found matching '{query}'.")
        return
    
    print(f"\n--- Results for '{query}' ---")
    for nation in results:
        print(f"  {nation['name']} — {nation.get('region', '')}")


#edit nation
def edit_nation(name):
    nations = storage.load("nations")
    nation = nations.get(name.lower())
    
    if not nation:
        print(f"\nNo nation found: '{name}'.")
        return
    
    print(f"\n--- Editing {nation['name']} ---")
    print("Press enter to keep current value. Type new value to change it.\n")
    
    fields = [
        ("name", "Name"),
        ("region", "Region"),
        ("capital", "Capital"),
        ("government", "Government"),
        ("current_ruler", "Current ruler"),
        ("culture", "Culture"),
        ("military", "Military"),
        ("economy", "Economy"),
        ("religion", "Religion"),
        ("allies", "Allies (comma separated)"),
        ("enemies", "Enemies (comma separated)"),
        ("internal_tensions", "Internal tensions"),
        ("history", "History"),
        ("secrets", "Secrets (comma separated)"),
        ("naming_language", "Naming language"),
        ("notes", "Notes"),
    ]
    
    list_fields = {"allies", "enemies", "secrets"}
    
    for key, label in fields:
        current = nation.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            if key in list_fields:
                nation[key] = new_value.split(",")
            else:
                nation[key] = new_value
    
    # Update key if name changed
    new_key = nation["name"].lower()
    if new_key != name.lower():
        del nations[name.lower()]
    nations[new_key] = nation
    storage.save("nations", nations)
    print(f"\n{nation['name']} updated.")


#delete nation
def delete_nation(name):
    nations = storage.load("nations")
    nation = nations.get(name.lower())
    
    if not nation:
        print(f"\nNo nation found: '{name}'.")
        return
    
    confirm = input(f"Are you sure you want to delete {nation['name']}? (y/n): ")
    if confirm.lower() == "y":
        del nations[name.lower()]
        storage.save("nations", nations)
        print(f"\n{nation['name']} deleted.")