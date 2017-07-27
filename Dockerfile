FROM python:3.6.2

ADD requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt

# Add application source code
COPY . /app

WORKDIR /app
CMD gunicorn -b :8080 server:app -w 8 --log-level=debug
EXPOSE 8080
