import sqlite3

# Connect to the database
conn = sqlite3.connect('data.db')

# Create a cursor object
cur = conn.cursor()

# Insert a deck named "KanjiToRomajis"
cur.execute('''
INSERT INTO Decks (DeckName, DeckDescription) VALUES ('KanjiToRomajis', 'JLPT N5 Kanji to Romajis')
''')
deck_id = cur.lastrowid

# Insert cards with basic JLPT N5 kanjis and their corresponding romaji pronunciations
kanji_romaji_pairs = [
    ('日', 'hi'), ('月', 'tsuki'), ('火', 'hi'), ('水', 'mizu'), ('木', 'ki'),
    ('金', 'kane'), ('土', 'tsuchi'), ('本', 'hon'), ('人', 'hito'), ('年', 'nen')
]

for kanji, romaji in kanji_romaji_pairs:
    cur.execute('''
    INSERT INTO Cards (CardQuestion, CardAnswer, DeckID) VALUES (?, ?, ?)
    ''', (kanji, romaji, deck_id))

# Ensure LevelTypes are present (if not already inserted by previous script)
level_types = [(0,), (1,), (2,), (3,)]
cur.executemany('INSERT OR IGNORE INTO LevelTypes (LevelType) VALUES (?)', level_types)

# Insert levels with specified names and types
levels = [
    ('Learn 1', 0), ('Learn 2', 0), ('Recap 1-2', 1),
    ('Learn 3', 0), ('Learn 4', 0), ('Recap 3-4', 1),
    ('Big Recap 1-4', 2), ('Boss 1', 3)
]

for level_name, level_type in levels:
    cur.execute('''
    INSERT INTO Levels (LevelName, LevelType, DeckID) VALUES (?, ?, ?)
    ''', (level_name, level_type, deck_id))

# Retrieve all cards and levels for association
cur.execute('SELECT CardID FROM Cards WHERE DeckID = ?', (deck_id,))
cards = cur.fetchall()

cur.execute('SELECT LevelID, LevelName FROM Levels WHERE DeckID = ?', (deck_id,))
levels = {level_name: level_id for level_id, level_name in cur.fetchall()}

# Associate cards with levels through the CardLevel table
# For simplicity, every card is associated with every level; adjust as needed
for card_id, in cards:
    for level_name in levels.keys():
        cur.execute('''
        INSERT INTO CardLevel (CardID, LevelID) VALUES (?, ?)
        ''', (card_id, levels[level_name]))

# Commit the changes
conn.commit()

# Close the connection
conn.close()