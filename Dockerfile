
FROM python:3.10

# Updating apt and install Firefox
RUN apt-get -y update
RUN apt-get -y install --no-install-recommends ca-certificates curl firefox-esr
RUN rm -fr /var/lib/apt/lists/*
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin
RUN apt-get -y purge ca-certificates curl

# Set display port as an environment variable
ENV DISPLAY=:99

COPY . /usr/app
WORKDIR /usr/app

# pip Install Requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run WSGI server on port 80
CMD gunicorn "app:app" -b "0.0.0.0:80"
