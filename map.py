import folium
import os
import cx_Oracle

# DataBase Connexion
conn = cx_Oracle.connect("admin", "Simplon.co63", "simplon_high")
print(conn.version)
cur=conn.cursor()
# Faster Route
coord_depart_query = """select id_station, station_name, lat, lon from station 
                        where id_station =(
                            select depart_station from trip where id_trip = (
                                select min(id_trip) from trip where type_trip ='F'
                                )
                            )"""

coord_query = """SELECT  S.ID_STATION, S.STATION_NAME, S.LAT, S.LON FROM STATION S, TRIP T
                    WHERE S.ID_STATION = T.ARRIVAL_STATION 
                    AND T.TYPE_TRIP = 'F'

                    ORDER BY T.ID_TRIP""" 
cur.execute(coord_depart_query)
coords_depart = cur.fetchone()
cur.execute(coord_query)
coords = cur.fetchall()
stations= {}
stations[coords_depart[1]] = coords_depart[2], coords_depart[3]
for coord in coords:
    stations[coord[1]] = coord[2], coord[3]
  
points = []
for cdr in stations.values():
    points.append(stations.values())



m = folium.Map(location=[48.84064284370186,2.319820501512474])

i = 1
for station, coords in stations.items():
    icon = folium.DivIcon(html= f'<h4>{i}</h4>')
    folium.Marker(coords, icon =icon).add_to(m)
    i= i+1
    if i <= 2: 
        folium.Marker(coords,icon=folium.Icon(color='red', icon='info-sign'), popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
    elif i>94:
        folium.Marker(coords,icon=folium.Icon(color='green', icon='info-sign'), popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
    else:
        folium.Marker(coords,popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
  
folium.PolyLine(points, color = 'red').add_to(m)
m.save('C:/Users/utilisateur/Desktop/Project02/Projet2_Groupe4/templates/faster.html')
  
# Greener Route
coord_depart_query = """select id_station, station_name, lat, lon from station 
                        where id_station =(
                            select depart_station from trip where id_trip = (
                                select min(id_trip) from trip where type_trip ='C'
                                )
                            )"""

coord_query = """SELECT  S.ID_STATION, S.STATION_NAME, S.LAT, S.LON FROM STATION S, TRIP T
                    WHERE S.ID_STATION = T.ARRIVAL_STATION 
                    AND T.TYPE_TRIP = 'C'

                    ORDER BY T.ID_TRIP""" 
cur.execute(coord_depart_query)
coords_depart = cur.fetchone()
cur.execute(coord_query)
coords = cur.fetchall()
stations= {}
stations[coords_depart[1]] = coords_depart[2], coords_depart[3]
for coord in coords:
    stations[coord[1]] = coord[2], coord[3]
  
points = []
for cdr in stations.values():
    points.append(stations.values())



m = folium.Map(location=[48.84064284370186,2.319820501512474])

i = 1
for station, coords in stations.items():
    icon = folium.DivIcon(html= f'<h4>{i}</h4>')
    folium.Marker(coords, icon =icon).add_to(m)
    i= i+1
    if i <= 2: 
        folium.Marker(coords,icon=folium.Icon(color='red', icon='info-sign'), popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
    elif i>94:
        folium.Marker(coords,icon=folium.Icon(color='green', icon='info-sign'), popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
    else:
        folium.Marker(coords,popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station).add_to(m)
  
folium.PolyLine(points, color = 'green').add_to(m)
m.save('C:/Users/utilisateur/Desktop/Project02/Projet2_Groupe4/templates/greener.html')
    
    
conn.commit()
cur.close()
conn.close()