import os
from os.path import dirname, join
import logging
import logging.config
import configparser
config = None
configpath = None
default_config_path = join(dirname(__file__), "conf", "default.ini")


def set_config(basepath, configfile='development'):
    global config
    global configpath
    config = configparser.ConfigParser()
    configpath = join(basepath, 'conf', "%s.ini" % configfile)
    logging.debug("Reading config from: %s" % configpath)
    config.read(default_config_path)
    config.read(configpath)
    try:
        logging.config.fileConfig(config)
    except KeyError:
        # python 3.4 addresses the issue of direclty passing config obj
        try:
            # try app config
            logging.config.fileConfig(configpath)
        except KeyError:
            # fallback to default
            logging.config.fileConfig(default_config_path)

    return config
