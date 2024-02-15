import sqlite3

def create_tables(cursor):
    """Create the Decks and Cards tables if they don't exist."""
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

def insert_decks(cursor):
    """Inserts the 'Capitales' and 'KanjiToRomaji' decks into the Decks table."""
    decks_to_add = [('Capitales', 'A deck of capital cities.'),
                    ('KanjiToRomaji', 'A deck for learning Kanji characters and their Romaji transliterations.')]
    cursor.executemany('INSERT INTO Decks (DeckName, DeckDescription) VALUES (?, ?)', decks_to_add)

def insert_cards(cursor):
    """Inserts cards into the Cards table for the newly created decks."""
    # Fetch the DeckIDs for "Capitales" and "KanjiToRomaji"
    cursor.execute("SELECT DeckID FROM Decks WHERE DeckName = 'Capitales'")
    capitales_deck_id = cursor.fetchone()[0]
    cursor.execute("SELECT DeckID FROM Decks WHERE DeckName = 'KanjiToRomaji'")
    kanji_to_romaji_deck_id = cursor.fetchone()[0]

    # Cards for the "Capitales" deck
    capitales_cards = [
        (capitales_deck_id, 'France', 'Paris'),
        (capitales_deck_id, 'Germany', 'Berlin'),
        (capitales_deck_id, 'Italy', 'Rome'),
        # Add more as needed
    ]

    # Cards for the "KanjiToRomaji" deck
    kanji_to_romaji_cards = [
        (kanji_to_romaji_deck_id, '日', 'Ni'),
        (kanji_to_romaji_deck_id, '本', 'Hon'),
        (kanji_to_romaji_deck_id, '人', 'Jin'),
        # Add more as needed
    ]

    # Insert the cards into the Cards table
    cursor.executemany('INSERT INTO Cards (DeckID, CardVisible, CardHidden) VALUES (?, ?, ?)', capitales_cards)
    cursor.executemany('INSERT INTO Cards (DeckID, CardVisible, CardHidden) VALUES (?, ?, ?)', kanji_to_romaji_cards)

def main():
    # Connect to your database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Create tables
    create_tables(cursor)

    # Insert decks
    insert_decks(cursor)

    # Commit the changes to ensure decks are inserted before adding cards
    conn.commit()

    # Insert cards
    insert_cards(cursor)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print('Decks and cards added successfully.')

if __name__ == "__main__":
    main()