import requests

def get_weather(city, api_key):
    url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Using a dictionary for parameters is safer and cleaner than f-strings
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        # A timeout prevents the script from freezing if the network fails
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            print(f"\nWeather in {city.title()}:")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Conditions: {data['weather'][0]['description'].title()}")
        else:
            print(f"Error: {data.get('message', 'Unknown error').capitalize()}")
            
    except requests.exceptions.RequestException:
        print("\nError: Unable to connect to the API. Check your internet connection.")

if __name__ == "__main__":
    # .strip() removes accidental whitespace from user input
    user_api_key = input("Enter API Key: ").strip()
    user_city = input("Enter City: ").strip()
    
    # Input validation prevents running the request with empty values
    if user_api_key and user_city:
        get_weather(user_city, user_api_key)
    else:
        print("Error: API Key and City cannot be empty.")

