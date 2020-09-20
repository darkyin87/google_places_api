import os
import json
import requests
from dotenv import load_dotenv
import csv
import urllib.parse

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey
        self.missing = open("Missing_Activities.csv", "w")

    def search_places_by_query(self, address_arr):
      query = ",".join(address_arr)
      inputtype = 'textquery'
      fields='name,business_status,formatted_address'
      endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
      params = {
        'fields': fields,
        'inputtype': inputtype,
        'input': query,
        'key': self.apiKey
      }
      params = urllib.parse.urlencode(params)
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
address_set = set()
import csv
with open("input.csv", "r") as f:
  reader = csv.reader(f, delimiter=",")
  for row in reader:
  #   full_address = row[0]
  #   if row[1]:
  #     full_address += "," + row[1]
  #   if row[2]:
  #     full_address += "," + row[2]
  #   if row[3]:
  #     full_address += "," + row[3]
    address_set.add(tuple(row))

  for item in address_set:
    addresses.append(list(item))

  # print(len(addresses))
  # print(addresses)


result_file = open("BOA_Activities_OperationalStatus.csv", "w")

csvwriter = csv.writer(result_file)
fields = ['input_name', 'input_address', 'output_name', 'output_address' , 'business_status']
csvwriter.writerow(fields)

for address in addresses:
  print("Searching for address: {}".format(address))
  candidates = places.search_places_by_query(address)
  if candidates is None:
    continue
  for candidate in candidates:
    candidate['input_name'] = "{}".format(address[0])
    candidate['input_address'] = ", ".join(address[1:])

    row = [
      candidate['input_name'],
      candidate['input_address'],
      candidate['name'],
      candidate['formatted_address'],
      candidate['business_status'] if 'business_status' in candidate else 'NOT_FOUND'
    ]
    csvwriter.writerow(row)

result_file.close()

