"""
This algorithm identifies the fastest trip.
"""

import datetime

import csv
import requests

import cx_Oracle


token = [
    "32309a06-a2c3-4724-9f37-f4d94586b6c7",
    "660ae566-43e0-4eb4-9950-aaed5e567866",
    "078f97ac-1d15-411d-963b-c6e46689e561",
    "9d8450f6-354d-4c82-ba48-771ebb775d7d",
    "35c22f68-836c-4170-80c2-ad26ffe8527f",
    "72078fc4-5d1e-40f0-a5b0-6d29d8bb4af1"]
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
index_start = codes_pref.index(5061)  # Gap

# Priorities
priorities = ['2408', '5061', '26198', '23096', '60057', '4112']
priority_trips = []

# start point
start_from = codes_pref[index_start]
start_time = "20200803T060000"

print('\n')
print('Start from ' + str(start_from))
codes_pref.remove(start_from)

faster_route = []
faster_trip = []
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
        pass

    try:
        journeys = data['journeys']
        print(str(len(journeys)) + " trips found.")

        for j in journeys:
            arrival_datetime = j["arrival_date_time"]
            temp.append(
                datetime.datetime.strptime(
                    arrival_datetime,
                    '%Y%m%dT%H%M%S%f'))

        index_faster = temp.index(min(temp))
        temp.clear()

        duration = journeys[index_faster]["durations"]["total"]
        co2 = journeys[index_faster]["co2_emission"]["value"]
        departure_time = journeys[index_faster]["departure_date_time"]
        arrival_time = journeys[index_faster]["arrival_date_time"]
        depart_station = journeys[index_faster]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(
            ':', '%3A')
        max_sections = len(journeys[index_faster]["sections"]) - 1
        arrival_station = journeys[index_faster]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(
            ':', '%3A')

        faster_trip.append([depart,
                            depart_station,
                            destination,
                            arrival_station,
                            departure_time,
                            duration,
                            arrival_time,
                            co2,
                            "F"])
        print("Faster trip saved.")

    except BaseException:
        try:
            error = requests.get(lien).json()['error']['message']
            print(error)
        except BaseException:
            print('ERROR')

temp.clear()
priority_trips.clear()


for f in faster_trip:
    if f[2] in priorities:
        priority_trips.append([faster_trip.index(f), f[6]])
    else:
        temp.append(f[6])

if priority_trips != []:
    temp.clear()
    for p in priority_trips:
        temp.append(p[1])
    index_priority = temp.index(min(temp))
    index_faster = priority_trips[index_priority][0]
else:
    index_faster = temp.index(min(temp))

faster_route.append(faster_trip[index_faster])

print("Starter faster route :")
print(faster_route)


# Next trips
while codes_pref != []:

    depart_pref = faster_route[-1][2]
    depart_station = faster_route[-1][3]
    depart_time = faster_route[-1][6]

    print('\n')
    print('Next step from ' + str(depart_pref))
    codes_pref.remove(int(depart_pref))

    faster_trip.clear()
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
            pass

        try:
            journeys = data['journeys']
            print(str(len(journeys)) + " trips found.")

            for j in journeys:
                arrival_datetime = j["arrival_date_time"]
                temp.append(
                    datetime.datetime.strptime(
                        arrival_datetime,
                        '%Y%m%dT%H%M%S%f'))

            index_faster = temp.index(min(temp))
            temp.clear()

            duration = journeys[index_faster]["durations"]["total"]
            co2 = journeys[index_faster]["co2_emission"]["value"]
            departure_time = journeys[index_faster]["departure_date_time"]
            arrival_time = journeys[index_faster]["arrival_date_time"]
            depart_station = journeys[index_faster]["sections"][0]["to"]['stop_point']['stop_area']['id'].replace(
                ':', '%3A')
            max_sections = len(journeys[index_faster]["sections"]) - 1
            arrival_station = journeys[index_faster]["sections"][max_sections]['from']['stop_point']['stop_area']['id'].replace(
                ':', '%3A')

            faster_trip.append([depart_pref,
                                depart_station,
                                destination,
                                arrival_station,
                                departure_time,
                                duration,
                                arrival_time,
                                co2,
                                "F"])

            print("Faster trip saved.")

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

    if faster_trip:
        for f in faster_trip:
            if f[2] in priorities:
                priority_trips.append([faster_trip.index(f), f[6]])
            temp.append(f[6])

        if priority_trips:
            print(priority_trips)
            temp.clear()
            for p in priority_trips:
                temp.append(p[1])
            index_priority = temp.index(min(temp))
            index_faster = priority_trips[index_priority][0]
        else:
            index_faster = temp.index(min(temp))

        faster_route.append(faster_trip[index_faster])

        print("Next faster route :")
        print(faster_route[-1])

        with open('faster.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(faster_route)

    else:
        print('No trip found for this route !')
        print('\n')


print('\n\n')
print('Faster route :')
print(faster_route)
