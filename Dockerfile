FROM python:3.8

WORKDIR ~

RUN mkdir solver
WORKDIR ./solver

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1  -y

RUN apt-get install -y python3-opencv
RUN pip install opencv-python

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 3001

ENTRYPOINT ["python", "./app.py"]
