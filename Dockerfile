FROM ubuntu 

RUN apt-get update
RUN apt-get install -y python3.11 python3-pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["python", "server.py", "--database_file", "urls.db"]