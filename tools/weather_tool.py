import requests
from langchain.tools import tool
from utils.logger import get_logger

logger = get_logger(__name__)

@tool
def get_weather(lat: float, lon: float):
    """Fetch weather from Open-Meteo"""
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max&timezone=auto"
        )
        res = requests.get(url, timeout=10).json()
        logger.info("Weather fetched successfully")
        return res["daily"]["temperature_2m_max"]
    except Exception as e:
        logger.error(f"Weather API failed: {e}")
        return {"error": "Weather service unavailable"}
