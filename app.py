import os
import json
import requests
from dotenv import load_dotenv
import csv

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_query(self, query):
      inputtype = 'textquery'
      fields='business_status,formatted_address'
      endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
      params="?fields={}&inputtype={}&input={}&key={}&".format(fields, inputtype, query, self.apiKey)
      res = requests.get(endpoint_url+params, params = params)
      response = json.loads(res.content)
      if response['status'] != 'OK':
        raise("Error finding with query: {}, Response: {}".format(query, response))
      if len(response['candidates']) == 0:
        raise("No resuls found for query: {}".format(query))
      return response['candidates']

#load api key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
# print(API_KEY)
places = GooglePlaces(API_KEY)
addresses = [
  'Dublin High School'
]
results = []
for address in addresses:
  candidates = places.search_places_by_query(address)
  for candidate in candidates:
    candidate['name'] = address
    results.append(candidate)

print(results)
csv_columns = ['name', 'formatted_address', 'business_status']
output_file = 'output.csv'
with open(output_file, 'w') as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
  writer.writeheader()
  for data in results:
      writer.writerow(data)