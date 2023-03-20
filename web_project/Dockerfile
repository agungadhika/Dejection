FROM python:3.9-alpine

WORKDIR /app

ADD . /app/

EXPOSE 8005

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /app

ENTRYPOINT ["python3"]

CMD ["manage.py", "runserver", "0.0.0.0:8005"]
