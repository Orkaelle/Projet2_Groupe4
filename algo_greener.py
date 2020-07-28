"""
This algorithm identifies the greenest trip.
"""

import datetime
import csv

import requests

import cx_Oracle


token = ["dd7fc13b-20c4-43b7-bee6-1995b3d77a60",
         "2e205281-070a-4755-a703-52fa77a9c943",
         "9e78ab8f-aa47-4261-a036-566f67929ada",
         "9bf360f1-dcb2-40f2-acc3-dee3f60c8f20",
         "91a3c8b6-10a5-454b-8191-4e391dd3ec9f"]
index_token = 4
tokenAPI = token[index_token]


# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur = conn.cursor()

# Extracting prefecture codes
cur.execute('SELECT city_id_pref FROM departementmetro')
result = cur.fetchall()
codes_pref = []
for r in result:
    codes_pref.append(r[0])


# Find start Code :
index_start = codes_pref.index(52121)

# Priorities
priorities = [
    '52121',
    '60057',
    '70550',
    '80021',
    '89024',
    '4112',
    '2408',
    '5061',
    '9122',
    '10387',
    '12202',
    '15014',
    '23096',
    '32013',
    '48095',
    '81004',
    '88160',
    '90010']
priority_trips = []


# start point
start_from = codes_pref[index_start]
start_time = "20200803T060000"

print('\n')
print('Start from ' + str(start_from))
codes_pref.remove(start_from)

greener_route = []
greener_trip = []
temp = []


# first trip
for c in codes_pref:
    depart = str(start_from)
    destination = str(c)
    depart_datetime = start_time

    print('to ' + destination)

    journey_list = []

    lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + depart + \
        "&to=admin%3Afr%3A" + destination + "&datetime=" + depart_datetime + "&max_nb_transfers=2&count=3&"
    data = requests.get(lien).json()

    try:
        message = data['message']
        print(message)
        print('Retry with another token...')
        tokenAPI = token[index_token + 1]
        lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A" + depart + \
            "&to=admin%3Afr%3A" + destination + "&datetime=" + depart_datetime + "&max_nb_transfers=2&count=3&"
        data = requests.get(lien).json()
    except BaseException:
        nada = []

    try:
        journeys = data['journeys']
        print(str(len(journeys)) + " trips found.")

        for j in journeys:
            co2 = j["co2_emission"]["value"]
            temp.append(co2)

        index_greener = temp.index(min(temp))
        temp.clear()

        duration = journeys[index_greener]["durations"]["total"]
        co2 = journeys[index_greener]["co2_emission"]["value"]
        departure_time = journeys[index_greener]["departure_date_time"]
        arrival_time = journeys[index_greener]["arrival_date_time"]
        depart_station = journeys[index_greener]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(
            ':', '%3A')
        max_sections = len(journeys[index_greener]["sections"]) - 1
        arrival_station = journeys[index_greener]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(
            ':', '%3A')

        greener_trip.append([depart,
                             depart_station,
                             destination,
                             arrival_station,
                             departure_time,
                             duration,
                             arrival_time,
                             co2,
                             "C"])

        print("Greener trip saved.")

    except BaseException:
        try:
            error = requests.get(lien).json()['error']['message']
            print(error)
        except BaseException:
            print('ERROR')

temp.clear()
priority_trips.clear()


for f in greener_trip:
    if f[2] in priorities:
        priority_trips.append([greener_trip.index(f), f[7]])
    else:
        temp.append(f[7])

if priority_trips != []:
    temp.clear()
    for p in priority_trips:
        temp.append(p[1])
    index_priority = temp.index(min(temp))
    index_greener = priority_trips[index_priority][0]
else:
    index_greener = temp.index(min(temp))

greener_route.append(greener_trip[index_greener])

print("Starter greener route :")
print(greener_route)


# Next trips

while codes_pref != []:

    depart_pref = greener_route[-1][2]
    depart_station = greener_route[-1][3]
    depart_time = greener_route[-1][6]

    print('\n')
    print('Next step from ' + str(depart_pref))
    codes_pref.remove(int(depart_pref))

    greener_trip.clear()
    temp.clear()

    for c in codes_pref:
        depart = str(depart_station)
        destination = str(c)
        depart_datetime = str(depart_time)

        print('to ' + destination)

        journey_list = []

        lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf//journeys?from=" + depart + "&to=admin%3Afr%3A" + \
            destination + "&max_nb_transfers=2&count=3&datetime=" + depart_datetime + "&datetime_represents=departure&"
        data = requests.get(lien).json()

        try:
            message = data['message']
            print(message)
            print('Retry with another token...')
            tokenAPI = token[index_token + 1]
            lien = "https://" + tokenAPI + ":@api.navitia.io/v1/coverage/sncf//journeys?from=" + depart + "&to=admin%3Afr%3A" + \
                destination + "&max_nb_transfers=2&count=3&datetime=" + depart_datetime + "&datetime_represents=departure&"
            data = requests.get(lien).json()

        except BaseException:
            nada = []

        try:
            journeys = data['journeys']
            print(str(len(journeys)) + " trips found.")

            for j in journeys:
                co2 = j["co2_emission"]["value"]
                temp.append(co2)

            index_greener = temp.index(min(temp))
            temp.clear()

            duration = journeys[index_greener]["durations"]["total"]
            co2 = journeys[index_greener]["co2_emission"]["value"]
            departure_time = journeys[index_greener]["departure_date_time"]
            arrival_time = journeys[index_greener]["arrival_date_time"]
            depart_station = journeys[index_greener]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(
                ':', '%3A')
            max_sections = len(journeys[index_greener]["sections"]) - 1
            arrival_station = journeys[index_greener]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(
                ':', '%3A')

            greener_trip.append([depart_pref,
                                 depart_station,
                                 destination,
                                 arrival_station,
                                 departure_time,
                                 duration,
                                 arrival_time,
                                 co2,
                                 "C"])

            print("greener trip saved.")

        except BaseException:
            try:
                message = requests.get(lien).json()['message']
                print(message)
            except BaseException:
                try:
                    error = requests.get(lien).json()['error']['message']
                    print(error)
                except BaseException:
                    print('ERROR')

    temp.clear()
    priority_trips.clear()

    if greener_trip:
        for f in greener_trip:
            if f[2] in priorities:
                priority_trips.append([greener_trip.index(f), f[7]])
            temp.append(f[7])

        if priority_trips:
            print(priority_trips)
            temp.clear()
            for p in priority_trips:
                temp.append(p[1])
            index_priority = temp.index(min(temp))
            index_greener = priority_trips[index_priority][0]
        else:
            index_greener = temp.index(min(temp))

        greener_route.append(greener_trip[index_greener])

        print("Next greener route :")
        print(greener_route[-1])

        with open('greener.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(greener_route)

    else:
        print('No trip found for this route !')
        print('\n')


print('\n\n')
print('greener route :')
print(greener_route)
