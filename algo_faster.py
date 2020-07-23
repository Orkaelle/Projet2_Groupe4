import cx_Oracle
import requests
import datetime

token = ["2e205281-070a-4755-a703-52fa77a9c943","9e78ab8f-aa47-4261-a036-566f67929ada","9bf360f1-dcb2-40f2-acc3-dee3f60c8f20","91a3c8b6-10a5-454b-8191-4e391dd3ec9f"]
index_token = 0
tokenAPI = token[index_token]


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()

# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departementmetro')
result = cur.fetchall()
codes_pref = []
for r in result :
    codes_pref.append(r[0])


# Find start Code :
index_start = codes_pref.index(29232) #Quimper

'''
# test version
codes_pref = [6088, 10387, 15014, 59350]
'''

# start point
start_from = codes_pref[index_start]
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
        message = data['message']
        print(message)
        print ('Retry with another token...')
        tokenAPI = token[index_token+1]
        lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + depart + "&to=admin%3Afr%3A" + destination + "&datetime=" + depart_datetime + "&max_nb_transfers=2&count=3&"
        data = requests.get(lien).json()


    except :
        print ("")
    try :
        journeys = data['journeys']
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
            message = data['message']
            print(message)
            print ('Retry with another token...')
            tokenAPI = token[index_token+1]
            lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf//journeys?from=" + depart + "&to=admin%3Afr%3A" + destination + "&max_nb_transfers=2&count=3&datetime=" + depart_datetime + "&datetime_represents=departure&"
            data = requests.get(lien).json()


        except :
            print ("")

        try :
            journeys = data['journeys']
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
                message = requests.get(lien).json()['message']
                print(message)
            except :
                try :
                    error = requests.get(lien).json()['error']['message']
                    print (error)
                except :
                    print ('ERROR')
        
    temp.clear()

    if faster_trip != [] :
        for f in faster_trip :
            temp.append(f[5])
        index_faster = temp.index(min(temp))
        faster_route.append(faster_trip[index_faster])

        print ("Next faster route :")
        print (faster_route[-1])
    else :
        print ('No trip found for this route !')
        print ('\n')



print ('\n\n')
print ('Faster route :')
print (faster_route)
