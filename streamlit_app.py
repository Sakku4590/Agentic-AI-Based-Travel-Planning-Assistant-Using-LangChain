import streamlit as st
from agent.travel_agent import create_agent
from utils.logger import get_logger
from data.cities import INDIAN_CITIES

logger = get_logger(__name__)

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ AI Travel Planning Assistant")
st.markdown(
    "Plan your trip intelligently using AI-powered recommendations."
)

# -------------------------------
# Sidebar Inputs
# -------------------------------

st.sidebar.header("Trip Details")

source_city = st.sidebar.selectbox(
    "Source City",
    INDIAN_CITIES,
    index=INDIAN_CITIES.index("Delhi")
)

destination_city = st.sidebar.selectbox(
    "Destination City",
    INDIAN_CITIES,
    index=INDIAN_CITIES.index("Goa")
)

trip_days = st.sidebar.slider(
    "Number of Days",
    min_value=2,
    max_value=10,
    value=3
)

hotel_budget = st.sidebar.number_input(
    "Max Hotel Price per Night (₹)",
    min_value=1000,
    max_value=10000,
    value=3500,
    step=500
)


# -------------------------------
# Generate Button
# -------------------------------
if st.button("🚀 Generate Trip Plan"):
    if not source_city or not destination_city:
        st.warning("Please enter both source and destination cities.")
    else:
        with st.spinner("Planning your trip..."):
            try:
                logger.info("Streamlit UI triggered trip planning")

                agent = create_agent()

                query = f"""
                Plan a {trip_days}-day trip from {source_city} to {destination_city}.
                My hotel budget is {hotel_budget} per night.
                Include flight, hotel, places, weather and total cost.
                """

                result = agent.run(
                    user_query=query,
                    source_city=source_city,
                    destination_city=destination_city,
                    trip_days=trip_days,
                    hotel_budget=hotel_budget
                )

                st.success("Trip plan generated successfully!")
                st.markdown("---")
                st.markdown(result)

            except Exception as e:
                logger.error(f"Streamlit app failed: {e}")
                st.error("Something went wrong while generating the trip plan.")
                st.exception(e)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with LangChain, OpenAI & Streamlit")
