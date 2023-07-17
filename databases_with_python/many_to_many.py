import sqlite3 as sql
import xml.etree.ElementTree as ET

# connect Python to SQL database file
conn = sql.connect('many2many_db.sqlite')

# SQL handle in Python
cur = conn.cursor()

# SQL: DROP TABLE IF EXIST table,  drop pre existing tables
# SQL: CREATE TABLE table(key1,key2,keyn)  create DB structures
cur.executescript('''

DROP TABLE IF EXISTS table_1;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course; 
DROP TABLE IF EXISTS Member;


CREATE TABLE User(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
name TEXT,
email TEXT
);

CREATE TABLE Course(
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
title TEXT 
);

CREATE TABLE Member(
user_id INTEGER,
course_id INTEGER,
role INTEGER, 

PRIMARY KEY(user_id, course_id)
);


''')

# SQL: INSERT INTO table (key1,key2,keyn) VALUES(val1,valn);
# insert some data into databases

cur.executescript('''

/*INSERT INTO table User  */
INSERT INTO User(name, email) VALUES ('Jane', 'jane@tsugi.org');
INSERT INTO User(name, email) VALUES ('Ed', 'ed@tsugi.org');
INSERT INTO User(name, email) VALUES ('Sue', 'sue@tsugi.org');

/*INSERT INTO table Course  */
INSERT INTO Course(title) VALUES ('Python');
INSERT INTO Course(title) VALUES ('SQL');
INSERT INTO Course(title) VALUES ('PHP');


/* INSERT INTO Member(pk_table1,pk_table2,key) VALUES(val1,val2,valn)
insert into intermediate table relationship between primary keys of other tables */

/*INSERT INTO table Member, role  0=student, 1=teacher  */

INSERT INTO Member(user_id, course_id, role) VALUES(1, 1, 1);
INSERT INTO Member(user_id, course_id, role) VALUES(2, 1, 0);
INSERT INTO Member(user_id, course_id, role) VALUES(3, 1, 0);

INSERT INTO Member(user_id, course_id, role) VALUES(1, 2, 0);
INSERT INTO Member(user_id, course_id, role) VALUES(2, 2, 1);

INSERT INTO Member(user_id, course_id, role) VALUES(2, 3, 1);
INSERT INTO Member(user_id, course_id, role) VALUES(3, 3, 0);


''')


# SQL: read(get) merge()  User,Member, Course tables,
# ORDER BY(group by) Course.title, Member. role DESC, User.name


merge_tables = '''
SELECT User.name, Member.role, Course.title
FROM User JOIN Member JOIN Course
ON Member.user_id=User.id AND Member.course_id=Course.id
ORDER BY Course.title, Member.role  DESC, User.name
'''

print
for column in cur.execute(merge_tables) :
    print(str(column[0]),str(column[1]),str(column[2]) )



# commit SQL commands
conn.commit()

# close SQL handle
cur.close()