import logging
import os
import yaml
from logging import config


class Conf(object):
    __instance = None

    ROOT_FOLDER = ""
    IMAGES_FOLDER = ""

    def __init__(self):
        self.app_conf = None

    @staticmethod
    def get_instance():
        if Conf.__instance is None:
            Conf.__instance = Conf()
        return Conf.__instance

    def init(self, curr_dir):
        Conf.ROOT_FOLDER = os.path.abspath(curr_dir + "/..")

        stream = open(Conf.ROOT_FOLDER + "/conf/logging.yaml", "r")
        config.dictConfig(yaml.load(stream))
        stream.close()
        logging.debug("Logging initialized")

        stream = open(Conf.ROOT_FOLDER + "/conf/app.yaml", "r")
        self.app_conf = yaml.load(stream)
        stream.close()
        logging.debug("Config initialized")

        logging.info("ROOT_FOLDER: %s" % Conf.ROOT_FOLDER)

    def get_value(self, key):
        return self.app_conf[key]

    def set_value(self, key, value):
        self.app_conf[key] = value

    @staticmethod
    def get(key):
        return Conf.get_instance().get_value(key)

    @staticmethod
    def set(key, value):
        Conf.get_instance().set_value(key, value)
