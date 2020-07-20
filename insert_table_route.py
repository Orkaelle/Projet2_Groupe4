# Imports
import cx_Oracle


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()


# Extracting Stations Codes
cur.execute('SELECT city_id_pref FROM departement;')
codes_pref = cur.fetchall()


'''
# VERSION TEST
import sqlite3
import os
import sys

dbName = 'test.db'
base_dir = os.path.dirname(sys.argv[0])
dir_path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(dir_path, dbName)

if os.path.exists(path):
    os.remove(path)

db = sqlite3.connect(path)
cur = db.cursor()
cur.execute('CREATE TABLE route (id_route INTEGER AUTO INCREMENT PRIMARY KEY, departure_city TEXT, arrival_city TEXT);')
codes_pref = [69877,65455,87966,98576,98990,43545,76344]
'''

# Creation dictionary for stations codes
routes = []
id = 1
for i in codes_pref :
    for j in codes_pref :
        if j != i :
            routes.append([id,i,j])
            id += 1
print (routes)



# Insert dictionary in db table
for r in routes :
    cur.execute('INSERT INTO route(id_route, departure_city, arrival_city) VALUES(?,?,?)', r)

db.commit()
db.close()




