FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install httpx

COPY . .

EXPOSE 8000
#Docker is on host 128.0.0.1 with port 8000 exposed
ENTRYPOINT ["python", "server.py", "--host", "127.0.0.1"] 