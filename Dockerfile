FROM alpine
MAINTAINER me@huy.im

RUN mkdir /app
ADD app.py /app
ADD requirements.txt /app/
WORKDIR /app
EXPOSE 8000

RUN apk add --update python py-pip 
RUN rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "app", "-w 2", "-b :8000"]


