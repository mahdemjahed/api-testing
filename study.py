import requests
import json
import os
import random

start = True
while start:
    user = input("Do you want to draw a Pokémon? Type 'yes' or 'no': \n")
    if user.lower() == "yes":
        pokeid = random.randint(1, 1025)  # You can change this ID to fetch different Pokémon

        try:
            # Fetch Pokémon data from PokeAPI
            poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokeid}")
            poke.raise_for_status()  # Raises an error for bad responses
            poke_dict = poke.json()

            # Create a dictionary with Pokémon information
            new_data = {
                "id": poke_dict["id"],
                "name": poke_dict["name"],
                "height": poke_dict["height"],
                "weight": poke_dict["weight"]
            }

            # File path
            file_path = 'poke.json'

            # Check if the file exists
            if os.path.exists(file_path):
                # Read existing data
                with open(file_path, 'r') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = {}
            else:
                existing_data = {}

            # Check if the Pokémon ID already exists in the data
            if str(new_data["id"]) not in existing_data:
                # Append new data only if the ID does not already exist
                existing_data[str(new_data["id"])] = new_data

                # Write the updated data back to the JSON file
                with open(file_path, 'w') as f:
                    json.dump(existing_data, f, indent=4)

            # Print Pokémon data in a nicely formatted way
            print("\nPokémon Data:")
            print("=" * 30)
            print(f"Name: {new_data['name'].capitalize()}")  # Capitalize the name for nicer output
            print(f"ID: {new_data['id']}")
            print(f"Height: {new_data['height']} decimeters")
            print(f"Weight: {new_data['weight']} hectograms")
            print("=" * 30)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching Pokémon data: {e}")
            continue  # Skip to the next iteration of the loop

    else:
        print("bye!")
        start = False
