
FROM ubuntu:20.04

# Updating apt and install Firefox
RUN apt-get -y update
RUN apt-get -y install python3
RUN apt-get -y install --no-install-recommends ca-certificates curl firefox-esr firefox-geckodriver
RUN rm -fr /var/lib/apt/lists/*
RUN apt-get -y purge ca-certificates curl
RUN apt autoremove

# Set display port as an environment variable
ENV DISPLAY=:99

COPY . /usr/app
WORKDIR /usr/app

# pip Install Requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run WSGI server on port 80
EXPOSE 80
CMD gunicorn "app:app" -b "0.0.0.0:80"
