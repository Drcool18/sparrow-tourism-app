import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# --- Use active Snowpark session ---
session = get_active_session()

st.sidebar.markdown("# 💡 Tips")

# --- Sidebar ---
# Load the table
df = session.table("tourism_data.public.tips_data")

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

# --- Get selected place from session state ---
selected_place = st.session_state.get("selected_place", None)

if not selected_place:
    st.warning("No place selected. Please select a destination.")
    st.stop()

# --- Fetch row for the selected place ---
df = session.table("TIPS_DATA").filter(col("NAME") == selected_place).to_pandas()

if df.empty:
    st.error(f"No data found for {selected_place}")
    st.stop()

row = df.iloc[0]

# --- Define category flags ---
categories = {
    "General": True,
    "Urban": row["URBAN"] == 1,
    "Mountain": row["MOUNTAIN"] == 1,
    "Winter": row["WINTER"] == 1,
    "Humid": row["HUMID"] == 1,
    "Dry Hot": row["DRYHOT"] == 1,
    "Rural": row["RURAL"] == 1,
    "Monsoon": row["MONSOON"] == 1
}

# --- Responsible Tourism Guidelines ---
guidelines = {
    "General": {
        "dos": [
            "Respect local culture and traditions 🙏",
            "Support local businesses 🛍️🤝",
            "Minimize your environmental impact ♻️💡🐾",
            "Be mindful of your water usage 💧",
            "Learn a few phrases in the local language 🗣️",
            "Ask for permission before taking photos 📸🚫",
            "Be aware of local laws and regulations ⚖️",
            "Stay hydrated 🚰",
            "Carry a basic first-aid kit 🩹💊",
            "Have travel insurance 🛡️💼"
        ],
        "donts": [
            "Engage in exploitative tourism 🚫💸",
            "Haggle disrespectfully 🤔😠",
            "Leave trash behind 🗑️❌",
            "Touch or disturb wildlife ✋🚫🐾",
            "Disrespect religious sites or practices 🚫🛐",
            "Buy souvenirs from endangered species 🦒🐘🚫",
            "Drink tap water unless safe 🚱",
            "Over-consume alcohol 🍻❌",
            "Ignore local health advisories 😷⚠️"
        ]
    },
    "Urban": {
        "dos": [
            "Respect local customs and etiquette 🙏🤫",
            "Support local businesses and artists 🛍️🎨",
            "Use public transport 🚇🚌",
            "Be aware of your surroundings 🎒👀",
            "Stay hydrated 💧",
            "Dispose of waste properly 🚮♻️",
            "Walk or cycle when feasible 🚶‍♀️🚴‍♀️",
            "Check food hygiene 🍔",
            "Keep hands clean 🧼🖐️"
        ],
        "donts": [
            "Litter 🚮",
            "Be loud in residential areas 📢🚫",
            "Ignore local laws ⚖️🚫",
            "Fall for tourist scams 騙子🚫",
            "Vandalize public property 🏛️🚫",
            "Overuse ride-sharing apps 🚕🚫",
            "Drink too much alcohol 🍻❌",
            "Buy fake or unethical souvenirs 🚫 authenticity"
        ]
    },
    "Mountain": {
        "dos": [
            "Stay on marked trails 🚶‍♀️⬆️",
            "Pack out all trash 🎒🚮",
            "Dress in layers 🧥🧣🧤",
            "Acclimatize gradually 🌬️",
            "Carry water and snacks 💧🍫",
            "Inform someone of hiking plans 🗺️📞",
            "Check weather forecasts ☀️🌧️",
            "Wear proper footwear 🥾",
            "Use sun protection ☀️🧴🧢🕶️",
            "Know signs of altitude sickness 🤕🤢⬇️"
        ],
        "donts": [
            "Go off-trail 🚫🚶‍♀️",
            "Litter 🍂🚫",
            "Underestimate the weather 🥶🥵",
            "Ascend too quickly 🚀⬆️",
            "Feed wild animals 🍎🚫🦊",
            "Make excessive noise 📢🤫",
            "Take unnecessary risks 🚧",
            "Contaminate water sources 🚫🧼💧"
        ]
    },
    "Winter": {
        "dos": [
            "Dress in warm layers 🧥🧣",
            "Protect extremities 🧤🥾🧢",
            "Stay hydrated 💧",
            "Know frostbite and hypothermia signs 🧊🤒",
            "Use proper gear for snow activities 🎿🥾",
            "Inform someone of your plans 🗺️📞",
            "Be careful on ice ⚠️⛸️",
            "Drive cautiously 🚗❄️",
            "Use moisturizer and lip balm 🧴👄"
        ],
        "donts": [
            "Underdress 🥶👕🚫",
            "Ignore shivering/numbness 🥶 numb",
            "Drink excessively 🍻❌",
            "Go off-piste without training ⛷️🚫⚠️",
            "Drive without snow gear 🚗🌨️",
            "Litter in snow 🚮",
            "Touch metal with bare skin 🚫🖐️🧊"
        ]
    },
    "Humid": {
        "dos": [
            "Wear breathable clothing 👕",
            "Stay hydrated 💧",
            "Use insect repellent 🦟🧴",
            "Protect from sun ☀️🧴",
            "Watch for slippery paths ⚠️",
            "Respect ecosystems 🐾🌿",
            "Be aware of local wildlife 🐍🕷️",
            "Store food properly airtight",
            "Prevent fungal infections 🍄🧼"
        ],
        "donts": [
            "Wear heavy clothing 👕🥵",
            "Forget insect protection 🦟🚫",
            "Litter 🚮",
            "Swim in stagnant water 🏊‍♀️🚫🦠",
            "Feed or disturb animals 🐒🚫",
            "Underestimate heat 🥵",
            "Leave food exposed 🍲🐜",
            "Ignore heat exhaustion 😵‍💫🤒"
        ]
    },
    "Dry Hot": {
        "dos": [
            "Drink plenty of water 💧💧",
            "Wear loose light clothing 👕☀️",
            "Use sun protection 🧴🧢🕶️",
            "Plan for cooler hours ⏰🌙",
            "Inform someone of travel 🗺️📞",
            "Be aware of resource scarcity 🏜️",
            "Know signs of heatstroke 🤢😵‍💫",
            "Protect eyes from glare 🕶️",
            "Moisturize lips 👄🧴"
        ],
        "donts": [
            "Underestimate heat 🥵⚠️",
            "Neglect hydration 💧❌",
            "Wear dark tight clothes ⚫👕",
            "Go off-road unprepared 🚗🚨",
            "Litter 🚮",
            "Harm desert life 🌵🦎🚫",
            "Exert during peak heat 🏃‍♀️☀️",
            "Ignore flood warnings 🌊⚠️"
        ]
    },
    "Rural": {
        "dos": [
            "Engage respectfully 🤗",
            "Ask before entering property 🏡🚪❓",
            "Support farmers and artisans 🥕🎨💰",
            "Respect farms and animals 🚜🐄",
            "Dress modestly 👗👖",
            "Expect limited infrastructure 📶🔌",
            "Learn about plants/animals 🌿🕷️",
            "Stay hydrated 💧",
            "Use insect protection 🦟🧴"
        ],
        "donts": [
            "Treat locals as curiosities 🧐📸🚫",
            "Damage crops/fences 🌽🚧",
            "Leave trash 🚮",
            "Make loud noise 📢🤫",
            "Demand unavailable services 😤",
            "Disrespect traditions 🚫🙏",
            "Walk barefoot 🦶🚫",
            "Eat unsafe produce 🥛🍓🚫"
        ]
    },
    "Monsoon": {
        "dos": [
            "Carry waterproof gear ☔🧥🥾",
            "Ensure food and water hygiene 🍲🚰",
            "Use mosquito protection 🦟🧴🛌",
            "Watch for slippery roads ⚠️",
            "Check rain forecasts 🌧️⚠️",
            "Carry first-aid kit 🩹💊",
            "Protect electronics 📱防水",
            "Prepare for delays ⏰✈️",
            "Wash hands often 🧼🖐️"
        ],
        "donts": [
            "Wade through floodwaters 🚶‍♀️🌊🚫",
            "Eat unhygienic street food 🥗🚫",
            "Drink tap water 🚰🚫",
            "Ignore mosquito bites 🦟⚠️",
            "Drive recklessly on wet roads 🚗🚫",
            "Visit landslide-prone areas ⛰️🌊🚫",
            "Wear slow-drying fabrics 👕🚫",
            "Forget essential meds 💊🚫"
        ]
    }
}

# --- Display ---
st.markdown("# 🌍 Responsible Tourism: Do's and Don'ts")

for category, enabled in categories.items():
    if enabled and category in guidelines:
        st.markdown(f"## {category}")
        st.markdown("**✅ Do's:**")
        for tip in guidelines[category]["dos"]:
            st.markdown(f"- {tip}")
        st.markdown("**❌ Don'ts:**")
        for tip in guidelines[category]["donts"]:
            st.markdown(f"- {tip}")

col1, col2 = st.columns(2)

with col1:
    if st.button("← Back to Locator", key="back_locator"):
        st.switch_page("streamlit_app")

with col2:
    if st.button("← Back to Details", key="back_details"):
        st.switch_page("pages/Details.py")

