#!/usr/bin/evn python
# -*- coding: UTF-8 -*-

from flask import Flask
app = Flask(__name__)

import socket
HOST = socket.gethostname()


@app.route("/")
def hello():
    return HOST + '-g'
