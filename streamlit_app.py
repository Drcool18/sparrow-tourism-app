import streamlit as st
import pandas as pd
import pydeck as pdk
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="🇮🇳 India's Hidden Gems", layout="wide")

session = get_active_session()

st.title("🇮🇳 Explore India's Hidden Gems")
st.sidebar.markdown("# 🧭 Locate")

st.write("""
Welcome to India's Hidden Gems! Discover off-the-beaten-path treasures across the country, from serene landscapes to cultural wonders.  
\n Use the sidebar to select a month and state to begin your exploration.
""")

# Load the whole table as pandas (for string operations)
df = session.table("tourism_data.public.map_data").to_pandas()
df = df[df['STATE'].notnull()]

# Extract all unique months from the TIME column strings
all_months = set()
for times in df['TIME'].dropna():
    months_list = [m.strip() for m in times.split(',')]
    all_months.update(months_list)
all_months = sorted(all_months)

# Insert "All" option at the beginning
all_months.insert(0, "All")

# Sidebar: Select a month, default no selection (index 0 => "All")
selected_month = st.sidebar.selectbox("Select a Month", all_months, index=0)

# Filter states based on month selection
if selected_month == "All":
    # No filtering by month, show all unique states
    filtered_df_for_states = df
else:
    # Filter rows where selected_month in TIME string (case-insensitive)
    filtered_df_for_states = df[df['TIME'].str.contains(selected_month, case=False, na=False)]

# Get sorted unique states from filtered data
states = sorted(filtered_df_for_states['STATE'].unique())

# Add a default empty selection at the top
states.insert(0, "Select a State")

# Sidebar: Select a state, default is empty ("Select a state")
selected_state = st.sidebar.selectbox("Select a State to Explore", states, index=0)

# When no state is selected
if selected_state == "Select a State":
    st.info("Please select a state from the sidebar to explore its hidden gems.")
else:
    # Filter places based on selected state and month
    if selected_state == "Select a state":
        final_filtered_df = pd.DataFrame()  # empty, no state selected yet
    else:
        if selected_month == "All":
            final_filtered_df = filtered_df_for_states[filtered_df_for_states['STATE'] == selected_state]
        else:
            final_filtered_df = filtered_df_for_states[
                (filtered_df_for_states['STATE'] == selected_state)
            ]
    
    if final_filtered_df.empty:
        if selected_state != "Select a state":
            st.warning(f"No places found for {selected_state} in {selected_month}.")
    else:
        view_state = pdk.ViewState(
            latitude=final_filtered_df['LATITUDE'].mean(),
            longitude=final_filtered_df['LONGITUDE'].mean(),
            zoom=5,
            pitch=0
        )
    
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=final_filtered_df,
            get_position='[longitude, latitude]',
            get_radius=50000,
            get_color=[0, 100, 200, 160],
            pickable=True
        )
    
        tooltip = {
            "html": "<b>{NAME}</b><br />{state}",
            "style": {"backgroundColor": "white", "color": "black"}
        }
    
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
        ))
    
        st.subheader(f"Explore {selected_state}")
        for idx, row in final_filtered_df.iterrows():
            place_name = row['NAME']
            if st.button(f"Explore {place_name}", key=f"explore_{place_name}_{idx}"):
                st.session_state['selected_place'] = place_name
                st.switch_page("pages/Details.py")
            st.write(f"Coordinates: {row['LATITUDE']}, {row['LONGITUDE']}")
            st.markdown("---")



