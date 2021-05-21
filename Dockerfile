# syntax=docker/dockerfile:1

FROM python:3.8

WORKDIR .

COPY requirements.txt requirements.txt

RUN python3.8 -m pip install -r requirements.txt

COPY . .

CMD ["python3.8","start_wow_news_bot.py"]
