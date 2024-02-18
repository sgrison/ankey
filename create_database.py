import sqlite3

# Connect to the database (creates the database if it does not exist)
conn = sqlite3.connect('data.db')

# Create a cursor object
cur = conn.cursor()

# Create the Decks table
cur.execute('''
CREATE TABLE IF NOT EXISTS Decks (
    DeckID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    DeckName TEXT NOT NULL,
    DeckDescription TEXT
)
''')

# Create the Cards table
cur.execute('''
CREATE TABLE IF NOT EXISTS Cards (
    CardID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    CardQuestion TEXT NOT NULL,
    CardAnswer TEXT NOT NULL,
    DeckID INTEGER,
    FOREIGN KEY (DeckID) REFERENCES Decks (DeckID)
)
''')

# Create the Levels table
cur.execute('''
CREATE TABLE IF NOT EXISTS Levels (
    LevelID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    LevelName TEXT NOT NULL,
    LevelDescription TEXT,
    DeckID INTEGER,
    LevelType INTEGER,
    LevelCompletion INTEGER DEFAULT 0,
    FOREIGN KEY (DeckID) REFERENCES Decks (DeckID),
    FOREIGN KEY (LevelType) REFERENCES LevelTypes (LevelTypeID)
)
''')

# Create the CardLevel Intermediate Table
cur.execute('''
CREATE TABLE IF NOT EXISTS CardLevel (
    CardLevelID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    CardID INTEGER,
    LevelID INTEGER,
    FOREIGN KEY (CardID) REFERENCES Cards (CardID),
    FOREIGN KEY (LevelID) REFERENCES Levels (LevelID)
)
''')

# Create the LevelTypes Table
cur.execute('''
CREATE TABLE IF NOT EXISTS LevelTypes (
    LevelTypeID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    LevelType INTEGER CHECK(LevelType BETWEEN 0 AND 3)
)
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()