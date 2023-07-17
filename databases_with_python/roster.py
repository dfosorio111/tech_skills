import json
import sqlite3 as sql

# connect Python to SQL database
conn = sql.connect('rosterdb.sqlite')

# SQL Python handle
cur = conn.cursor()

# SQL: drop User, Member, Courser tables,
# create tables database structure
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;


CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);
CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);
CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

# input user file of data to process

# *** READ .json files
input_file = input('Enter input file name:')
if len(input_file) < 1:
    fname = 'roster_data.json'

# open file of data, read
str_data = open(fname).read()

# load json data format
# json data is an array of arrays [[],[],[]... ]
json_data = json.loads(str_data)

# iterate through arrays (rows) in the json data array file
for entry in json_data:

    # new entry in database
    name = entry[0]
    title = entry[1]
    role = entry[2]

    print(name, title, role)

    # independant tables entry

    # SQL: INSERT OR IGNORE INTO User,  insert new_user into table User, or ignore if key=name exists
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', (name, ))
    # SQL: INSERT OR IGNORE INTO Course, insert new_course into table Course, or ignore if key=title exists
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', (title, ))

    # SQL: read(get)  user_id, from new_user  key=name, instance for dependent tables
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    # SQL: catch
    user_id = cur.fetchone()[0]

    # SQL: read(get)  course_id, from new_course  key=title
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    # SQL: catch
    course_id = cur.fetchone()[0]


    # SQL: INSERT OR REPALCE(update) INTO Member,  insert new_member into table Member, or update
    # if keys=(user_id, course_id, role) VALUES() exists
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        (user_id, course_id, role))


action = '''
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1;
'''

print
for column in cur.execute(action) :
    print(str(column[0]) )

# commit SQL commands
conn.commit()

# close SQL handle
cur.close()