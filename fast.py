import folium
import os

def get_coord():
    stations={"Paris-Montparnasse": (48.84064284370186,2.319820501512474),
            "Clermont-La Pardieu": (45.76691187923342,3.134295625201944),
            "Lyon-Perrache": (45.748088539684176, 4.823194036939477)}
    return stations


m = folium.Map(location=[48.84064284370186,2.319820501512474])
icon = folium.DivIcon(html="your temperature here")
i = 1
for station, coords in get_coord().items():
    icon = folium.DivIcon(html= f'<h4>{i}</h4>')
    folium.Marker(coords, icon =icon).add_to(m)
    i= i+1
    folium.Marker(coords, popup=f'<strong>{ station}</strong><b>{ coords }</b>', tooltip= station ).add_to(m)
points = [(48.84064284370186,2.319820501512474),
          (45.76691187923342,3.134295625201944),
          (45.748088539684176, 4.823194036939477)]   
folium.PolyLine(points).add_to(m)
m.save('C:/Users/utilisateur/Desktop/Project02/Projet2_Groupe4/templates/shortestpath.html')
  

    
    