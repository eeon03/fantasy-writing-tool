import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

def add_city():
    print("\n--- Add New City / Village / Landmark ---")
    
    city = {}
    
    city["name"] = input("Name: ")
    city["type"] = input("Type (capital city/city/town/village/fortress/ruin/landmark): ")
    city["nation"] = input("Nation it belongs to: ")
    city["population"] = input("Population (exact number or hamlet/town/city/metropolis): ")
    city["description"] = input("Description (architecture, layout, first impression): ")
    city["atmosphere"] = input("Atmosphere (mood — bustling, oppressive, dying, lawless): ")
    city["sounds_and_smells"] = input("Sounds and smells (sensory detail for writing): ")
    city["ruler"] = input("Ruler or controlling power: ")
    city["notable_inhabitants"] = input("Notable inhabitants (comma separated character names): ").split(",")
    city["factions"] = input("Factions present (comma separated): ").split(",")
    city["social_tensions"] = input("Social tensions: ")
    city["history"] = input("History: ")
    city["secrets"] = input("Secrets (comma separated): ").split(",")
    city["landmarks"] = input("Notable landmarks within (comma separated): ").split(",")
    city["connected_to"] = input("Connected to (comma separated city/location names): ").split(",")
    city["scenes_set_here"] = []
    city["notes"] = input("Notes: ")
    
    cities = storage.load("cities")
    cities[city["name"].lower()] = city
    storage.save("cities", cities)
    
    print(f"\n{city['name']} saved.")


def view_city(name):
    cities = storage.load("cities")
    city = cities.get(name.lower())
    
    if not city:
        print(f"\nNo city found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {city['name']}  —  {city.get('type', '')}")
    print(f"  {city.get('nation', '')}  |  Pop: {city.get('population', 'unknown')}")
    print(f"{'='*40}")
    
    fields = [
        ("Description", "description"),
        ("Atmosphere", "atmosphere"),
        ("Sounds & smells", "sounds_and_smells"),
        ("Ruler", "ruler"),
        ("Notable inhabitants", "notable_inhabitants"),
        ("Factions", "factions"),
        ("Social tensions", "social_tensions"),
        ("History", "history"),
        ("Secrets", "secrets"),
        ("Landmarks", "landmarks"),
        ("Connected to", "connected_to"),
        ("Scenes set here", "scenes_set_here"),
        ("Notes", "notes"),
    ]
    
    for label, key in fields:
        value = city.get(key, "")
        if isinstance(value, list):
            value = ", ".join(v.strip() for v in value if v.strip())
        if value:
            print(f"\n  {label.upper()}")
            print(f"    {value}")


def list_cities():
    cities = storage.load("cities")
    
    if not cities:
        print("\nNo cities yet.")
        return
    
    print(f"\n--- Cities & Villages ({len(cities)}) ---")
    for city in cities.values():
        nation = city.get("nation", "no nation set")
        city_type = city.get("type", "")
        print(f"  {city['name']} — {city_type} ({nation})")


def list_cities_in_nation(nation_name):
    cities = storage.load("cities")
    results = [c for c in cities.values()
               if c.get("nation", "").lower() == nation_name.lower()]
    
    if not results:
        print(f"\nNo cities found in '{nation_name}'.")
        return
    
    print(f"\n--- Cities in {nation_name} ({len(results)}) ---")
    for city in results:
        print(f"  {city['name']} — {city.get('type', '')}")


def search_cities(query):
    cities = storage.load("cities")
    query = query.lower()
    results = []
    
    for city in cities.values():
        searchable = " ".join([
            city.get("name", ""),
            city.get("type", ""),
            city.get("nation", ""),
            city.get("description", ""),
            city.get("atmosphere", ""),
            city.get("history", ""),
            city.get("social_tensions", ""),
        ]).lower()
        
        if query in searchable:
            results.append(city)
    
    if not results:
        print(f"\nNo cities found matching '{query}'.")
        return
    
    print(f"\n--- Results for '{query}' ---")
    for city in results:
        print(f"  {city['name']} — {city.get('type', '')} ({city.get('nation', '')})")


#edit city
def edit_city(name):
    cities = storage.load("cities")
    city = cities.get(name.lower())
    
    if not city:
        print(f"\nNo city found: '{name}'.")
        return
    
    print(f"\n--- Editing {city['name']} ---")
    print("Press enter to keep current value. Type new value to change it.\n")
    
    fields = [
        ("name", "Name"),
        ("type", "Type"),
        ("nation", "Nation"),
        ("population", "Population"),
        ("description", "Description"),
        ("atmosphere", "Atmosphere"),
        ("sounds_and_smells", "Sounds and smells"),
        ("ruler", "Ruler"),
        ("notable_inhabitants", "Notable inhabitants (comma separated)"),
        ("factions", "Factions (comma separated)"),
        ("social_tensions", "Social tensions"),
        ("history", "History"),
        ("secrets", "Secrets (comma separated)"),
        ("landmarks", "Landmarks (comma separated)"),
        ("connected_to", "Connected to (comma separated)"),
        ("scenes_set_here", "Scenes set here (comma separated)"),
        ("notes", "Notes"),
    ]
    
    list_fields = {"notable_inhabitants", "factions", "secrets", "landmarks", "connected_to", "scenes_set_here"}
    
    for key, label in fields:
        current = city.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            if key in list_fields:
                city[key] = new_value.split(",")
            else:
                city[key] = new_value
    
    # Update key if name changed
    new_key = city["name"].lower()
    if new_key != name.lower():
        del cities[name.lower()]
    cities[new_key] = city
    storage.save("cities", cities)
    print(f"\n{city['name']} updated.")


#delete city
def delete_city(name):
    cities = storage.load("cities")
    city = cities.get(name.lower())
    
    if not city:
        print(f"\nNo city found: '{name}'.")
        return
    
    confirm = input(f"Are you sure you want to delete {city['name']}? (y/n): ")
    if confirm.lower() == "y":
        del cities[name.lower()]
        storage.save("cities", cities)
        print(f"\n{city['name']} deleted.")