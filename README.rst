Altair-CDN
==========

Dockerized content delivery for Altair based charts

Tech Stack
----------

Altair-CDN is built on the following technologies:

- Docker_ : to simplify deployment
- Nginx_ : high-performance reverse proxy to speed up web page serving
- Gunicorn_ : a light-weight WSGI HTTP server
- Flask_ : a python microframework that makes web app development fun
- Altair_ : declarative visualization for python

.. _Docker: https://www.docker.com/
.. _Nginx: https://www.nginx.com/resources/wiki/
.. _Gunicorn:: http://gunicorn.org/
.. _Flask: http://flask.pocoo.org/
.. _Altair: https://altair-viz.github.io/


Installation
------------

.. code-block:: bash

    # 1. clone the repo
    git clone https://github.com/gramhagen/altair-cdn
    cd altair-cdn

    # 2. build the container
    docker build -t altair-cdn .

    # 3. run the container
    docker run -d -P -e USER=<USERNAME> -e PASSWORD=<PASSWORD> cdn

    # 4. fire up lets-nginx and point to published ports if https is desired
    https://github.com/smashwilson/lets-nginx


**note: https://getcarina.com/docs/ is a very easy to use service to try out when hosting docker containers

Usage
-----

HTTP POST requests are accepted to the service at the root level. They should have the altair json blob in the json
field of the request. A filename is generated and a png and html file is created to capture the provided charting data.
The png filename is provided back to the client.

HTTP GET requests are accepted to the service at the root level. These should match provided resources from previous
POST requests.

Additionally some basic status information can be accessed via HTTP GET at /status