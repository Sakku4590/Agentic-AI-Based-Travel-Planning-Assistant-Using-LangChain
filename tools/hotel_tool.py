from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def recommend_hotel(city: str, max_price: int):
    """Recommend best hotel by stars within budget"""
    try:
        hotels = load_json("data/hotels.json")

        filtered = [
            h for h in hotels
            if h.get("city") == city and h.get("price_per_night", 0) <= max_price
        ]

        if not filtered:
            logger.warning("No hotels found")
            return {"error": "No hotels available"}

        best = max(filtered, key=lambda x: x.get("stars", 0))
        logger.info("Hotel recommended successfully")

        return {
            "name": best.get("name"),
            "price_per_night": best.get("price_per_night"),
            "stars": best.get("stars")
        }

    except Exception as e:
        logger.error(f"Hotel recommendation failed: {e}")
        return {"error": str(e)}
