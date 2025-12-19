import streamlit as st
from agent.travel_agent import create_agent
from utils.logger import get_logger

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

source_city = st.sidebar.text_input(
    "Source City",
    value="Delhi"
)

destination_city = st.sidebar.text_input(
    "Destination City",
    value="Goa"
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
                Plan a 3-day trip from {source_city} to {destination_city}.
                My hotel budget is {hotel_budget} per night.
                Include flight, hotel, places, weather and total cost.
                """

                result = agent.run(query)

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
