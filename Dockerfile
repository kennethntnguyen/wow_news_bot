# syntax=docker/dockerfile:1

FROM python:3.8.10-slim

ENV MONGODB_CONNECTION_STRING="" \
    DISCORD_BOT_TOKEN=""

WORKDIR /app

COPY . .

RUN python3.8 -m pip install --no-cache-dir -r requirements.txt

CMD ["python3.8","wow_news_bot.py"]
  