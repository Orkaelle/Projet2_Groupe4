# Imports
import cx_Oracle
import requests
import json
import datetime

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
routes = [[1, 6088, 10387], [2, 10387, 15014], [3, 6088, 15014], [4, 10387, 6088], [5, 15014, 10387], [6, 15014, 6088]]
codes_pref = [6088, 10387, 15014]


# Creation departure hypothesis
id_trip = 1

c = codes_pref[0]
depart_datetime = "20200801T060000"
faster_trip = []
greener_trip = []
faster = []
greener = []

print ("\n")
print ("Test trips from " + str(c))

for r in routes :
    if r[1] == c :
        print ("to " + str(r[2]))
        liste_trajets = []

        depart = r[1]
        destination = r[2]

        lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + str(depart) + "&to=admin%3Afr%3A" + str(destination) + "&datetime=" + depart_datetime + "&max_nb_transfers=2&count=3&"
        data = requests.get(lien).json()

        try :
            journeys = requests.get(lien).json()['journeys']
            print ("OK : " + str(len(journeys)) + " trips found.")   

            temp_faster_trip = []
            temp_greener_trip = []
            for j in journeys :

                duration = j["durations"]["total"]
                co2 = j["co2_emission"]["value"]
                arrival_time = j["arrival_date_time"]
                depart_station = j["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(':','%3A')
                max_sections = len(j["sections"])-1
                arrival_station = j["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(':','%3A')
                liste_trajets.append([depart, destination, duration, co2, arrival_time, depart_station, arrival_station])
                temp_faster_trip.append(datetime.datetime.strptime(arrival_time,'%Y%m%dT%H%M%S%f'))
                temp_greener_trip.append(co2)


            index_faster_trip = temp_faster_trip.index(min(temp_faster_trip))
            index_greener_trip = temp_greener_trip.index(min(temp_greener_trip))
            faster_trip.append(liste_trajets[index_faster_trip])
            greener_trip.append(liste_trajets[index_greener_trip])


        except :
            try :
                error = requests.get(lien).json()['error']['message']
                print (error)
            except :
                print ('An error has occured')   


temp_faster = []
temp_greener = []

if (faster_trip) :
    for f in faster_trip :
        temp_faster.append(f[4])
    index_faster = temp_faster.index(min(temp_faster))
    faster_route = faster_trip[index_faster]

if (greener_trip) :
    for g in greener_trip :
        temp_greener.append(f[3])
    index_greener = temp_greener.index(min(temp_greener))
    greener_route = greener_trip[index_greener]

print ("Faster route :")
print (faster_route)
print ("Greener route :")
print (greener_route)

depart_datetime_faster = faster_route[4]
depart_datetime_greener = greener_route[4]
depart_station_faster = faster_route[6]
depart_station_greener = greener_route[6]
depart_pref_faster = faster_route[1]
depart_pref_greener = greener_route[1]

faster.append(faster_route)
greener.append(greener_route)

faster_route.clear()
greener_route.clear()

exclude = []
exclude.append(c)

print ('\n')
print ('Next faster step :')
print ('from ' + str(depart_pref_faster))

faster_trip.clear()
greener_trip.clear()


for r in routes :

    if r[1] == depart_pref_faster :
        if not r[2] in exclude :
            print ("to " + str(r[2]))
            liste_trajets.clear()

            depart = depart_station_faster
            destination = r[2]
            datetime = depart_datetime_faster

            lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf//journeys?from=" + str(depart) + "&to=admin%3Afr%3A" + str(destination) + "&max_nb_transfers=2&count=3&datetime=" + datetime + "&datetime_represents=departure&"
            print (lien)
            try :
                journeys = requests.get(lien).json()['journeys']
                print ("OK : " + str(len(journeys)) + " trips found.")   
                
                temp_faster_trip.clear()
                temp_greener_trip.clear()
                for j in journeys :
                    duration = j["durations"]["total"]
                    co2 = j["co2_emission"]["value"]
                    arrival_time = j["arrival_date_time"]
                    depart_station = j["sections"][0]["from"]['stop_area']['id'].replace(':','%3A')
                    max_sections = len(j["sections"])-1
                    arrival_station = j["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(':','%3A')
                    liste_trajets.append([depart, destination, duration, co2, arrival_time, depart_station, arrival_station])
                    temp_faster_trip.append(datetime.datetime.strptime(arrival_time,'%Y%m%dT%H%M%S%f'))
                    temp_greener_trip.append(co2)


                index_faster_trip = temp_faster_trip.index(min(temp_faster_trip))
                index_greener_trip = temp_greener_trip.index(min(temp_greener_trip))
                faster_trip.append(liste_trajets[index_faster_trip])
                greener_trip.append(liste_trajets[index_greener_trip])


            except :
                try :
                    error = requests.get(lien).json()['error']['message']
                    print (error)
                except :
                    print ('An error has occured')   

temp_faster.clear()
temp_greener.clear()

if (faster_trip) :
    for f in faster_trip :
        temp_faster.append(f[2])
    index_faster = temp_faster.index(min(temp_faster))
    faster_route = faster_trip[index_faster]

if (greener_trip) :
    for g in greener_trip :
        temp_greener.append(f[3])
    index_greener = temp_greener.index(min(temp_greener))
    greener_route = greener_trip[index_greener]

print ("Faster route :")
print (faster_route)
print ("Greener route :")
print (greener_route)

depart_datetime_faster = faster_route[4]
depart_datetime_greener = greener_route[4]
depart_station_faster = faster_route[6]
depart_station_greener = greener_route[6]
depart_pref_faster = faster_route[1]
depart_pref_greener = greener_route[1]




            

            

# conn.commit()
# conn.close()