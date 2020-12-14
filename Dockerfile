FROM python:3.8.6-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "gunicorn", "-b", "0.0.0.0:5000", "application:application" ]