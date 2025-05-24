import streamlit as st
import pandas as pd

# Load local CSV (replace with Snowflake connection later)
df = pd.read_csv("sparrow_tourism_with_images.csv")  # If hosting online, use a Snowflake connector

st.set_page_config(page_title="Sparrow - Explore My Desh", layout="wide")
st.markdown("""
    <style>
    body {
        background-color: #f2faff;
    }
    .main {
        background-color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🕊️ Sparrow App")
page = st.sidebar.radio("Navigate", ["Map", "Explore", "Responsible Tourism", "Trip Calculator"])

# -------------------- PAGE 1: Map ------------------------
if page == "Map":
    st.title("📍 Discover India's Hidden Gems")
    if 'Latitude' in df.columns and 'Longitude' in df.columns:
        df = df.dropna(subset=['Latitude', 'Longitude'])
        df = df.astype({"Latitude": "float", "Longitude": "float"})
        st.map(df[['Latitude', 'Longitude']])
    else:
        st.warning("No location data available.")

    st.write("Click below to explore places in table format:")
    st.dataframe(df[['Name', 'State/UT', 'Type', 'Best Time to Visit']])

# -------------------- PAGE 2: Explore ------------------------
elif page == "Explore":
    st.title("🔍 Explore Lesser-Known Places")
    for idx, row in df.iterrows():
        with st.expander(f"{row['Name']} ({row['State/UT']})"):
            if pd.notna(row.get("Image_URL")):
                st.image(row["Image_URL"], width=600)
            st.markdown(f"**Type:** {row['Type']}")
            st.markdown(f"**Uniqueness:** {row['Uniqueness Factor']}")
            st.markdown(f"**Things to Do:** {row['Things to Do']}")
            st.markdown(f"**Cuisine:** {row['Local Cuisine Specialties']}")
            st.markdown(f"**Cultural Events:** {row['Cultural Events']}")

# -------------------- PAGE 3: Responsible Tourism ------------------------
elif page == "Responsible Tourism":
    st.title("🌿 Responsible Tourism Guidelines")

    st.markdown("### 🌍 Principles of Responsible Tourism")
    st.success("""
- Leave nature's treasures untouched.
- Learn local customs; engage with humility.
- Choose eco-friendly transport.
- Respect the rhythm of places—speak gently.
- Support artisans and local guides.
- Ask before taking photos of people or sacred spaces.
- Avoid feeding wild animals.
- Be water-conscious.
- Dress modestly at cultural sites.
- Travel is an invitation to responsibility.
- Choose impact over Instagram.
- Silence is often respectful.
- Slow travel > checklist travel.
- Avoid exploitative animal experiences.
    """)

    st.markdown("### 🚯 Waste Disposal & Plastic Use")
    st.info("""
- Carry waste until you find a bin.
- Avoid single-use plastics.
- Don’t treat compostable as litterable.
- Refuse excessive packaging.
- Be the traveler who takes their trash back.
    """)

    st.markdown("### 🐘 Wildlife & Cultural Sensitivity")
    st.warning("""
- Observe animals quietly from afar.
- Never feed them human food.
- Respect sacred spaces: remove shoes, dress appropriately.
- Don’t treat festivals like performances.
- Modesty shows respect.
    """)

# -------------------- PAGE 4: Travel Calculator ------------------------
elif page == "Trip Calculator":
    st.title("🧮 Travel Cost Calculator")
    st.markdown("Estimate your travel cost based on distance and mode of transport.")

    distance = st.number_input("Distance in kilometers:", min_value=0)
    mode = st.selectbox("Choose Mode of Travel:", ["Bus", "Train", "Taxi"])

    rate = {"Bus": 1.5, "Train": 1.0, "Taxi": 10.0}

    if distance > 0:
        cost = distance * rate[mode]
        st.success(f"Estimated cost by {mode}: ₹{cost:.2f}")
