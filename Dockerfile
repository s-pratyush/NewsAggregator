FROM python:3.8-buster

ADD . /NewsAggregator

WORKDIR /NewsAggregator

RUN pip install --upgrade pip

RUN pip install -r requirements.txt && \
    python manage.py makemigrations && \
    python manage.py migrate

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
