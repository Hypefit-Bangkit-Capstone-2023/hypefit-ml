FROM python:3.10

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt

CMD ["python3", "api.py"]