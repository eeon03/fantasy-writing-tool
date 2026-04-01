import sys
import os

from M1 import characters
from M1 import regions
from M1 import nations
from M1 import cities
from M1 import lore
from M1 import magic
from M1 import naming
import storage

def project_menu():
    while True:
        print("\n" + "="*40)
        print("   FANTASY WORLD ENGINE")
        print("="*40)
        
        projects = storage.list_projects()
        
        if projects:
            summary = storage.project_summary()
            print("\n  YOUR WORLDS:\n")
            for i, project in enumerate(projects, 1):
                counts = summary.get(project, {})
                total = sum(counts.values())
                details = []
                if counts.get("characters"):
                    details.append(
                        f"{counts['characters']} characters"
                    )
                if counts.get("nations"):
                    details.append(
                        f"{counts['nations']} nations"
                    )
                if counts.get("cities"):
                    details.append(
                        f"{counts['cities']} cities"
                    )
                detail_str = (
                    ", ".join(details) if details
                    else "empty"
                )
                print(f"  {i}. {project}  ({detail_str})")
        else:
            print("\n  No worlds yet. Create one to get started.")
        
        print("\n  N. New world")
        print("  R. Rename a world")
        print("  D. Delete a world")
        print("  0. Exit")
        
        choice = input("\n  Choose a world or option: ").strip()
        
        if choice == "0":
            print("\n  Goodbye.\n")
            sys.exit()
        
        elif choice.upper() == "N":
            create_project_flow()
        
        elif choice.upper() == "R":
            if not projects:
                print("\n  No worlds to rename.")
                continue
            name = input("  World to rename: ").strip()
            new_name = input("  New name: ").strip()
            success, result = storage.rename_project(name, new_name)
            if success:
                print(f"\n  Renamed to '{result}'.")
            else:
                print(f"\n  Could not rename: {result}")
        
        elif choice.upper() == "D":
            if not projects:
                print("\n  No worlds to delete.")
                continue
            name = input(
                "  World to delete (type name exactly): "
            ).strip()
            confirm = input(
                f"  Delete '{name}'? This cannot be undone. (yes/no): "
            ).strip()
            if confirm.lower() == "yes":
                success = storage.delete_project(name)
                if success:
                    print(f"\n  '{name}' deleted.")
                else:
                    print(f"\n  No world found called '{name}'.")
        
        elif choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(projects):
                selected = projects[index]
                storage.set_project(selected)
                print(f"\n  Opening '{selected}'...")
                world_menu()
            else:
                print("\n  Invalid choice.")
        
        else:
            print("\n  Invalid choice.")


def create_project_flow():
    print("\n  --- Create New World ---")
    name = input("  World name: ").strip()
    
    if not name:
        print("  Name cannot be empty.")
        return
    
    success, clean_name = storage.create_project(name)
    
    if not success:
        print(f"\n  A world called '{clean_name}' already exists.")
        return
    
    storage.set_project(clean_name)
    print(f"\n  '{clean_name}' created. Opening your new world...")
    world_menu()


def world_menu():
    while True:
        project = storage.get_project()
        print(f"\n  {'='*40}")
        print(f"   {project.upper()}")
        print(f"  {'='*40}")
        print("  1. Characters")
        print("  2. Locations")
        print("  3. Lore")
        print("  4. Magic Systems")
        print("  5. Naming & Languages")
        print("  0. Back to worlds")
        
        choice = input("\n  Choose: ").strip()
        
        if choice == "1":
            characters_menu()
        elif choice == "2":
            locations_menu()
        elif choice == "3":
            lore_menu()
        elif choice == "4":
            magic_menu()
        elif choice == "5":
            naming_menu()
        elif choice == "0":
            break
        else:
            print("  Invalid choice.")


def characters_menu():
    while True:
        print("\n    --- Characters ---")
        print("    1. Add character")
        print("    2. View character")
        print("    3. List all characters")
        print("    4. Search characters")
        print("    5. Edit character")
        print("    0. Back")
        
        choice = input("\n    Choose: ").strip()
        
        if choice == "1":
            characters.add_character()
        elif choice == "2":
            name = input("    Character name: ")
            characters.view_character(name)
        elif choice == "3":
            characters.list_characters()
        elif choice == "4":
            query = input("    Search query: ")
            characters.search_characters(query)
        elif choice == "5":
            name = input("    Character name to edit: ")
            characters.edit_character(name)
        elif choice == "0":
            break
        else:
            print("    Invalid choice.")


def locations_menu():
    while True:
        print("\n    --- Locations ---")
        print("    1. Regions")
        print("    2. Nations")
        print("    3. Cities & Villages")
        print("    0. Back")
        
        choice = input("\n    Choose: ").strip()
        
        if choice == "1":
            regions_menu()
        elif choice == "2":
            nations_menu()
        elif choice == "3":
            cities_menu()
        elif choice == "0":
            break
        else:
            print("    Invalid choice.")


