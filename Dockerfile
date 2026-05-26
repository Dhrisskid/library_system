FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cached-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]

