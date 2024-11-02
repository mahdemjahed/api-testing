import requests
import json
import os
import random

def fetch_pokemon_data(pokeid):
    """Fetch Pokémon data from PokeAPI."""
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeid}")
        response.raise_for_status()
        poke_dict = response.json()
        return {
            "id": poke_dict["id"],
            "name": poke_dict["name"],
            "height": poke_dict["height"],
            "weight": poke_dict["weight"]
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokémon data: {e}")
        return None

def load_existing_data(file_path):
    """Load existing Pokémon data from JSON file if it exists."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_data(file_path, data):
    """Save Pokémon data to JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def display_pokemon_data(data):
    """Display Pokémon data in a nicely formatted way."""
    print("\nPokémon Data:")
    print("=" * 30)
    print(f"Name: {data['name'].capitalize()}")
    print(f"ID: {data['id']}")
    print(f"Height: {data['height']} decimeters")
    print(f"Weight: {data['weight']} hectograms")
    print("=" * 30)

def main():
    file_path = 'poke.json'
    start = True

    while start:
        user = input("Do you want to draw a Pokémon? Type 'yes' or 'no': \n").strip().lower()
        if user == "yes":
            pokeid = random.randint(1, 1025)
            new_data = fetch_pokemon_data(pokeid)

            if new_data:
                existing_data = load_existing_data(file_path)

                if str(new_data["id"]) not in existing_data:
                    existing_data[str(new_data["id"])] = new_data
                    save_data(file_path, existing_data)

                display_pokemon_data(new_data)

        else:
            print("Goodbye!")
            start = False

if __name__ == "__main__":
    main()
