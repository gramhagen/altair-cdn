# -*- coding: utf-8 -*-
"""WSGI app """

from app_factory import build_app


app = build_app()


if __name__ == '__main__':
    app.run()
