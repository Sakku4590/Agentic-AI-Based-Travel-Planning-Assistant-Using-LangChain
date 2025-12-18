from langchain.tools import tool
from services.data_loader import load_json
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def recommend_hotel(city: str, max_price: int):
    """Recommend best hotel based on price & rating"""
    try:
        hotels = load_json("data/hotels.json")
        filtered = [
            h for h in hotels
            if h["city"] == city and h["price_per_night"] <= max_price
        ]
        best = max(filtered, key=lambda x: x["rating"])
        logger.info("Hotel recommended successfully")
        return best
    except Exception as e:
        logger.error(f"Hotel recommendation failed: {e}")
        return {"error": "Hotel recommendation failed"}
