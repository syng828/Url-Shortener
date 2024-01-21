FROM python:3.9-slim-buster

WORKDIR /backend

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./backend .

EXPOSE 8000

ENTRYPOINT ["python", "server.py"] 