from flask import Flask, render_template, request, abort, Response, url_for, flash, redirect

import json
import requests
from usefulFunctions import get_date_day

app = Flask(__name__)
app.config['SECRET_KEY'] = '4c27c7fb80966bf0f26f75a3ed9ce0782ebc3ab92e6e6a9b'

city = "london"
country = "england"

def checkAPI(response):
    if (response.status_code == requests.codes.ok):
        print("Working")
    else:
        print("Error: ", response.status_code)

@app.route('/', methods=['GET','POST'])
@app.route('/weather', methods=['GET','POST'])
def weather():
    #empty dictionary
    info = {}
    #Placeholder
    city = 'london'
    api_url = 'https://geocoding-api.open-meteo.com/v1/search?name={}&count=1&language=en&format=json'.format(city)
    response = requests.get(api_url)
    checkAPI(response)
    results = (json.loads(response.text).get("results"))[0]
    name = results.get('name')
    lat = round(results.get('latitude'))
    long = round(results.get('longitude'))
    country = results.get('country')

    info["name"] = name
    info["country"] = country

    #get the weather
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=temperature_2m_max,temperature_2m_min&temperature_unit=fahrenheit&timezone=auto".format(round(lat,2),round(long,2))
    weather_response = requests.get(weather_url)
    checkAPI(weather_response)
    results = json.loads(weather_response.text)   

    date = results.get("daily").get("time")
    temperature_max = results.get("daily").get("temperature_2m_max")
    temperature_min = results.get("daily").get("temperature_2m_min")

    info["date"] = date
    info["Tmax"] = temperature_max
    info["Tmin"] = temperature_min

    days_of_week = []
    for x in range(len(info['date'])):
        #get day and append
        days_of_week.append(get_date_day(info["date"][x]))
    
    info["days"] = days_of_week
        
    return render_template('weather.html', info = info)

@app.route('/test', methods=['GET','POST'])
def test():
    if request.method == 'POST':
        title = request.form['title']

        print(title)
    return render_template('test.html')

#urlBuild = 'https://api.api-ninjas.com/v1/geocoding?city=' + city + '&country=' + country
#open data from api
if __name__ == "__main__":
    app.run(debug = True)