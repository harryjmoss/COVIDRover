FROM ubuntu:bionic

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3-pip
    
RUN pip3 install setuptools wheel
RUN pip3 install -r requirements.txt
