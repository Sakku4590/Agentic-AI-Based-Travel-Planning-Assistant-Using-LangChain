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

    def run(self,user_query: str,source_city: str,destination_city: str,trip_days: int,hotel_budget: int) -> str:
        logger.info("Starting travel planning")

        # -------------------------------
        # Tool Calls
        # -------------------------------
        flight = search_flights.run({
            "source": source_city,
            "destination": destination_city
        })
        
        flight_note = ""
        if "error" in flight:
            flight_note = "⚠ No flight found in dataset"

        hotel = recommend_hotel.run({
            "city": destination_city,
            "max_price": hotel_budget
        })

        places = discover_places.run({
            "city": "Goa"
        })

        weather = get_weather.run({
            "lat": 15.2993,
            "lon": 74.1240
        })
        logger.info(f"Weather raw response: {weather}")
        
        if flight.get("type") == "connecting":
            airline = "Connecting Flight"
            flight_price = flight.get("total_price", 0)
            departure_time = flight["legs"][0].get("departure_time", "N/A")
            flight_route = flight.get("route")

        elif "price" in flight:
            airline = flight.get("airline", "N/A")
            flight_price = flight.get("price", 0)
            departure_time = flight.get("departure_time", "N/A")
            flight_route = f"{source_city} → {destination_city}"

        else:
            airline = "Not Available"
            flight_price = 0
            departure_time = "N/A"
            flight_route = f"{source_city} → {destination_city}"
        # -------------------------------
        # Safe Value Extraction
        # -------------------------------
        
        hotel_name = hotel.get("name", "N/A")
        hotel_price = hotel.get("price_per_night", 0)
        hotel_stars = hotel.get("stars", "N/A")

        temps = weather if isinstance(weather, list) else []

        available_weather_days = len(temps)

        if available_weather_days == 0:
            final_days = trip_days
        else:
            final_days = min(trip_days, available_weather_days)

        weather_lines = (
            [f"Day {i+1}: {temps[i]}°C" for i in range(final_days)]
            if temps else ["Weather data not available"]
        )

        # Ensure temps is a list
        temps = temps if isinstance(temps, list) else []


        # Ensure at least 1 day
        if available_weather_days == 0:
            final_days = trip_days
        else:
            final_days = min(trip_days, available_weather_days)

        if not temps:
            weather_lines = ["Weather data not available"]
        else:
            weather_lines = [f"Day {i+1}: {temps[i]}°C" for i in range(final_days)]
    
        itinerary = []
        for i in range(final_days):
            place_slice = places[i*2:(i+1)*2]
            if place_slice:
                itinerary.append(f"Day {i+1}: {', '.join(place_slice)}")
            else:
                itinerary.append(f"Day {i+1}: Leisure / Local Exploration")

        hotel_total = hotel_price * final_days
        food_budget = 1500 * final_days
        total_cost = flight_price + hotel_total + food_budget

        # -------------------------------
        # Prompt for Final Formatting
        # -------------------------------
        prompt = f"""
        You are a professional AI travel planner.

        Generate the trip itinerary in EXACTLY the following format
        (no extra headings, no explanations):

        Your {final_days}-Day Trip to {destination_city}

        Flight Selected:
        - {airline} (₹{flight_price}) – Route: {flight_route}
        {flight_note}

        Hotel Booked:
        - {hotel_name} (₹{hotel_price}/night, {hotel_stars}-star)

        Weather:
        {chr(10).join(weather_lines)}

        Itinerary:
        {chr(10).join(itinerary)}

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
