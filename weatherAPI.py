from flask import Flask, render_template, request, abort, Response

import json
import requests

app = Flask(__name__)

city = "london"
country = "england"

@app.route('/', methods=['GET'])
@app.route('/weather', methods=['GET'])
def weather():
    city = 'london'
    api_url = 'https://geocoding-api.open-meteo.com/v1/search?name={}&count=1&language=en&format=json'.format(city)
    response = requests.get(api_url)
    if response.status_code == requests.codes.ok:
        print('Working')
    else:
        print("Error:", response.status_code)
    print("------------------------------Printing---------------------------")
    print(json.loads(response.text))
    return render_template('index.html', response=response)

#urlBuild = 'https://api.api-ninjas.com/v1/geocoding?city=' + city + '&country=' + country
#open data from api
if __name__ == "__main__":
    app.run(debug = True)