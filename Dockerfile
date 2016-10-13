FROM python:2.7.12-slim

MAINTAINER gramhagen

# install packages
RUN apt-get update && \
    apt-get install -y nginx supervisor && \
    apt-get install -y curl git libcairo2-dev libjpeg62-turbo-dev libpango1.0-dev libgif-dev build-essential g++

# install node.js
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - && \
    apt-get install -y nodejs

# setup directory permissions
RUN mkdir /var/log/app && \
    mkdir -p /www/images && \
    chown www-data /www/images && \
    chgrp www-data /www/images && \
    chown www-data /var/log/app && \
    chgrp www-data /var/log/app

# install python requirements
WORKDIR /tmp
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt
# install dev version of altair until savechart is released
RUN pip install git+https://github.com/altair-viz/altair.git

# install node dependencies
WORKDIR /tmp
COPY package.json /tmp/package.json
RUN npm install && \
    mkdir -p /opt/app && \
    cp -a /tmp/node_modules /opt/app/

# add supervisor configuration
COPY config/supervisor.conf /etc/supervisor/conf.d/

# setup nginx
RUN rm -rf /var/lib/apt/lists/* && \
    rm -rf /etc/nginx/sites-enabled/* && \
    chown -R www-data:www-data /var/lib/nginx
COPY ./config/nginx.conf /etc/nginx/

# add authentication.sh
COPY authentication.sh /tmp/
RUN chmod 700 /tmp/authentication.sh

# pull in code
COPY ./app /opt/app/
ENV PYTHONPATH=/opt/app

EXPOSE 80

CMD ["/usr/bin/supervisord"]
