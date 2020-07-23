import cx_Oracle
import requests
import datetime


tokenAPI = "91a3c8b6-10a5-454b-8191-4e391dd3ec9f"

'''
# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()

# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departement;')
codes_pref = cur.fetchall()
print (codes_pref)
'''

# test version
codes_pref = [6088, 10387, 15014, 59350]

# start point
start_from = codes_pref[0]
start_time = "20200801T060000"

print ('\n')
print ('Start from ' + str(start_from))
codes_pref.remove(start_from)

faster_route = []
faster_trip = []
temp = []


# first trip
for c in codes_pref :
    depart = str(start_from)
    destination = str(c)
    depart_datetime = start_time

    print ('to ' + destination)

    journey_list = []

    lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + depart + "&to=admin%3Afr%3A" + destination + "&datetime=" + depart_datetime + "&max_nb_transfers=2&count=3&"
    data = requests.get(lien).json()

    try :
        journeys = requests.get(lien).json()['journeys']
        print (str(len(journeys)) + " trips found.")

        for j in journeys :
            arrival_datetime = j["arrival_date_time"]
            temp.append(datetime.datetime.strptime(arrival_datetime,'%Y%m%dT%H%M%S%f'))

        index_faster = temp.index(min(temp))
        temp.clear()

        duration = journeys[index_faster]["durations"]["total"]
        co2 = journeys[index_faster]["co2_emission"]["value"]
        arrival_time = journeys[index_faster]["arrival_date_time"]
        depart_station = journeys[index_faster]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(':','%3A')
        max_sections = len(journeys[index_faster]["sections"])-1
        arrival_station = journeys[index_faster]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(':','%3A')

        faster_trip.append([depart, depart_station, destination, arrival_station, duration, arrival_time, co2])

        print ("Faster trip saved.")

    except :
        try :
            error = requests.get(lien).json()['error']['message']
            print (error)
        except :
            print ('ERROR')
    
temp.clear()

for f in faster_trip :
    temp.append(f[5])
index_faster = temp.index(min(temp))
faster_route.append(faster_trip[index_faster])

print ("Starter faster route :")
print (faster_route)



# Next trips

while codes_pref != [] :

    depart_pref = faster_route[-1][2]
    depart_station = faster_route[-1][3]
    depart_time = faster_route[-1][5]

    print ('\n')
    print ('Next step from ' + str(depart_pref))
    codes_pref.remove(int(depart_pref))

    faster_trip.clear()
    temp.clear()

    for c in codes_pref :
        depart = str(depart_station)
        destination = str(c)
        depart_datetime = str(depart_time)

        print ('to ' + destination)

        journey_list = []

        lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf//journeys?from=" + depart + "&to=admin%3Afr%3A" + destination + "&max_nb_transfers=2&count=3&datetime=" + depart_datetime + "&datetime_represents=departure&"
        data = requests.get(lien).json()

        try :
            journeys = requests.get(lien).json()['journeys']
            print (str(len(journeys)) + " trips found.")

            for j in journeys :
                arrival_datetime = j["arrival_date_time"]
                temp.append(datetime.datetime.strptime(arrival_datetime,'%Y%m%dT%H%M%S%f'))

            index_faster = temp.index(min(temp))
            temp.clear()

            duration = journeys[index_faster]["durations"]["total"]
            co2 = journeys[index_faster]["co2_emission"]["value"]
            arrival_time = journeys[index_faster]["arrival_date_time"]
            depart_station = journeys[index_faster]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(':','%3A')
            max_sections = len(journeys[index_faster]["sections"])-1
            arrival_station = journeys[index_faster]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(':','%3A')

            faster_trip.append([depart_pref, depart_station, destination, arrival_station, duration, arrival_time, co2])

            print ("Faster trip saved.")

        except :
            try :
                error = requests.get(lien).json()['error']['message']
                print (error)
            except :
                print ('ERROR')
        
    temp.clear()

    for f in faster_trip :
        temp.append(f[5])
    index_faster = temp.index(min(temp))
    faster_route.append(faster_trip[index_faster])

    print ("Next faster route :")
    print (faster_route[-1])

print ('\n\n')
print ('Faster route :')
print (faster_route)






    

