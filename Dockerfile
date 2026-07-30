FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY service/ ./service/


EXPOSE 8000

CMD uvicorn service.main:app --host 0.0.0.0 --port ${PORT:-8000}