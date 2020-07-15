import requests
import pprint

lien ="https://ressources.data.sncf.com/api/records/1.0/search/?dataset=liste-des-gares&q=&rows=4281&facet=fret&facet=voyageurs&facet=code_ligne&facet=departement&refine.voyageurs=O"
list_gare =[]
list_gare= requests.get(lien).json()['records']
print(len(list_gare))
pprint.pprint(list_gare[2000])



