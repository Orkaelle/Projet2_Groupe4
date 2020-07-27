import requests
import csv
import pprint
import cx_Oracle

# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()


#getting the shortest strip between tow city

link_trips = "https://api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A69123&to=admin%3Afr%3A75056&datetime=20200803T060000&count=19&"