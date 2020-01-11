FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /geomk
WORKDIR /geomk
COPY requirements.txt /geomk/
RUN pip install -r requirements.txt
COPY . /geomk/