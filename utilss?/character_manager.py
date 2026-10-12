import json
import os

CHARACTERS_FILE = os.path.join("data", "characters.json")

def load_characters():
    """Reads and returns the list of characters from the JSON file."""
    if not os.path.exists(CHARACTERS_FILE):
        return []
    try:
        with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_character(name: str, personality: str, backstory: str, visual_traits: str):
    """Adds or updates a character sheet in characters.json."""
    characters = load_characters()
    
    new_character = {
        "name": name,
        "personality": personality,
        "backstory": backstory,
        "visual_traits": visual_traits
    }
    
    # Overwrite if character name exists, otherwise append
    characters = [c for c in characters if c["name"].lower() != name.lower()]
    characters.append(new_character)
    
    with open(CHARACTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(characters, f, indent=4)
    
    return new_character

def format_character_sheet_for_prompt():
    """Formats character sheets into clean text to inject into chapter prompts."""
    characters = load_characters()
    if not characters:
        return "No specific character traits registered."
    
    formatted = ""
    for idx, c in enumerate(characters, 1):
        formatted += f"\n--- Character {idx}: {c['name']} ---\n"
        formatted += f"Personality: {c['personality']}\n"
        formatted += f"Backstory: {c['backstory']}\n"
        formatted += f"Visual Traits: {c['visual_traits']}\n"
    return formatted