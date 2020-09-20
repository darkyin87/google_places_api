import os
import json
import requests
from dotenv import load_dotenv
import csv

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
        self.missing = open("Missing_Activities.csv", "w")

    def search_places_by_query(self, query):
      inputtype = 'textquery'
      fields='business_status,formatted_address'
      endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
      params="?fields={}&inputtype={}&input={}&key={}".format(fields, inputtype, query, self.apiKey)
      print(endpoint_url+params)
      res = requests.get(endpoint_url+params)
      response = json.loads(res.content)
      if response['status'] != 'OK':
        if response['status'] == 'ZERO_RESULTS':
          self.missing.write("{}\n".format(query))
          return None
          # raise Exception("No resuls found for query: {}".format(query))
        print(res.status_code)
        raise Exception("Error finding with query: {}, Response: {}".format(query, response))
      return response['candidates']

#load api key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
# print(API_KEY)
places = GooglePlaces(API_KEY)
results = []

addresses = []
import csv
with open("input.csv", "r") as f:
  # lines = f.read().splitlines()
  # parts = lines.spli(",")
  reader = csv.reader(f, delimiter=",")
  for row in reader:
    full_address = row[0]
    if row[1]:
      full_address += "," + row[1]
    if row[2]:
      full_address += "," + row[2]
    if row[3]:
      full_address += "," + row[3]
    addresses.append(full_address)

# print (addresses)




result_file = open("BOA_Activities_OperationalStatus.csv", "w")
result_file.write("'name', 'formatted_address', 'business_status'\n")

for address in addresses:
  print("Searching for address: {}".format(address))
  candidates = places.search_places_by_query(address)
  if candidates is None:
    continue
  for candidate in candidates:
    candidate['name'] = "'{}'".format(address)

    result_file.write("{}, {}, {}\n".format(
      candidate['name'],
      candidate['formatted_address'],
      candidate['business_status'] if 'business_status' in candidate else 'NOT_FOUND')
    )
    results.append(candidate)

result_file.close()



# print(results)
# csv_columns = ['name', 'formatted_address', 'business_status']
# output_file = 'output.csv'
# with open(output_file, 'w') as csvfile:
#   writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#   writer.writeheader()
#   for data in results:
#       writer.writerow(data)