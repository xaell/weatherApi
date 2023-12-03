from flask import Flask, render_template, request, abort, Response, url_for, flash, redirect

from geopy.geocoders import Nominatim
import json
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '4c27c7fb80966bf0f26f75a3ed9ce0782ebc3ab92e6e6a9b'

def checkAPI(response):
    if (response.status_code == requests.codes.ok):
        print("Working")
    else:
        print("Error: ", response.status_code)

@app.route('/', methods=['GET','POST'])
@app.route('/weather', methods=['GET','POST'])
def weather():
    locator = Nominatim(user_agent="weatherAPI.py")
    location = locator.geocode("Champ de Mars, Paris, France")

    print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

    if request.method == "POST":
        #Get the info and replace city with it
        city = request.form["cityName"]
        country = request.form["countryName"]
    else:
        #Replace city with placeholder
        city = 'new york city'
        country = "new york"

    #empty dictionary
    api_url = 'https://geocoding-api.open-meteo.com/v1/search?name={}&count=1&language=en&format=json'.format(city)
    response = requests.get(api_url)
    checkAPI(response)
    results = (json.loads(response.text).get("results"))[0]

    info = {
        "city": city,
        "country": country,
        "lat": round(results.get('latitude')),
        "long": round(results.get('longitude'))
    }

    #get the weather
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,apparent_temperature,wind_speed_10m&daily=apparent_temperature_max,apparent_temperature_min,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7".format(round(info.get("lat"),2),round(info.get("long"),2))
    weather_response = requests.get(weather_url)
    checkAPI(weather_response)
    
    results = json.loads(weather_response.text)
    #TODO:
    #- Get the max and min and divide by 2
    #- Display them

    #DEBUGGING
    print(results)
    #DEBUGGING

    #This will overwrite the last info hashmap!!!
    info = {
        "city": city,
        "country": country,
        "date": results.get("daily").get("time"),
        "maxTemp": [round(num,2) for num in results.get("daily").get("apparent_temperature_max")]
    }

    days_of_week = []
    for x in range(len(info['date'])):
        #get day and append
        days_of_week.append(info["date"][x])
    
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