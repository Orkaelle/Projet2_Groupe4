'''
This file is used to calculate the global time of the fastest journey,
and the total CO2 emissions of the grennest one.
'''

import csv
import datetime

co2 = []

print('\n')

with open('faster.csv', newline='') as f:
    reader = list(csv.reader(f))

    depart_time = reader[0][-3]
    arrival_time = reader[-1][-3]

    start = datetime.datetime.strptime(depart_time, '%Y%m%dT%H%M%S%f')
    end = datetime.datetime.strptime(arrival_time, '%Y%m%dT%H%M%S%f')

    total_time = end - start
    print('Total time :')
    print(total_time)

print('\n')

with open('greener.csv', newline='') as g:
    reader = csv.reader(g)

    for row in reader:
        co2.append(float(row[-2]))

    total_co2 = round(sum(co2), 4)
    print('Total CO2 (gEC) :')
    print(total_co2)

print('\n')
