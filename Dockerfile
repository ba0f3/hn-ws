FROM alpine
MAINTAINER me@huy.im

RUN mkdir /app
WORKDIR /app
EXPOSE 8000

RUN apk add --update python py-pip
RUN rm -rf /var/cache/apk/*

ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD app.py /app

ENTRYPOINT ["gunicorn", "-w 4", "-b :8000", "app"]
