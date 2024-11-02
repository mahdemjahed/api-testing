

# Pokémon Drawer

A fun Python application to randomly draw a Pokémon and save its information in a local JSON file! Each time you draw a Pokémon, its name, height, and weight are stored, allowing you to build a collection over time.

## Features

- **Random Pokémon Drawing**: Draws a random Pokémon from the [PokeAPI](https://pokeapi.co/) and fetches its details.
- **Persistent Storage**: Saves each Pokémon’s details to a JSON file, so your collection grows with each draw.
- **Duplicate Check**: Only adds a Pokémon to the collection if it hasn’t been saved previously.
- **Formatted Display**: Presents Pokémon information in a user-friendly way.

## Getting Started

### Prerequisites

- **Python 3.6+**
- **Requests library**: Install via pip

  ```bash
  pip install requests
  ```

### Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/mahdemjahed/api-testing.git
    ```

2. Navigate to the project directory:
    ```bash
    cd api-testing
    ```

### Usage

1. Run the program:
    ```bash
    python main.py
    ```

2. When prompted, type `yes` to draw a Pokémon or `no` to exit.

### Example Output

```plaintext
Do you want to draw a Pokémon? Type 'yes' or 'no': 
> yes

Pokémon Data:
==============================
Name: Pikachu
ID: 25
Height: 4 decimeters
Weight: 60 hectograms
==============================
```

### JSON Database

Each Pokémon drawn is saved to a `poke.json` file in the following format:

```json
{
    "25": {
        "id": 25,
        "name": "pikachu",
        "height": 4,
        "weight": 60
    }
}
```

## Project Structure

- `main.py`: The main Python script to run the app.
- `poke.json`: JSON file where Pokémon data is saved.
  
## Future Improvements

- **User Interface**: Add a GUI for more interactive use.
- **Filtering**: Allow users to filter Pokémon based on different attributes (height, weight, etc.).
- **Expanded Details**: Save more information like abilities, types, or moves.

## Contributing

Contributions are welcome! Please submit a pull request with any suggested improvements.

