import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Weather Dashboard", 
    page_icon="🌤️", 
    layout="centered"
)

# Header Section
st.title("🌤️ Real-Time Weather Dashboard")
st.markdown("Get comprehensive weather insights instantly, powered by your OpenWeather API key.")

# Sidebar for secure credentials
with st.sidebar:
    st.header("🔑 Configuration")
    user_api_key = st.text_input("OpenWeather API Key:", type="password", placeholder="Paste key here...").strip()
    st.markdown("---")
    st.markdown("[Get a free OpenWeather API key](https://openweathermap.org/)")
    st.markdown("💡 *Tip: Your key stays secure in your active session.*")

# Main content layout
st.markdown("### 📍 Search Location")
user_city = st.text_input("Enter City Name:", placeholder="e.g., London, Tokyo, New York").strip()

# Backend API Request Function
def get_weather(city, api_key):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            return True, data
        else:
            return False, data.get('message', 'Unknown error').capitalize()
            
    except requests.exceptions.RequestException:
        return False, "Unable to connect to the API. Check your internet connection."

# Action Button (use_container_width makes it look modern and span nicely)
if st.button("Get Weather Forecast", type="primary", use_container_width=True):
    if not user_api_key:
        st.warning("⚠️ Please enter your OpenWeather API Key in the sidebar.")
    elif not user_city:
        st.warning("⚠️ Please enter a city name.")
    else:
        with st.spinner("Fetching live weather data..."):
            success, result_data = get_weather(user_city, user_api_key)
            
            if success:
                # Extract values from dictionary
                city_name = result_data.get("name", user_city.title())
                country = result_data["sys"]["country"]
                temp = result_data["main"]["temp"]
                feels_like = result_data["main"]["feels_like"]
                humidity = result_data["main"]["humidity"]
                wind = result_data["wind"]["speed"]
                desc = result_data["weather"][0]["description"].title()
                
                # Visual separator
                st.divider()
                st.success(f"Weather successfully loaded for **{city_name}, {country}**!")
                
                # Display metrics in 3 clean columns
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(label="🌡️ Temperature", value=f"{temp}°C", delta=f"Feels {feels_like}°C")
                with col2:
                    st.metric(label="💧 Humidity", value=f"{humidity}%")
                with col3:
                    st.metric(label="💨 Wind Speed", value=f"{wind} m/s")
                
                # Styled info box for general description
                st.info(f"📋 **Current Sky Condition:** {desc}")
                
            else:
                st.error(f"❌ Error: {result_data}")