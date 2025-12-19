from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger
from data.nearby_cities import NEARBY_CITIES

logger = get_logger(__name__)

@tool
def search_flights(source: str, destination: str):
    """Find cheapest flight between source and destination"""
    try:
        flights = load_json("data/flights.json")

        # 1️⃣ Direct flights
        direct = [
            f for f in flights
            if f.get("from") == source and f.get("to") == destination
        ]

        if direct:
            return min(direct, key=lambda x: x["price"])

        logger.warning("No direct flight found, trying nearby cities")

        # 2️⃣ Try nearby cities
        for mid_city in NEARBY_CITIES.get(destination, []):
            leg1 = [
                f for f in flights
                if f.get("from") == source and f.get("to") == mid_city
            ]
            leg2 = [
                f for f in flights
                if f.get("from") == mid_city and f.get("to") == destination
            ]

            if leg1 and leg2:
                best_leg1 = min(leg1, key=lambda x: x["price"])
                best_leg2 = min(leg2, key=lambda x: x["price"])

                return {
                    "type": "connecting",
                    "route": f"{source} → {mid_city} → {destination}",
                    "total_price": best_leg1["price"] + best_leg2["price"],
                    "legs": [best_leg1, best_leg2]
                }

        return {"error": "No flights available"}

    except Exception as e:
        logger.error(f"Flight search failed: {e}")
        return {"error": str(e)}
