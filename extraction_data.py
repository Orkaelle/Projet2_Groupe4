import requests
import pprint



# lien ="https://ressources.data.sncf.com/api/records/1.0/search/?dataset=liste-des-gares&q=&rows=4281&facet=fret&facet=voyageurs&facet=code_ligne&facet=departement&refine.voyageurs=O"
# list_gare =[]
# list_gare= requests.get(lien).json()['records']
# print(len(list_gare))
# pprint.pprint(list_gare[7])

lien1 = "https://9bf360f1-dcb2-40f2-acc3-dee3f60c8f20:@api.navitia.io/v1/coverage/sncf/journeys?from=admin%3Afr%3A69123&to=admin%3Afr%3A75056&datetime=20200826T000000&"
list_trajet= []
list_trajet = requests.get(lien1).json()['journeys']
pprint.pprint(list_trajet[0]['sections'][1])


