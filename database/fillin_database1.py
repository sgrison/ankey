import sqlite3

# Connect to the database
conn = sqlite3.connect('data.db')

# Create a cursor object
cur = conn.cursor()

# Insert a deck named "Capitales"
cur.execute('''
INSERT INTO Decks (DeckName, DeckDescription) VALUES ('Capitales', 'European Capitals')
''')
deck_id = cur.lastrowid

# Insert cards with European capitals and their corresponding countries
capitals = [
    ('Berlin', 'Germany'),
    ('Paris', 'France'),
    ('Rome', 'Italy'),
    ('Madrid', 'Spain'),
    ('Lisbon', 'Portugal'),
    ('Athens', 'Greece'),
    ('Vienna', 'Austria'),
    ('Brussels', 'Belgium'),
    ('Warsaw', 'Poland'),
    ('Budapest', 'Hungary')
]

for capital, country in capitals:
    cur.execute('''
    INSERT INTO Cards (CardQuestion, CardAnswer, DeckID) VALUES (?, ?, ?)
    ''', (capital, country, deck_id))

# Insert LevelTypes if not already present
level_types = [(0,), (1,), (2,), (3,)]
cur.executemany('INSERT INTO LevelTypes (LevelType) VALUES (?)', level_types)

# Levels with specified names and types
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
# This is a simplified example. You'll need to adjust the logic based on the level and cards you want to associate.
for card_id, in cards:
    for level_name in levels.keys():
        cur.execute('''
        INSERT INTO CardLevel (CardID, LevelID) VALUES (?, ?)
        ''', (card_id, levels[level_name]))

# Commit the changes
conn.commit()

# Close the connection
conn.close()