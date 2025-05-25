import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Details")

# WEATHER API (WIP)
"""
import requests

# Add this function to fetch weather data
def get_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Add your OpenWeather API key here
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"
"""

# Get the current credentials
session = get_active_session()

st.sidebar.markdown("# 🗒️ Details")

# Load the table
df = session.table("tourism_data.public.info_data")

# Get distinct and sorted list of states
states = df.select("STATE").distinct().collect()
state_options = sorted([row["STATE"] for row in states])

# State selection dropdown
selected_state = st.sidebar.selectbox("Pick a State / UT:", state_options, key="state")

# Get places filtered by selected state
places_df = df.filter(df["STATE"] == selected_state).select("NAME").distinct()
place_options = sorted([row["NAME"] for row in places_df.collect()])

# Place selection dropdown (update session state on change)
selected_place = st.sidebar.selectbox("Choose a place:", place_options, key="place")

def get_place_detail(column_name):
    result = (
        df.filter(df["NAME"] == selected_place)
          .select(column_name)
          .distinct()
          .collect()
    )
    return result[0][column_name.upper()] if result else "Not available"

if selected_place:
    st.markdown(f"# 🏞️ Discover: {selected_place}")

    type = get_place_detail("TYPE")
    unique_info = get_place_detail("UNIQUE_INFO")
    activities = get_place_detail("ACTIVITIES")
    cuisine = get_place_detail("FOOD_INFO")
    events = get_place_detail("EVENTS")
    accomodation = get_place_detail("ACCOMODATION")
    accessibility_info = get_place_detail("ACCESSIBILITY_INFO")
    accessibility_rating = get_place_detail("ACCESSIBILITY_RATING")
    travel_rating = get_place_detail("TRAVEL")
    travel_info = get_place_detail("TRAVEL_INFO")
    initiatives = get_place_detail("INITIATIVES")

    st.write(f"**Type:** {type}")
    st.markdown(f"**Uniqueness:** {unique_info}")
    st.markdown(f"**Things to Do:** {activities}")
    st.markdown(f"**Cuisine:** {cuisine}")
    st.markdown(f"**Cultural Events:** {events}")
    st.markdown(f"**Accomodation:** {accomodation}")

    # Weather API (WIP)
    """
    with st.expander("Weather (Present)", expanded=False):
        # Fetch latitude and longitude for the selected place from MAP_DATA table
        map_df = session.table("tourism_data.public.map_data")
        coords = (
            map_df.filter(map_df["NAME"] == selected_place)
            .select("LATITUDE", "LONGITUDE")
            .collect()
        )
        
        if coords:
            lat = coords[0]["LATITUDE"]
            lon = coords[0]["LONGITUDE"]
        
            weather_data = get_weather(lat, lon, OPENWEATHER_API_KEY)
        
            if weather_data:
                st.markdown("### 🌤️ Current Weather")
                main = weather_data.get("weather")[0].get("main", "N/A")
                description = weather_data.get("weather")[0].get("description", "N/A").title()
                temp = weather_data.get("main", {}).get("temp", "N/A")
                humidity = weather_data.get("main", {}).get("humidity", "N/A")
                wind_speed = weather_data.get("wind", {}).get("speed", "N/A")
        
                st.write(f"**Condition:** {main} - {description}")
                st.write(f"**Temperature:** {temp} °C")
                st.write(f"**Humidity:** {humidity} %")
                st.write(f"**Wind Speed:** {wind_speed} m/s")
            else:
                st.warning("Weather data currently unavailable.")
        else:
            st.warning("Coordinates not found for this place.")
    """
    # WEATHER API END (WIP)
    
    if initiatives:
        st.markdown(f"##### Initiatives Existing / Ongoing:\n{initiatives}")

    else:
        st.write("#### Travel Details")
        if travel_rating == "Easy":
            st.success(travel_info)
        elif travel_rating == "Difficult":
            st.error(travel_info)
        elif travel_rating == "Moderate":
            st.warning(travel_info)
    
        with st.expander("Accessibility Information", expanded=False):
            if accessibility_rating == "Accessible":
                st.success(accessibility_info)
            elif accessibility_rating == "Not Accessible":
                st.error(accessibility_info)
            elif accessibility_rating == "Moderate":
                st.warning(accessibility_info)
else:
    st.markdown(f"# 🏞️ Discover ")
    st.warning("No place selected. Please select a place from the sidebar, or go back to the Locator.")

col1, col2 = st.columns(2)

with col1:
    if st.button("← Back to Locator", key="back_locator"):
        st.switch_page("streamlit_app")

with col2:
    if st.button("Go to Tips →", key="go_tips"):
        st.switch_page("pages/Tips.py")
