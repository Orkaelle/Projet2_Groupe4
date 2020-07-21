# Imports
import cx_Oracle


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print('Connected : ' + conn.version)
cur=conn.cursor()


# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departement')
result = cur.fetchall()
codes_pref = []

for r in result :
    codes_pref.append(r[0])
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

# Insert dictionary in db table
liste_id = []
liste_i = []
liste_j = []
for r in routes :
    liste_id.append(r[0])
    liste_i.append(r[1])
    liste_j.append(r[2])
liste_import = [liste_id, liste_i, liste_j]

# cur.execute('INSERT INTO route(id_route, depart_city, arrival_city) VALUES(?,?,?)', liste_import)

conn.commit()
conn.close()




