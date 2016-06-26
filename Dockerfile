FROM alpine
MAINTAINER me@huy.im

RUN mkdir /app
ADD app.py /app
ADD requirements.txt /app/
WORKDIR /app
EXPOSE 8000

RUN apk add --update python python-dev py-pip gcc musl-dev libxml2-dev libxslt-dev
RUN rm -rf /var/cache/apk/*
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-w 4", "-b :8000", "app"]


