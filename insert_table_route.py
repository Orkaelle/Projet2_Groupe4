# Imports
import cx_Oracle


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()


# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departement;')
codes_pref = cur.fetchall()
print (codes_pref)

# version test
#codes_pref = [69877,65455,87966,98576,98990,43545,76344]


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

conn.commit()
conn.close()




