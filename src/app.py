import logging
import os
import sys
from conf import Conf

from flask import Flask
from pyboot.decorator import Controller

ROOT_FOLDER = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/..")

logging.info("Python version: " + sys.version)
logging.info("Root folder: " + ROOT_FOLDER)

flask = Flask(__name__, template_folder="templates", static_folder="../public", static_url_path="/static")
Conf.get_instance().init(os.path.dirname(os.path.realpath(__file__)))

controller = Controller()