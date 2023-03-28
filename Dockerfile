FROM python:3.10

WORKDIR ~

RUN mkdir solver
WORKDIR ./solver

SHELL ["/bin/bash", "-c"]

RUN apt-get update && \
    apt-get install ffmpeg libsm6 libxext6 libgl1 curl python3-opencv -y && \
    rm -rf /var/lib/apt/lists/*

RUN curl https://raw.githubusercontent.com/jliuu1/solver-backend/main/requirements.txt -o requirements.txt && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 3001

ENTRYPOINT ["python", "./app.py"]
