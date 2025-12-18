from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def search_flights(source: str, destination: str):
    """Search cheapest flight between two cities"""
    try:
        flights = load_json("data/flights.json")
        options = [
            f for f in flights
            if f["source"] == source and f["destination"] == destination
        ]
        cheapest = min(options, key=lambda x: x["price"])
        logger.info("Flight selected successfully")
        return cheapest
    except Exception as e:
        logger.error(f"Flight search failed: {e}")
        return {"error": "Flight search failed"}