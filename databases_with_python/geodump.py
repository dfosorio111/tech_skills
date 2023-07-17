import sqlite3
import json
import codecs

# connect Python to SQL database
conn = sqlite3.connect('geodata.sqlite')

# SQL Python handle
cur = conn.cursor()

# read(get) all from table=Locatins
cur.execute('SELECT * FROM Locations')

# open where.js  javascript file
fhand = codecs.open('where.js', 'w', "utf-8")


# write data
fhand.write("myData = [\n")


# count of entries
count = 0

# iterate through all table rows
for row in cur :

    # decode data from SQL file table
    data = str(row[1].decode())

    # try to load the row data to JSON file
    try:
        js = json.loads(str(data))
    except:
        continue


    # if JSON file statues is NOT=OK, continue to next iteration (row)
    if not('status' in js and js['status'] == 'OK') :
        continue

    # get coordinates of address entry from JSON file
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lng = js["results"][0]["geometry"]["location"]["lng"]

   # if coordinates = [0,0], continue to next iteration
    if lat == 0 or lng == 0 :
        continue

    # add new location address
    where = js['results'][0]['formatted_address']
    # format address
    where = where.replace("'", "")
    try :
        print(where, lat, lng)

        # add 1 to locations count
        count = count + 1
        if count > 1 :
            # write a space
            fhand.write(",\n")

        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")

# close Python handle
cur.close()
fhand.close()

print(count, "records written to where.js")
print("Open where.html to view the data in a browser")

