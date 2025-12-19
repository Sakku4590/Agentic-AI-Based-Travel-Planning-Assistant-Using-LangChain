import requests
from langchain.tools import tool
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def get_weather(lat: float, lon: float):
    """
    Returns daily max temperatures as a LIST
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&daily=temperature_2m_max"
            "&timezone=auto"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        temps = data.get("daily", {}).get("temperature_2m_max", [])

        logger.info("Weather fetched successfully")
        return temps  # ✅ ALWAYS RETURN A LIST

    except Exception as e:
        logger.error(f"Weather fetch failed: {e}")
        return [] 
