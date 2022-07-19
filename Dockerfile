FROM python:3.10-alpine
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

COPY . /app
WORKDIR /app

RUN apk update && \
    apk add zip && \
    pip install -r requirements.txt

ENTRYPOINT ["python", "server.py"]
