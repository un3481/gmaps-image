
FROM python:3.10-buster

# Set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Update apt and install Chromium
RUN apt-get -y update
RUN apt-get -y install chromium chromium-driver libgl1

# Set display port as an environment variable
ENV DISPLAY=:99

# Copy files into image
COPY . /usr/app
WORKDIR /usr/app

# Pip Install Requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run WSGI server on port 80
EXPOSE 80
CMD gunicorn "app:app" -b "0.0.0.0:80"
