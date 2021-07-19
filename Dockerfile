FROM python:3

WORKDIR /

COPY ["requirements.txt", "./"]

COPY . .

RUN python3 -m pip install -r requirements.txt
CMD ["python3", "streamAPI_to_pubsub.py"]
