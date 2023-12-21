from flask import Flask, render_template, request, url_for, flash, redirect

from geopy.geocoders import Nominatim
import json
import requests

from datetime import datetime

#Saves the data of previous sessions
info = []

app = Flask(__name__)
app.config['SECRET_KEY'] = '4c27c7fb80966bf0f26f75a3ed9ce0782ebc3ab92e6e6a9b'

def checkAPI(response):
    if (response.status_code != requests.codes.ok):
        print("Error: ", response.status_code)

@app.route('/', methods=['GET','POST'])
@app.route('/weather', methods=['GET','POST'])
def weather():
    locator = Nominatim(user_agent="weatherAPI.py")

    if request.method == "POST":
        #Get the info and replace city with it
        city = request.form["cityName"]
        country = request.form["countryName"]

        stringBuilder = city + ", " + country
        location = locator.geocode(stringBuilder)

    else:
        #Replace city with initial placeholder
        city = "new york city"
        country = "new york"

        stringBuilder = city + ", " + country
        location = locator.geocode(stringBuilder)

    if location is None:
        #This will just return the current webpage if a valid country isn't found
        #Use js to give a warning about that
        flash("Inputted location could not be found")
        return redirect(url_for('weather'))
        #return redirect(url_for('weather'))
    
    info = {
        "city": city,
        "country": country,
        "lat": round(location.latitude, 2),
        "long": round(location.longitude, 2)
    }

    #get the weather
    weather_url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&current=temperature_2m,apparent_temperature,wind_speed_10m&daily=apparent_temperature_max,apparent_temperature_min,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=auto&forecast_days=7".format(round(info.get("lat"),2),round(info.get("long"),2))
    weather_response = requests.get(weather_url)
    checkAPI(weather_response)
    
    results = json.loads(weather_response.text)

    """
    #DEBUGGING
    print(results)
    #DEBUGGING
    """

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
        #This should be a string
        #Split into year, month, and day
        days_of_week.append(info["date"][x])
        #TODO!!!
    
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


"""
NOTE:
1. Add error screen
    - I think you can just use flask alerts, 
"""