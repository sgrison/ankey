import sqlite3
import random

def setup_database(cursor):
    """Create tables for the flashcards database."""
    cursor.execute('''CREATE TABLE IF NOT EXISTS Decks (
                      DeckID INTEGER PRIMARY KEY AUTOINCREMENT,
                      DeckName TEXT NOT NULL,
                      DeckDescription TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cards (
                      CardID INTEGER PRIMARY KEY AUTOINCREMENT,
                      DeckID INTEGER,
                      CardContent TEXT NOT NULL,
                      CardAnswer TEXT,
                      FOREIGN KEY (DeckID) REFERENCES Decks(DeckID))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Levels (
                      LevelID INTEGER PRIMARY KEY AUTOINCREMENT,
                      DeckID INTEGER,
                      LevelName TEXT NOT NULL,
                      FOREIGN KEY (DeckID) REFERENCES Decks(DeckID))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS CardLevel (
                      CardLevelID INTEGER PRIMARY KEY AUTOINCREMENT,
                      CardID INTEGER,
                      LevelID INTEGER,
                      FOREIGN KEY (CardID) REFERENCES Cards(CardID),
                      FOREIGN KEY (LevelID) REFERENCES Levels(LevelID))''')

def insert_initial_data(cursor):
    """Insert decks and their specific cards. Then, create levels for each deck."""
    decks_to_add = [('Capitales', 'A deck of capital cities.'),
                    ('KanjiToRomaji', 'A deck for learning Kanji characters and their Romaji transliterations.')]

    # Insert Decks and Cards
    for deck_name, description in decks_to_add:
        cursor.execute('INSERT INTO Decks (DeckName, DeckDescription) VALUES (?, ?)', (deck_name, description))
        deck_id = cursor.lastrowid  # Get the ID of the inserted deck

        if deck_name == 'Capitales':
            cards = [('France', 'Paris'), ('Germany', 'Berlin'), ('Italy', 'Rome')]
        elif deck_name == 'KanjiToRomaji':
            cards = [('日', 'Ni'), ('本', 'Hon'), ('人', 'Jin')]

        for content, answer in cards:
            cursor.execute('INSERT INTO Cards (DeckID, CardVisible, CardHidden) VALUES (?, ?, ?)', (deck_id, content, answer))
        
        # Create 10 Levels for each Deck
        for i in range(1, 11):
            cursor.execute('INSERT INTO Levels (DeckID, LevelName) VALUES (?, ?)', (deck_id, f'Level {i}'))

def assign_random_cards_to_levels(cursor):
    """For each deck, assign 3 random cards to each of its levels."""
    cursor.execute("SELECT DeckID, LevelID FROM Levels")
    level_info = cursor.fetchall()

    for deck_id, level_id in level_info:
        cursor.execute("SELECT CardID FROM Cards WHERE DeckID = ?", (deck_id,))
        cards = [card[0] for card in cursor.fetchall()]
        selected_cards = random.sample(cards, min(len(cards), 3))

        for card_id in selected_cards:
            cursor.execute('INSERT INTO CardLevel (CardID, LevelID) VALUES (?, ?)', (card_id, level_id))

def main():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # setup_database(cursor)
    insert_initial_data(cursor)
    assign_random_cards_to_levels(cursor)

    conn.commit()
    conn.close()
    print("Database setup with decks, cards, levels, and card assignments complete.")

if __name__ == "__main__":
    main()