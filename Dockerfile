FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential apt-utils
RUN apt-get install -y libxml2-dev libxslt-dev lib32z1-dev python-lxml

COPY . /app
ENV HOME=/app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "application.py" ]