FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONUNBFFERED = 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
        && pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501

RUN mkdir -p ~/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
\n\
[browser]\n\
gatherUsageStats = false\n\
" > ~/.streamlit/config.toml

CMD ["streamlit", "run", "streamlit_app.py"]