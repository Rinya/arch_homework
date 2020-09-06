FROM python:3.9.0rc1-alpine3.12

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    python3 -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENTRYPOINT ["python", "/usr/src/app/main.py"]