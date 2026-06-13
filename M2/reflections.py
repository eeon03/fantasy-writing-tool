import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import storage
from datetime import datetime


def save_reflection(reflection_text, context="", linked_entry_type="", linked_entry_name=""):
    reflections = storage.load("reflections")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    reflection_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    reflections[reflection_id] = {
        "id": reflection_id,
        "timestamp": timestamp,
        "reflection": reflection_text,
        "context": context,
        "linked_entry_type": linked_entry_type,
        "linked_entry_name": linked_entry_name,
    }
    
    storage.save("reflections", reflections)
    print(f"\n  Reflection saved.")
    return reflection_id


def view_reflection(reflection_id):
    reflections = storage.load("reflections")
    entry = reflections.get(reflection_id)
    
    if not entry:
        print(f"\n  No reflection found with id '{reflection_id}'.")
        return
    
    print(f"\n  {'='*40}")
    print(f"  {entry.get('timestamp')}")
    print(f"  {'='*40}")
    
    if entry.get("linked_entry_name"):
        print(f"\n  Linked to: {entry.get('linked_entry_type')} — {entry.get('linked_entry_name')}")
    
    if entry.get("context"):
        print(f"\n  CONTEXT YOU WERE WORKING ON")
        print(f"  {entry.get('context')}")
    
    print(f"\n  YOUR REFLECTION")
    print(f"  {entry.get('reflection')}")


def list_reflections(linked_entry_name=""):
    reflections = storage.load("reflections")
    
    if not reflections:
        print("\n  No reflections yet.")
        return
    
    entries = list(reflections.values())
    entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    if linked_entry_name:
        entries = [
            e for e in entries
            if e.get("linked_entry_name", "").lower() == linked_entry_name.lower()
        ]
        if not entries:
            print(f"\n  No reflections linked to '{linked_entry_name}'.")
            return
        print(f"\n  --- Reflections for '{linked_entry_name}' ({len(entries)}) ---")
    else:
        print(f"\n  --- All Reflections ({len(entries)}) ---")
    
    for entry in entries:
        timestamp = entry.get("timestamp", "")
        reflection = entry.get("reflection", "")[:60]
        linked = entry.get("linked_entry_name", "")
        link_str = f" [{linked}]" if linked else ""
        print(f"  {timestamp}{link_str} — {reflection}...")


def push_to_world(reflection_id):
    reflections = storage.load("reflections")
    entry = reflections.get(reflection_id)
    
    if not entry:
        print(f"\n  No reflection found.")
        return
    
    print(f"\n  --- Push to World ---")
    print(f"  Reflection: {entry.get('reflection')[:100]}...")
    print("\n  Where to save this?")
    print("  1. As a lore entry")
    print("  2. As a character note")
    print("  3. As a decision log entry")
    
    choice = input("\n  Choose: ").strip()
    
    if choice == "1":
        from m1 import lore
        lore_data = storage.load("lore")
        name = input("  Lore entry name: ").strip()
        summary = input("  One line summary: ").strip()
        
        lore_data[name.lower()] = {
            "name": name,
            "type": "other",
            "summary": summary,
            "full_detail": entry.get("reflection"),
            "related_nations": [],
            "related_characters": [],
            "related_locations": [],
            "tags": ["from-reflection"],
            "notes": ""
        }
        storage.save("lore", lore_data)
        print(f"\n  Saved as lore entry '{name}'.")
    
    elif choice == "2":
        characters = storage.load("characters")
        name = input("  Which character to add a note to: ").strip()
        character = characters.get(name.lower())
        
        if not character:
            print(f"\n  No character found: '{name}'.")
            return
        
        existing_notes = character.get("notes", "")
        timestamp = entry.get("timestamp", "")
        character["notes"] = f"{existing_notes}\n[{timestamp}] {entry.get('reflection')}".strip()
        characters[name.lower()] = character
        storage.save("characters", characters)
        print(f"\n  Added to {name}'s notes.")
    
    elif choice == "3":
        decisions = storage.load("decisions")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        decision_id = datetime.now().strftime("%Y%m%d%H%M%S")
        reason = input("  One line reason for this decision: ").strip()
        
        decisions[decision_id] = {
            "id": decision_id,
            "timestamp": timestamp,
            "decision": entry.get("reflection"),
            "reason": reason,
            "source": "reflection"
        }
        storage.save("decisions", decisions)
        print(f"\n  Saved to decision log.")
    
    else:
        print("  Invalid choice.")


def search_reflections(query):
    reflections = storage.load("reflections")
    query = query.lower()
    results = []
    
    for entry in reflections.values():
        searchable = " ".join([
            entry.get("reflection", ""),
            entry.get("context", ""),
            entry.get("linked_entry_name", ""),
        ]).lower()
        
        if query in searchable:
            results.append(entry)
    
    if not results:
        print(f"\n  No reflections found matching '{query}'.")
        return
    
    results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    print(f"\n  --- Results for '{query}' ({len(results)}) ---")
    for entry in results:
        timestamp = entry.get("timestamp", "")
        reflection = entry.get("reflection", "")[:60]
        print(f"  {timestamp} — {reflection}...")