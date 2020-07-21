# Imports
import cx_Oracle
import requests

tokenAPI = "91a3c8b6-10a5-454b-8191-4e391dd3ec9f"

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
id_trip = 1
for c in codes_pref :
    hyp = "H" + str(c)
    datetime = "20200801T060000"
    print (hyp)

    for r in routes :
        if r[1] == c :

            faster = []
            greener = []

            depart = r[1]
            destination = r[2]
            lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + str(depart) + "&to=admin%3Afr%3A" + str(destination) + "&datetime=" + datetime + "&max_nb_transfers=2&count=3&"
            journeys = requests.get (lien).json()['journeys']
            liste_trajets = []

            id = 0
            for j in journeys :
                duration = j["durations"]["total"]
                co2 = j["co2_emission"]["value"]
                arrival_time = j["arrival_date_time"]
                liste_trajets.append([hyp + "->" + str(destination) + "-" + str(id), duration, co2, arrival_time])
                id += 1

            temp_faster = []
            temp_greener = []
            for l in liste_trajets :
                temp_faster.append(l[1])
                temp_greener.append(l[2])
            index_faster = temp_faster.index(min(temp_faster)))
            index_greener = temp_greener.index(min(temp_greener)))

            faster.append(liste_trajets[index_faster])
            greener.append(liste_trajets[index_greener])






            

            






# conn.commit()
# conn.close()




