FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

RUN apk update && apk add zip
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
COPY . /app/
WORKDIR /app/

ENTRYPOINT ["python", "server.py"]
