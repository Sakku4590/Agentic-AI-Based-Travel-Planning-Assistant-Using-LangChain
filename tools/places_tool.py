from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def discover_places(city: str):
    """Discover popular places"""
    try:
        places = load_json("data/places.json")
        top = [
            p["name"] for p in places
            if p["city"] == city and p["rating"] >= 4.0
        ]
        logger.info("Places discovered")
        return top[:5]
    except Exception as e:
        logger.error(f"Places discovery failed: {e}")
        return []
