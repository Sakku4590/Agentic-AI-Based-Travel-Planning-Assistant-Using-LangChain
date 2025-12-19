from langchain_openai import ChatOpenAI
from utils.logger import get_logger

from tools.flight_tool import search_flights
from tools.hotel_tool import recommend_hotel
from tools.places_tool import discover_places
from tools.weather_tool import get_weather

import os
from dotenv import load_dotenv

load_dotenv()
logger = get_logger(__name__)

class TravelAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def run(self, user_query: str) -> str:
        logger.info("Starting travel planning")

        # -------------------------------
        # Tool Calls
        # -------------------------------
        flight = search_flights.run({
            "source": "Delhi",
            "destination": "Goa"
        })

        hotel = recommend_hotel.run({
            "city": "Goa",
            "max_price": 3500
        })

        places = discover_places.run({
            "city": "Goa"
        })

        weather = get_weather.run({
            "lat": 15.2993,
            "lon": 74.1240
        })

        # -------------------------------
        # Safe Value Extraction
        # -------------------------------
        airline = flight.get("airline", "N/A")
        flight_price = flight.get("price", 0)
        departure_time = flight.get("departure_time", "N/A")

        hotel_name = hotel.get("name", "N/A")
        hotel_price = hotel.get("price_per_night", 0)
        hotel_stars = hotel.get("stars", "N/A")

        day1_weather = f"{weather[0]}°C" if len(weather) > 0 else "N/A"
        day2_weather = f"{weather[1]}°C" if len(weather) > 1 else "N/A"
        day3_weather = f"{weather[2]}°C" if len(weather) > 2 else "N/A"

        day1_places = ", ".join(places[:2]) if len(places) >= 2 else "City Exploration"
        day2_places = ", ".join(places[2:4]) if len(places) >= 4 else "Local Sightseeing"
        day3_places = places[4] if len(places) >= 5 else "Leisure / Shopping"

        hotel_total = hotel_price * 2
        food_budget = 2500
        total_cost = flight_price + hotel_total + food_budget

        # -------------------------------
        # Prompt for Final Formatting
        # -------------------------------
        prompt = f"""
You are a professional AI travel planner.

Generate the trip itinerary in EXACTLY the following format
(no extra headings, no explanations):

Your 3-Day Trip to Goa (Feb 12–14)

Flight Selected:
- {airline} (₹{flight_price}) – Departs Delhi at {departure_time}

Hotel Booked:
- {hotel_name} (₹{hotel_price}/night, {hotel_stars}-star)

Weather:
- Day 1: {day1_weather}
- Day 2: {day2_weather}
- Day 3: {day3_weather}

Itinerary:
Day 1: {day1_places}
Day 2: {day2_places}
Day 3: {day3_places}

Estimated Total Budget:
- Flight: ₹{flight_price}
- Hotel: ₹{hotel_total}
- Food & Travel: ₹{food_budget}
-------------------------------------
Total Cost: ₹{total_cost}
"""

        response = self.llm.invoke(prompt)

        logger.info("Travel plan generated successfully")
        return response.content


def create_agent():
    """
    Factory method to create TravelAgent instance
    """
    return TravelAgent()
