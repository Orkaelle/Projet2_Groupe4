# Imports
import cx_Oracle

'''
# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()


# Extracting Routes
cur.execute('SELECT * FROM route;')
routes = cur.fetchall()
print (routes)

# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departement;')
codes_pref = cur.fetchall()
print (codes_pref)
'''

# version test
routes = [[1, 6088, 10387], [2, 10387, 15014], [3, 6088, 15014], [4, 10387, 15014], [5, 15014, 10387], [6, 15014, 6088]]
codes_pref = [6088, 10387, 15014]


# Creation departure hypothesis
trips = []
id_trip = 1
for i in codes_pref :
    hyp = "H" + str(i)
    print (hyp)
    for j in routes :
        if j[1] = i :
            






# conn.commit()
# conn.close()




