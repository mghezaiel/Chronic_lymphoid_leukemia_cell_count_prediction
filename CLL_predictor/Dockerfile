# Dockerfile

FROM python:3.9-slim

# Author
LABEL maintainer.author.name = Morad Ghezaiel 
LABEL maintainer.email = ghezaiel.morad@gmail.com 

# Dependency list and app folders
COPY requirements.txt /tmp/requirements.txt
COPY src /home/src 
COPY data /home/data 
COPY app_data /home/app_data

# Library installation
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*
 
RUN pip3 install -r /tmp/requirements.txt

# Working directory 
WORKDIR /home/src

# Commands to run the app
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "CLL_predictor.py", "--server.port=8501","--server.address=0.0.0.0"]

