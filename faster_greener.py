import requests
import csv
import pprint
import cx_Oracle
import datetime




# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()


#getting data from faster.csv
list_faster =[]
with open ("faster.csv", "r", encoding="utf-8") as file:
    data_faster = csv.reader(file)
    for row in data_faster:
        tupl_faster= tuple(row)
        tupl_faster = int(tupl_faster[1][23:]),\
                      int(tupl_faster[3][23:]), \
                      datetime.datetime(int(tupl_faster[4][:4]), int(tupl_faster[4][4:6]), int(tupl_faster[4][6:8]), \
                      int(tupl_faster[4][9:11]), int(tupl_faster[4][11:13]), int(tupl_faster[4][13:])).strftime("%Y/%m/%d %H:%M:%S"),\
                      datetime.datetime(int(tupl_faster[6][:4]), int(tupl_faster[6][4:6]), int(tupl_faster[6][6:8]),\
                      int(tupl_faster[6][9:11]), int(tupl_faster[6][11:13]), int(tupl_faster[6][13:])).strftime("%Y/%m/%d %H:%M:%S"),\
                      int(tupl_faster[5]),\
                      float(tupl_faster[7]),\
                      (tupl_faster[8])
        
        list_faster.append(tupl_faster)
print(list_faster[0])

#Insert  faster trip into TRIP table
fatser_trip_insert = """INSERT INTO TRIP (DEPART_STATION, ARRIVAL_STATION, DEPARTURE_DATETIME, ARRIVAL_DATETIME, DURATION, CO2,TYPE_TRIP) 
                                VALUES (:1, :2, to_date(:3, 'YYYY/MM/DD  HH24:MI:SS'),to_date(:4, 'YYYY/MM/DD  HH24:MI:SS'), :5, :6, :7)"""
cur.executemany(fatser_trip_insert, list_faster)

 #getting data from greener.csv
list_greener =[]
with open ("greener.csv", "r", encoding="utf-8") as file:
    data_greener = csv.reader(file)
    for row in data_greener:
        tupl_grenner= tuple(row)
        tupl_grenner = int(tupl_grenner[1][23:]),\
                      int(tupl_grenner[3][23:]), \
                      datetime.datetime(int(tupl_grenner[4][:4]), int(tupl_grenner[4][4:6]), int(tupl_grenner[4][6:8]), \
                      int(tupl_grenner[4][9:11]), int(tupl_grenner[4][11:13]), int(tupl_grenner[4][13:])).strftime("%Y/%m/%d %H:%M:%S"),\
                      datetime.datetime(int(tupl_grenner[6][:4]), int(tupl_grenner[6][4:6]), int(tupl_grenner[6][6:8]),\
                      int(tupl_grenner[6][9:11]), int(tupl_grenner[6][11:13]), int(tupl_grenner[6][13:])).strftime("%Y/%m/%d %H:%M:%S"),\
                      int(tupl_grenner[5]),\
                      float(tupl_grenner[7]),\
                      (tupl_grenner[8])
      
        list_greener.append(tupl_grenner)
print(list_greener[0])

#Insert  greener trip into TRIP table
greener_trip_insert = """INSERT INTO TRIP (DEPART_STATION, ARRIVAL_STATION, DEPARTURE_DATETIME, ARRIVAL_DATETIME, DURATION, CO2,TYPE_TRIP) 
                                VALUES (:1, :2, to_date(:3, 'YYYY/MM/DD  HH24:MI:SS'),to_date(:4, 'YYYY/MM/DD  HH24:MI:SS'), :5, :6, :7)"""
cur.executemany(greener_trip_insert, list_greener)                     


conn.commit()
cur.close()
conn.close()

print("Insert completed")

        



