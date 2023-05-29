from flask import Flask, render_template, request
import requests
from main import get_points_of_interest, Location, MY_API_KEY

app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/results', methods=['POST'])
def search():
  query = request.form['query']
  results = get_points_of_interest(query)
  return render_template('results.html', results=results)

@app.route('/location/<locationid>')
def details(locationid):
  headers = {"accept": "application/json"}
  response2 = requests.get(
    'https://api.content.tripadvisor.com/api/v1/location/' + locationid +
    '/details',
    headers=headers,
    params={
      'key': API_KEY
    }).json()
  location_id2 = response2.get('location_id')
  location_name = response2.get('name')
  location_address = response2.get('address_obj').get('address_string')
  new_location = Location(location_id2, location_name, 0,
                            location_address)
  return render_template('details.html', location=new_location)


API_KEY = MY_API_KEY
