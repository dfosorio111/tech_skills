import xml.etree.ElementTree as ET
import sqlite3

# connect Python to database file
conn = sqlite3.connect('music_tracks.sqlite')

# SQL handle
cur = conn.cursor()


# cur.executescript('''...''') execute large lines of commands in database

# SQL: CREATE TABLE ('Artist', 'Genre', 'Album', 'Track')
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Genre; 
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Track;
DROP TABLE IF EXISTS table_1;


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

# input user file of data to process

input_file = input('Enter input file name:')

# if no filename as input
if ( len(input_file) < 1 ) :
    #default filename#
    input_file = 'Library.xml'

# look for  function
def lookup(dict, key):
    found = False

    # iterate through external dict
    for items in dict:
        # if found==True
        if found :
            # returns the key.text
            return items.text

        # if external dic.tag=='key' AND child.text == Jey
        if items.tag == 'key' and items.text == key :
            # founds
            found = True
    return None

# parse filename string,  parse all input data file to process
file_string = ET.parse(input_file)

# findall() internal keys from dict
tracks_datafile = file_string.findall('dict/dict/dict')
# print count of tracks
print('Dict count:', len(tracks_datafile),"\b")
print("\b")
print("The number of tracks found on input data file is: "+ str(len(tracks_datafile)))

# iterate through tracks in datafile
# insert track into database

for track in tracks_datafile:

    print(track)
    # if track is not in Track ID
    if (lookup(track, 'Track ID')is None):
        continue

    # create new track

    name = lookup(track,'Name')
    artist = lookup(track,'Artist')
    album = lookup(track,'Album')

    genre = lookup(track,'Genre')
    count = lookup(track,'Play Count')
    rating = lookup(track,'Rating')
    length = lookup(track,'Total Time')

    # if any attribute is None, continue to next iteration (track)
    if name is None or artist is None or album is None or genre is None:
        continue

    # print key values of new entry (track)
    print(name,artist,album,genre,count,rating,length)

    # SQL: insert into table OR ignore, if key,val already in table
    # insert artist entry into Artist table, ignore if artist already exists
    cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES (?)''',(artist,)  )


    # SQL: insert into table OR ignore, if key,val already in table
    # insert genre  into Genre table, ignore if genre name already exists
    cur.execute('''INSERT OR IGNORE INTO Genre (name) 
        VALUES ( ? )''', ( genre, ) )

    # get primary keys PK, key values for tables that depend on to create new entry

    # SQL: read(get) new_artist(or old) primary key PK id
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist,))
    # SQL: cur.fetchone()[0] get first element from SQL console
    artist_id = cur.fetchone()[0]

    # SQL: read(get) new_genre(or old) primary key PK id
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    # get/grab genre id just added
    genre_id = cur.fetchone()[0]

    # SQL: insert into table OR ignore, if key,val already in table
    # insert album entry into Album table, ignore if name already exists
    cur.execute('''INSERT OR IGNORE INTO Album (title,artist_id) VALUES (?,?)''', (album, artist_id))


    # SQL: read(get) new_album(or old) primary key PK id
    cur.execute('''SELECT id FROM Album WHERE title = ? ''', (album,) )
    album_id = cur.fetchone()[0]


    # SQL: insert into table or replace(update), if keys,vals already in table
    cur.execute('''INSERT OR REPLACE INTO Track(title, album_id, genre_id, len, rating, count)
    VALUES(?, ?, ? ,? ,?, ?)''', (name, album_id, genre_id, length, rating,count)  )




# conn.commit() , execute SQL commands to database
conn.commit()

# close SQL handle
cur.close()






