FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install httpx

COPY . .

EXPOSE 80

ENTRYPOINT ["python", "server.py", "--database_file", "urls.db"]