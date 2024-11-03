import requests
import json
import os
import random
import sqlite3  # Use sqlite3 instead of MySQL connector

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

def display_pokemon_data(data):
    """Display Pokémon data in a nicely formatted way."""
    print("\nPokémon Data:")
    print("=" * 30)
    print(f"Name: {data['name'].capitalize()}")
    print(f"ID: {data['id']}")
    print(f"Height: {data['height']} decimeters")
    print(f"Weight: {data['weight']} hectograms")
    print("=" * 30)

def insert_pokemon_data(cursor, data):
    """Insert Pokémon data into the database."""
    insert_query = "INSERT INTO pokemon (id, name, height, weight) VALUES (?, ?, ?, ?)"
    try:
        cursor.execute(insert_query, (data['id'], data['name'], data['height'], data['weight']))
        print(f"Successfully inserted: {data['id']}")
    except sqlite3.IntegrityError:
        print(f"Pokémon (ID {data['id']}) already exists in the database.")
    except sqlite3.Error as err:
        print(f"Error inserting data: {err}")

def check_pokemon_exists(cursor, pokeid):
    """Check if Pokémon already exists in the database."""
    query = "SELECT * FROM pokemon WHERE id = ?"
    cursor.execute(query, (pokeid,))
    return cursor.fetchone() is not None

def main():
    start = True

    # Connect to the SQLite database (or create it if it doesn't exist)
    db_connection = sqlite3.connect('pokemon_db.sqlite')
    cursor = db_connection.cursor()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            height INTEGER,
            weight INTEGER
        )
    ''')

    while start:
        user = input("Do you want to draw a Pokémon? Type 'yes' or 'no': \n").strip().lower()
        if user == "yes":
            pokeid = random.randint(1, 898)  # Pokémon IDs go up to 898

            # Fetch data from the API
            new_data = fetch_pokemon_data(pokeid)

            if new_data:
                print(f"Fetched data: {new_data}")  # Debug: Check the fetched data

                # Check if the Pokémon ID exists in the database
                if not check_pokemon_exists(cursor, new_data['id']):
                    # Insert data into SQLite database
                    insert_pokemon_data(cursor, new_data)
                    db_connection.commit()  # Commit the transaction
                else:
                    print(f"Pokémon (ID {new_data['id']}) already exists in the database.")

                # Display the Pokémon data
                display_pokemon_data(new_data)

        else:
            print("Goodbye!")
            start = False

    # Close the cursor and connection
    cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
