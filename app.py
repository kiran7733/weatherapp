from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "1ef088a9f620c538e8a36b7e18ed0864"  # Your API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            geo_params = {
                'q': city,
                'limit': 1,
                'appid': API_KEY
            }

            try:
                geo_response = requests.get(GEO_URL, params=geo_params)
                geo_response.raise_for_status()
                location = geo_response.json()

                if location:
                    lat, lon = location[0]['lat'], location[0]['lon']

                    weather_params = {
                        'lat': lat,
                        'lon': lon,
                        'appid': API_KEY,
                        'units': 'metric'
                    }

                    response = requests.get(BASE_URL, params=weather_params)
                    response.raise_for_status()
                    data = response.json()

                    if data.get('cod') == 200:
                        weather_data = {
                            'city': data['name'],
                            'temperature_celsius': data['main']['temp'],
                            'temperature_fahrenheit': (data['main']['temp'] * 9/5) + 32,
                            'description': data['weather'][0]['description'],
                            'icon': data['weather'][0]['icon'],
                            'humidity': data['main']['humidity'],
                            'wind_speed': data['wind']['speed']
                        }
                    else:
                        error = "Weather data not available."

                else:
                    error = "City not found. Please enter a valid city name."

            except requests.exceptions.RequestException as e:
                error = f"Network error: {str(e)}"

    return render_template('index.html', weather_data=weather_data, error=error)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
