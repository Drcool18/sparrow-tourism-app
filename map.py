import streamlit as st
import pandas as pd
import pydeck as pdk

# Load cleaned data (later replace with Snowflake connector)
df = pd.read_csv("cleaned_snowflake_map_data.csv")

st.set_page_config(page_title="India's Hidden Gems Map", layout="wide")
st.title("📍 Discover India's Hidden Gems")

# Sidebar filter by State
states = df['State/UT'].dropna().unique()
selected_state = st.sidebar.selectbox("Select a State to Explore", sorted(states))

# Filter by selected state
filtered_df = df[df['State/UT'] == selected_state]

# Create pydeck map with markers
view_state = pdk.ViewState(
    latitude=filtered_df['Latitude'].mean(),
    longitude=filtered_df['Longitude'].mean(),
    zoom=5,
    pitch=0
)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=filtered_df,
    get_position='[Longitude, Latitude]',
    get_radius=50000,
    get_color=[0, 100, 200, 160],
    pickable=True
)

tooltip = {
    "html": "<b>{Name}</b><br />{State/UT}",
    "style": {
        "backgroundColor": "white",
        "color": "black"
    }
}

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[layer],
    tooltip=tooltip
))

st.subheader(f"Explore {selected_state}")
for _, row in filtered_df.iterrows():
    st.markdown(f"### [{row['Name']}](#details-{row['Name'].replace(' ', '-')})")
    st.write(f"Coordinates: {row['Latitude']}, {row['Longitude']}")
    st.markdown("---")
