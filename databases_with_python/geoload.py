import urllib.request, urllib.parse, urllib.error
import http
import sqlite3
import json
import time
import ssl
import sys


# get api_key
api_key = False
# If you have a Google Places API key, enter it here
# api_key = 'AIzaSy___IDByT70'

# initialize api_key
if api_key is False:
    api_key = 42
    serviceurl = "http://py4e-data.dr-chuck.net/json?"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

# Additional detail for urllib
# http.client.HTTPConnection.debuglevel = 1

# connect Python to database file
conn = sqlite3.connect('geodata.sqlite')

# SQL: Python handle
cur = conn.cursor()

# SQL: CREATE TABLE Locations keys(address TEXT, geodata TEXT)
cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


# open where.data file data
fh = open("where.data")
count = 0

# iterate through where.data file to get address of University
for line in fh:

    # if count of universities uploaded is more than 200, then break
    if count > 200 :
        print('Retrieved 200 locations, restart to retrieve more')
        break

    # line.strip() get address from file
    address = line.strip()
    print('')

    # read(get) key=geodata, table Locations, condition WHERE address=
    cur.execute("SELECT geodata FROM Locations WHERE address= ?",
        (memoryview(address.encode()), ))


    try:
        # catch geodata from address of line
        data = cur.fetchone()[0]
        print("Found in database, then don't add location to google maps, continue to next iteration",address)
        continue
    except:
        pass



    # create  dictionary  address-api_key
    parms = dict()
    parms["address"] = address
    if api_key is not False:
        parms['key'] = api_key

    url = serviceurl + urllib.parse.urlencode(parms)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))

    # add a count
    count = count + 1

    try:
        # JSON: load new data in array format
        js = json.loads(data)
    except:
        print(data)  # We print in case unicode causes an error
        continue


    # JSON load NOT OK
    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') :
        print('==== Failure To Retrieve ====')
        print(data)
        break

    # SQL: INSERT INTO table=Locations (key1,key2) VALUES(?, ?)
    cur.execute('''INSERT INTO Locations (address, geodata)
            VALUES ( ?, ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )

    # commit SQL commands
    conn.commit()


    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print("Run geodump.py to read the data from the database so you can vizualize it on a map.")