def regions_menu():
    while True:
        print("\n      --- Regions ---")
        print("      1. Add region")
        print("      2. View region")
        print("      3. List all regions")
        print("      4. Search regions")
        print("      5. Edit region")
        print("      0. Back")
        
        choice = input("\n      Choose: ").strip()
        
        if choice == "1":
            regions.add_region()
        elif choice == "2":
            name = input("      Region name: ")
            regions.view_region(name)
        elif choice == "3":
            regions.list_regions()
        elif choice == "4":
            query = input("      Search query: ")
            regions.search_regions(query)
        elif choice == "5":
            name = input("      Region name to edit: ")
            regions.edit_region(name)
        elif choice == "0":
            break
        else:
            print("      Invalid choice.")


def nations_menu():
    while True:
        print("\n      --- Nations ---")
        print("      1. Add nation")
        print("      2. View nation")
        print("      3. List all nations")
        print("      4. Search nations")
        print("      5. Edit nation")
        print("      0. Back")
        
        choice = input("\n      Choose: ").strip()
        
        if choice == "1":
            nations.add_nation()
        elif choice == "2":
            name = input("      Nation name: ")
            nations.view_nation(name)
        elif choice == "3":
            nations.list_nations()
        elif choice == "4":
            query = input("      Search query: ")
            nations.search_nations(query)
        elif choice == "5":
            name = input("      Nation name to edit: ")
            nations.edit_nation(name)
        elif choice == "0":
            break
        else:
            print("      Invalid choice.")


def cities_menu():
    while True:
        print("\n      --- Cities & Villages ---")
        print("      1. Add city or village")
        print("      2. View city or village")
        print("      3. List all cities")
        print("      4. Search cities")
        print("      5. Edit city or village")
        print("      6. List cities in a nation")
        print("      0. Back")
        
        choice = input("\n      Choose: ").strip()
        
        if choice == "1":
            cities.add_city()
        elif choice == "2":
            name = input("      City name: ")
            cities.view_city(name)
        elif choice == "3":
            cities.list_cities()
        elif choice == "4":
            query = input("      Search query: ")
            cities.search_cities(query)
        elif choice == "5":
            name = input("      City name to edit: ")
            cities.edit_city(name)
        elif choice == "6":
            nation = input("      Nation name: ")
            cities.list_cities_in_nation(nation)
        elif choice == "0":
            break
        else:
            print("      Invalid choice.")


def lore_menu():
    while True:
        print("\n    --- Lore ---")
        print("    1. Add lore entry")
        print("    2. View lore entry")
        print("    3. List all lore")
        print("    4. List lore by type")
        print("    5. Search lore")
        print("    6. Edit lore entry")
        print("    0. Back")
        
        choice = input("\n    Choose: ").strip()
        
        if choice == "1":
            lore.add_lore()
        elif choice == "2":
            name = input("    Lore entry name: ")
            lore.view_lore(name)
        elif choice == "3":
            lore.list_lore()
        elif choice == "4":
            lore.list_by_type()
        elif choice == "5":
            query = input("    Search query: ")
            lore.search_lore(query)
        elif choice == "6":
            name = input("    Lore entry name to edit: ")
            lore.edit_lore(name)
        elif choice == "0":
            break
        else:
            print("    Invalid choice.")


def magic_menu():
    while True:
        print("\n    --- Magic Systems ---")
        print("    1. Add magic system")
        print("    2. View magic system")
        print("    3. List all magic systems")
        print("    4. Edit magic system")
        print("    5. Sanderson audit")
        print("    6. Check scene for violations")
        print("    0. Back")
        
        choice = input("\n    Choose: ").strip()
        
        if choice == "1":
            magic.add_magic_system()
        elif choice == "2":
            name = input("    Magic system name: ")
            magic.view_magic(name)
        elif choice == "3":
            magic.list_magic()
        elif choice == "4":
            name = input("    Magic system name to edit: ")
            magic.edit_magic(name)
        elif choice == "5":
            name = input("    Magic system name: ")
            magic.sanderson_audit(name)
        elif choice == "6":
            name = input("    Magic system name: ")
            scene = input("    Paste scene text: ")
            magic.check_violation(scene, name)
        elif choice == "0":
            break
        else:
            print("    Invalid choice.")

def naming_menu():
    while True:
        print("\n    --- Naming & Languages ---")
        print("    1. Add language")
        print("    2. View language")
        print("    3. List all languages")
        print("    4. Edit language")
        print("    5. Generate names")
        print("    6. Check a name")
        print("    0. Back")
        
        choice = input("\n    Choose: ").strip()
        
        if choice == "1":
            naming.add_language()
        elif choice == "2":
            name = input("    Language name: ")
            naming.view_language(name)
        elif choice == "3":
            naming.list_languages()
        elif choice == "4":
            name = input("    Language name to edit: ")
            naming.edit_language(name)
        elif choice == "5":
            lang = input("    Language name: ")
            name_type = input("    Type (male/female/place): ")
            count = input("    How many names: ")
            naming.generate_names(lang, name_type, int(count))
        elif choice == "6":
            name = input("    Name to check: ")
            lang = input("    Language name: ")
            name_type = input("    Type (male/female/place): ")
            naming.check_name(name, lang, name_type)
        elif choice == "0":
            break
        else:
            print("    Invalid choice.")

project_menu()