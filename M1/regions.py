import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import storage

#add region
def add_region():
    print("\n--- Add New Region ---")
    
    region = {}
    
    region["name"] = input("Name: ")
    region["type"] = input("Type (forest/mountain range/desert/tundra/etc): ")
    region["description"] = input("Description: ")
    region["climate"] = input("Climate: ")
    region["atmosphere"] = input("Atmosphere (mood — ancient, dangerous, sacred): ")
    region["history"] = input("History: ")
    region["significance"] = input("Significance (why it matters): ")
    region["dangers"] = input("Dangers (comma separated): ").split(",")
    region["secrets"] = input("Secrets (comma separated): ").split(",")
    region["notes"] = input("Notes: ")
    
    regions = storage.load("regions")
    regions[region["name"].lower()] = region
    storage.save("regions", regions)
    
    print(f"\n{region['name']} saved.")


def view_region(name):
    regions = storage.load("regions")
    region = regions.get(name.lower())
    
    if not region:
        print(f"\nNo region found: '{name}'.")
        return
    
    print(f"\n{'='*40}")
    print(f"  {region['name']}  —  {region.get('type', '')}")
    print(f"{'='*40}")
    
    fields = [
        ("Description", "description"),
        ("Climate", "climate"),
        ("Atmosphere", "atmosphere"),
        ("History", "history"),
        ("Significance", "significance"),
        ("Dangers", "dangers"),
        ("Secrets", "secrets"),
        ("Notes", "notes"),
    ]
    
    for label, key in fields:
        value = region.get(key, "")
        if isinstance(value, list):
            value = ", ".join(v.strip() for v in value if v.strip())
        if value:
            print(f"\n  {label.upper()}")
            print(f"    {value}")
    
    # Show child nations
    nations = storage.load("nations")
    children = [n for n in nations.values() 
                if n.get("region", "").lower() == name.lower()]
    
    if children:
        print(f"\n  NATIONS WITHIN THIS REGION")
        for nation in children:
            capital = nation.get("capital", "no capital set")
            print(f"    → {nation['name']} (capital: {capital})")
    else:
        print(f"\n  NATIONS WITHIN THIS REGION")
        print(f"    None added yet.")


def list_regions():
    regions = storage.load("regions")
    
    if not regions:
        print("\nNo regions yet.")
        return
    
    print(f"\n--- Regions ({len(regions)}) ---")
    for region in regions.values():
        print(f"  {region['name']} — {region.get('type', '')}")


def search_regions(query):
    regions = storage.load("regions")
    query = query.lower()
    results = []
    
    for region in regions.values():
        searchable = " ".join([
            region.get("name", ""),
            region.get("type", ""),
            region.get("description", ""),
            region.get("atmosphere", ""),
            region.get("history", ""),
        ]).lower()
        
        if query in searchable:
            results.append(region)
    
    if not results:
        print(f"\nNo regions found matching '{query}'.")
        return
    
    print(f"\n--- Results for '{query}' ---")
    for region in results:
        print(f"  {region['name']} — {region.get('type', '')}")


#edit region
def edit_region(name):
    regions = storage.load("regions")
    region = regions.get(name.lower())
    
    if not region:
        print(f"\nNo region found: '{name}'.")
        return
    
    print(f"\n--- Editing {region['name']} ---")
    print("Press enter to keep current value. Type new value to change it.\n")
    
    fields = [
        ("name", "Name"),
        ("type", "Type"),
        ("description", "Description"),
        ("climate", "Climate"),
        ("atmosphere", "Atmosphere"),
        ("history", "History"),
        ("significance", "Significance"),
        ("dangers", "Dangers (comma separated)"),
        ("secrets", "Secrets (comma separated)"),
        ("notes", "Notes"),
    ]
    
    list_fields = {"dangers", "secrets"}
    
    for key, label in fields:
        current = region.get(key, "")
        if isinstance(current, list):
            current_display = ", ".join(v.strip() for v in current if v.strip())
        else:
            current_display = current
        
        new_value = input(f"{label} [{current_display}]: ")
        
        if new_value.strip():
            if key in list_fields:
                region[key] = new_value.split(",")
            else:
                region[key] = new_value
    
    # Update key if name changed
    new_key = region["name"].lower()
    if new_key != name.lower():
        del regions[name.lower()]
    regions[new_key] = region
    storage.save("regions", regions)
    print(f"\n{region['name']} updated.")


#delete region
def delete_region(name):
    regions = storage.load("regions")
    region = regions.get(name.lower())
    
    if not region:
        print(f"\nNo region found: '{name}'.")
        return
    
    confirm = input(f"Are you sure you want to delete {region['name']}? (y/n): ")
    if confirm.lower() == "y":
        del regions[name.lower()]
        storage.save("regions", regions)
        print(f"\n{region['name']} deleted.")