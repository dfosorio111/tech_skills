import xml.etree.ElementTree as ET
import sqlite3

# connect Python to database file
conn = sqlite3.connect('example_tracks.sql')

# SQL handle
cur = conn.cursor()

# Make some fresh tables using executescript()
# cur.executescript('''...''') execute large lines of commands in database

# SQL: CREATE TABLE ('Artist', 'Genre', 'Album', 'Track')
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre; 
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;


CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
);
CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
        AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
);
''')

# input user file name
fname = input('Enter file name: ')

# if no filename as input
if ( len(fname) < 1 ) :
    #default filename
    fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>

# look for
def lookup(d, key):
    found = False

    # iterate through external dict
    for child in d:
        # if it found
        if found :
            # returns the key.text
            return child.text

        # if external dic.tag=='key' AND child.text == Jey
        if child.tag == 'key' and child.text == key :
            # founds
            found = True
    return None

# parse filename string
stuff = ET.parse(fname)

# findall() internal keys from dict
all = stuff.findall('dict/dict/dict')
# print count of tracks
print('Dict count:', len(all))

# iterate through all list of keys (tracks)
for entry in all:

    # if track is not in Track ID
    if ( lookup(entry, 'Track ID') is None ) :
        continue

    # add new track
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')

    #added this
    genre = lookup(entry,'Genre')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')

    if name is None or artist is None or album is None or genre is None:
        continue

    # print track key values
    print(name, artist, album, genre, count, rating, length)

    # SQL: insert into table OR ignore, if key,val already in table

    # '''INSERT OR IGNORE INTO table(key) VALUES (?)''',(val_tuple,) ) ,  ?=tuple to complete
    cur.execute('''INSERT OR IGNORE INTO Artist (name) 
        VALUES ( ? )''', ( artist, ) )

    # SQL: read(get) new_artist id
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    # SQL: cur.fetchone()[0] get first element from SQL console
    artist_id = cur.fetchone()[0]

    # SQL: insert into table OR ignore, if key,val already in table

    # '''INSERT OR IGNORE INTO table(key) VALUES (?)''',(val_tuple,) ) ,  ?=tuple to complete
    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    # get/grab genre id just added
    genre_id = cur.fetchone()[0]


    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) 
        VALUES ( ?, ? )''', ( album, artist_id ) )


    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    # SQL: insert into table OR replace(UPDATE),  if key,val already in table

    # '''INSERT OR REPACE INTO table(key) VALUES (?)''',(val_tuple,) ) ,  ?=tuple to complete
    cur.execute('''INSERT OR REPLACE INTO Track
        (title, album_id, genre_id, len, rating, count) 
        VALUES ( ?, ?, ?, ?, ?, ? )''',
        ( name, album_id, genre_id, length, rating, count ) )


    # conn.commit(),  excecute commands
    conn.commit()
#Added this
sqlstr = 'SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Genre JOIN Album JOIN Artist ON Track.genre_id = Genre.ID and Track.album_id = Album.id AND Album.artist_id = Artist.id ORDER BY Artist.name LIMIT 3'

print
for row in cur.execute(sqlstr) :
    print(str(row[0]),str(row[1]),str(row[2]),str(row[3]))

cur.close()