
FROM python:3.10

# Set noninteractive installation
ENV DEBIAN_FRONTEND=noninteractive

# Add build-essential
RUN apt-get -y install curl gnupg
RUN apt-get install g++ build-essential --yes

# Adding Google Chrome to the repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Unzip the Chrome Driver into /usr/local/bin directory
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

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
