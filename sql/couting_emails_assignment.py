# Week 2: Counting emails in database

# import libraries SQL
import sqlite3 as sql

# connect python to database='database_counting_email.sqlite'
conn = sql.connect('database_counting_email.sqlite')

# SQL: execute commands from python to SQL (handle databases from python)
cur = conn.cursor()

# SQL: DROP TABLE IF EXISTS table,  drop table to initialize
cur.execute('DROP TABLE IF EXISTS Counts')

# SQL: create table=Counts  keys(org TEXT, cont INTEGER)
cur.execute('CREATE TABLE Counts (org TEXT, count INTEGER)')

#  user input filename
fname = input('Enter file name: ')

# if user didn't enter file name
if (len(fname) < 1):
    fname = 'mbox.txt'

# open file
fh = open(fname)
# iterate through lines in file
for line in fh:

    # print(line)

    # if line doesn't start with 'From: '
    if not line.startswith('From: '):
        continue

    # split line starting with 'From: ', by space ""
    pieces = line.split()

    # email is pieces[1]  2nd position
    email = pieces[1]

    # split email string by '@'
    email_split = email.split("@")

    # get domain from email_split
    domain = email_split[1]

    print(domain)

    # SQL: read key=columns (or all*) FROM table, WHERE key=val_cond is matched

    # SQL:  SELECT columns (or all *) FROM table WHERE key=val_cond, ? tuple to fill with

    cur.execute('SELECT * FROM Counts WHERE org = ? ', (domain,))

    # get row
    row = cur.fetchone()

    # if NO entry with org= domain, create INSERT INTO() new organization
    if row is None:
        # INSERT INTO table(key1,key n) VALUES (1,?,X),(val1,valx)
        # start organization count with 1
        cur.execute('INSERT INTO Counts (org, count) VALUES (?, 1) ', (domain,))


    # if there is already an entry with org=domain
    else:

        # UPDATE table SET action key=new_val WHERE key=val_cond
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?', (domain,))

# execute SQL commands
conn.commit()

# SQL: read keys= email,count FROM table=Counts ORDER BY sort key=count  DESC LIMIT 10
# sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'

# for row in cur.execute(sqlstr):
#    print(str(row[0]), row[1])

# close connection
cur.close()