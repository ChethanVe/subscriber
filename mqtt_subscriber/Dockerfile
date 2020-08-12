FROM python:3.7.4
EXPOSE 4900
RUN pip install paho-mqtt
RUN pip install requests
RUN apt-get update && apt-get install -y vim

COPY ./app /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["subscriber.py"]