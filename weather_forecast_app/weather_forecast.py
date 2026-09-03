import requests

api_key = input("Enter API Key: ")
city = input("Enter City: ")

url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
data = response.json()

if response.status_code == 200:
    print(f"\nWeather in {city.title()}:")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Humidity: {data['main']['humidity']}%")
    print(f"Conditions: {data['weather'][0]['description'].title()}")
else:
    print(f"Error: {data.get('message', 'Unknown error')}")