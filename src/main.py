import logging
import os
import sys

from app import flask as application
import controller

logging.info("Python version: " + sys.version)
logging.info("Current directory: " + os.getcwd())


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000, debug=True)
