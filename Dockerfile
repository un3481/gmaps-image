
FROM ubuntu:20.04

# set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Updating apt and install Firefox
RUN apt-get -y update
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install --no-install-recommends ca-certificates curl firefox firefox-geckodriver

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
