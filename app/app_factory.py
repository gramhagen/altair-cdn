# -*- coding: utf-8 -*-
"""Application Factory"""

import json
import logging
import os
import time
import uuid

from altair import Chart
from datetime import datetime
from flask import Flask, request
from glob import glob1


def insert_image(image_dir, json_data, max_image_age=15):
    """Inserts and image into the image directory, removing old images

    Args:
        image_dir (str): base path to image directory
        json_data (str): vega-lite json representation of image
        max_image_age (int): number of days for images to be retained
    Returns:
        (str): image file name
    """

    # cleanup old images
    current_images = dict()
    for image in glob1(image_dir, '*.png'):
        full_path = os.path.join(image_dir, image)
        image_age = (time.time() - os.path.getmtime(full_path)) / (60 * 60 * 24)
        if image_age > max_image_age:
            os.remove(full_path)
        else:
            current_images[image] = True

    # generate image_id (avoiding collisions)
    for _ in range(10):
        image = '{}.png'.format(uuid.uuid4().hex)
        if image not in current_images:
            break
    else:
        raise ValueError('Could not find unused key for image')

    # save data to new image
    filename = os.path.join(image_dir, image)
    chart = Chart.from_json(json_data)
    chart.savechart(filename)

    # save data as html
    filename = os.path.join(image_dir, '{}.html'.format(image[:-4]))
    chart.savechart(filename)

    return image


def build_app():
    """Create flask app

    Returns:
        (object) : Flask application
    """
    app = Flask(__name__)

    app.config['START_TIME'] = datetime.now()
    app.config['POST_COUNT'] = 0

    # configure logging
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    handler = logging.StreamHandler()
    handler.setFormatter(fmt=logging.Formatter(fmt='[%(asctime)s %(levelname)s %(funcName)s:%(lineno)s] %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(level=logging.getLevelName(log_level.upper()))

    # check image directory
    image_dir = os.getenv('IMAGE_DIR', '/www/images')
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)
    app.config['IMAGE_DIR'] = image_dir

    @app.route('/', methods=['POST'])
    def save_image():
        """Save image file

        Returns:
            (status): imagefile name if successful or error message and status of result
        """

        try:
            app.logger.debug('received data: %s', request.json)
            image = insert_image(image_dir, request.json)
            app.config['POST_COUNT'] += 1
            return image, 201
        except Exception as e:
            return 'Error: {}'.format(e), 500

    @app.route('/status')
    def status():
        started = app.config['START_TIME'].strftime('%Y-%m-%d %H:%M:%S UTC')
        uptime = str(datetime.now() - app.config['START_TIME'])
        output = dict(started=started, uptime=uptime, post_count=app.config['POST_COUNT'])
        return json.dumps(output), 200

    app.logger.debug('created flask app')

    return app
