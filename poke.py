import requests
import sqlite3
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

def display_pokemon_data(data):
    """Display Pokémon data in a nicely formatted way."""
    print("\nPokémon Data:")
    print("=" * 30)
    print(f"Name: {data['name'].capitalize()}")
    print(f"ID: {data['id']}")
    print(f"Height: {data['height']} decimeters")
    print(f"Weight: {data['weight']} hectograms")
    print("=" * 30)

def create_table(cursor):
    """Create the pokemon table if it doesn't exist."""
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        height INTEGER NOT NULL,
        weight INTEGER NOT NULL
    )
    """)

def insert_pokemon_data(cursor, data):
    """Insert Pokémon data into the SQLite database."""
    try:
        cursor.execute("INSERT INTO pokemon (id, name, height, weight) VALUES (?, ?, ?, ?)",
                       (data['id'], data['name'], data['height'], data['weight']))
        print(f"Successfully inserted: {data['id']}")
    except sqlite3.IntegrityError:
        print(f"Pokémon (ID {data['id']}) already exists in the database.")

def check_pokemon_exists(cursor, pokeid):
    """Check if Pokémon already exists in the SQLite database."""
    cursor.execute("SELECT 1 FROM pokemon WHERE id = ?", (pokeid,))
    return cursor.fetchone() is not None

def main():
    start = True

    # Define the path for the SQLite database file
    db_path = os.path.join(os.path.dirname(__file__), 'pokemon_db.sqlite')

    # Use context manager for SQLite connection
    with sqlite3.connect(db_path) as db_connection:
        cursor = db_connection.cursor()
        
        # Ensure the table exists
        create_table(cursor)

        while start:
            user = input("Do you want to draw a Pokémon? Type 'yes' or 'no': \n").strip().lower()
            if user == "yes":
                pokeid = random.randint(1, 898)  # Random Pokémon ID from 1 to 898
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

                    display_pokemon_data(new_data)

            else:
                print("Goodbye!")
                start = False

        cursor.close()  # Close cursor

if __name__ == "__main__":
    main()
