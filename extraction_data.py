import requests
import csv
import pprint
import cx_Oracle

# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()

#Extraction liste des villes
list_ville =[]
with open("villes_france.csv", "r") as file:
    data_ville = csv.reader(file)
    for row in data_ville:
        tupl_ville= tuple(row)
        tupl_ville = int(tupl_ville[10]), tupl_ville[3], int(tupl_ville[1])
        list_ville.append(tupl_ville)

#Insert into City table 
city_insert = """INSERT INTO city VALUES (:1, :2)"""
cur.executemany(city_insert, list_ville)

#Extraction liste des départements
list_departement= []
with open("departement2020.csv", "r", encoding='utf-8') as file:
    data_dept= csv.reader(file)
    next(data_dept)
    for row in data_dept:
        tupl_dept = tuple(row)
        tupl_dept = int(tupl_dept[0]), tupl_dept[6], int(tupl_dept[2])
        list_departement.append(tupl_dept)

    
#Insert into Departement table
departement_insert = """INSERT INTO DEPARTEMENT VALUES (:1, :2, :3)"""
cur.executemany(departement_insert, list_departement)

# Extraction liste gares 
lien ="https://ressources.data.sncf.com/api/records/1.0/search/?dataset=liste-des-gares&q=&rows=4281&facet=fret&facet=voyageurs&facet=code_ligne&facet=departement&refine.voyageurs=O"
list_gares= requests.get(lien).json()['records']
list_gare =[]
for liste in list_gares:
    try:
        list_gare.append({"id_station":liste['fields']['code_uic'],
                          "code_line":int(liste['fields']['code_ligne']), 
                          "station_name":liste['fields']['libelle'],
                          "station_commune":liste['fields']['commune'],
                          "lon":liste['fields']['x_wgs84'],
                          "lat":liste['fields']['y_wgs84']})
    except:
        pass

data_station = []
for ls in list_gare:
    tupl=tuple(ls.values())
    tupl = tupl + (1,)
    data_station.append(tupl)




# #Insert into station table
station_insert = """INSERT INTO STATION VALUES (:1, :2, :3, :4, :5, :6, :7)"""
for data in data_station:
    try:
        cur.execute(station_insert, data)
        print("one row insert completed")
    except:
        pass
conn.commit()
cur.close()
conn.close()

print("Insert completed")



    





        

  


# lien1 = "https://9bf360f1-dcb2-40f2-acc3-dee3f60c8f20:@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A69123&to=admin%3Afr%3A75056&datetime=20200826T000000&"
# list_trajet= []
# list_trajet = requests.get(lien1).json()['journeys']
# pprint.pprint(list_trajet[0]['sections'][1])


