<h1>Agentic AI Travel Planning Assistant</h1>

<h3>Overview</h3>

This project is an industry-ready Agentic AI Travel Planner that generates end-to-end travel itineraries using structured datasets and real-time weather data. It orchestrates multiple tools (flights, hotels, places, weather) with robust logging and defensive error handling to produce clear, human-readable itineraries in a business-required format.

<h3>Key Features</h3>

Agent-like orchestration with tool calls

Defensive coding against missing/partial data

Centralized logging for observability and debugging

Real-time weather via Open-Meteo (no API key)

Clean, business-ready output format

<h3>Tech Stack</h3>

Python 3.10+

LangChain (modern tool orchestration)

OpenAI (LLM)

Open-Meteo API

Streamlined project structure

<h3>Project Structure</h3>
Agentic-AI-Based-Travel-Planning-Assistant-Using-LangChain/
├── app.py
├── agent/
│   ├── __init__.py
│   └── travel_agent.py
├── tools/
│   ├── flight_tool.py
│   ├── hotel_tool.py
│   ├── places_tool.py
│   └── weather_tool.py
├── services/
│   └── data_loader.py
├── utils/
│   └── logger.py
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
├── logs/
│   └── app.log
├── requirements.txt
└── README.md
<h3>Setup Instructions</h3>

<h6>Create & activate virtual environment</h6>

python -m venv venv
venv\Scripts\activate

<h6>Install dependencies</h6>

pip install -r requirements.txt

<h6>Set OpenAI API Key (Windows)</h6>

setx OPENAI_API_KEY "your_api_key_here"

Restart the terminal and re-activate the venv.

<h6>Run the app</h6>

python app.py

<h3>Example Output</h3>
Your 3-Day Trip to Goa (Feb 12–14)


Flight Selected:
- IndiGo (₹4800) – Departs Delhi at 14:00


Hotel Booked:
- Sea View Resort (₹3200/night, 4-star)


Weather:
- Day 1: 31°C
- Day 2: 30°C
- Day 3: 29°C


Itinerary:
Day 1: Baga Beach, Candolim Market
Day 2: Basilica of Bom Jesus, Old Goa Heritage Walk
Day 3: Water Sports at Calangute


Estimated Total Budget:
- Flight: ₹4800
- Hotel: ₹6400
- Food & Travel: ₹2500
-------------------------------------
Total Cost: ₹13,700
<h3>Logging & Debugging</h3>

Logs are written to logs/app.log

Errors such as missing data or no flights found are logged with context

The app continues gracefully with safe defaults

<h3>Notes for Reviewers</h3>

JSON schema alignment is handled explicitly in tools

Missing data is handled with fallbacks (no crashes)

Output formatting matches business requirements exactly

<h3>Future Enhancements</h3>

Streamlit UI

Structured JSON + text output

Ranking (cheapest vs fastest)

Retry/fallback logic

Dockerization

Author: Sk Sakline Mustaque