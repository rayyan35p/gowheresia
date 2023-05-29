from flask import Flask, render_template, request
import requests
import json

MY_API_KEY = "Enter your API Key here"
API_KEY = MY_API_KEY


class Location():
  API_KEY = MY_API_KEY

  def __init__(self, locationid, name, distance, address):
    self.locationid = locationid
    self.name = name
    self.distance = distance
    self.address = address

  def getName(self):
    return self.name

  def getImage(self):
    API_KEY = MY_API_KEY
    headers = {"accept": "application/json"}
    response = requests.get(
      "https://api.content.tripadvisor.com/api/v1/location/" +
      self.locationid + "/photos",
      headers=headers,
      params={
        'key': API_KEY
      }).json()

    try:
      return response.get('data')[0].get('images').get('large').get('url')
    except:
      return "https://www.escapeauthority.com/wp-content/uploads/2116/11/No-image-found.jpg"

  def getReviews(self):
    API_KEY = MY_API_KEY
    headers = {"accept": "application/json"}
    response = requests.get(
      "https://api.content.tripadvisor.com/api/v1/location/" +
      self.locationid + "/reviews",
      headers=headers,
      params={
        'key': API_KEY
      }).json()
    reviews = ""
    try:
      for items in response.get('data'):
        reviews = reviews + items.get('text') + "\n"
      return reviews
    except:
      return "No Reviews"


def get_points_of_interest(location):

  url = 'https://api.content.tripadvisor.com/api/v1/location/search'
  params = {'key': API_KEY, 'searchQuery': location}

  headers = {"accept": "application/json"}

  response = requests.get(url, headers=headers, params=params).json()
  #put try exception in case of no results
  location_id1 = response.get('data')[0].get('location_id')
  response2 = requests.get(
    'https://api.content.tripadvisor.com/api/v1/location/' + location_id1 +
    '/details',
    headers=headers,
    params={
      'key': API_KEY
    }).json()
  location_longitude = response2.get('longitude')
  location_latitude = response2.get('latitude')
  latLong = location_latitude + "," + location_longitude
  print(latLong)

  response3 = requests.get(
    'https://api.content.tripadvisor.com/api/v1/location/nearby_search',
    headers=headers,
    params={
      'key': API_KEY,
      'latLong': latLong
    }).json()
  list_of_locations = []
  for locations in response3.get('data'):
    location_id2 = locations.get('location_id')
    location_name = locations.get('name')
    location_distance = locations.get('distance')
    location_address = locations.get('address_obj').get('address_string')
    new_location = Location(location_id2, location_name, location_distance,
                            location_address)
    list_of_locations.append(new_location)
  return list_of_locations