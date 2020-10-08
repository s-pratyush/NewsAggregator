FROM python:3.8-buster

ADD . /NewsAggregator

WORKDIR /NewsAggregator

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]
