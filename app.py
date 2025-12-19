from agent.travel_agent import create_agent
from utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("AI Travel Agent started")

    agent = create_agent()

    query = """
    Plan a 3-day trip from Delhi to Goa.
    My hotel budget is 3500 per night.
    Include flight, hotel, places, weather and total cost.
    """

    result = agent.run(query)

    print("\n===== AI TRAVEL PLAN =====\n")
    print(result)

if __name__ == "__main__":
    main()
