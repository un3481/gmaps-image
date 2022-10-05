
FROM python:3.10

# Adding Google Chrome to the repositories
RUN  apt-get update \
    && apt-get install -y wget gnupg ca-certificates \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Download the Chrome Driver
RUN apt-get -yqq install unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/ curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

COPY . /app
WORKDIR /usr/app

# pip Install Requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run WSGI server on port 80
CMD gunicorn "app:app" -b "0.0.0.0:80"
