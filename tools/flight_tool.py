from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def search_flights(source: str, destination: str):
    """Find cheapest flight between source and destination"""
    try:
        flights = load_json("data/flights.json")

        options = [
            f for f in flights
            if f.get("from") == source and f.get("to") == destination
        ]

        if not options:
            logger.warning("No flights found")
            return {"error": "No flights available"}

        cheapest = min(options, key=lambda x: x.get("price", float("inf")))
        logger.info("Flight selected successfully")

        return {
            "airline": cheapest.get("airline"),
            "price": cheapest.get("price"),
            "departure_time": cheapest.get("departure_time")
        }

    except Exception as e:
        logger.error(f"Flight search failed: {e}")
        return {"error": str(e)}
