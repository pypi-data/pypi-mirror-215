import yaml
import pymysql
import configparser
import os

def connect_to_lims(config=None, environment=None):
    config = configparser.ConfigParser()
    config.read('config.ini')

    config_file = config.get('shared', 'config_file')
    environment = config.get('shared', 'environment')

    if config_file is None or environment is None:
        raise ValueError("Options cmhlims.lims_config_yaml and cmhlims.lims_environment must be set before using cmhlims functions.")

    with open(config_file, 'r') as file:
        lims_config = yaml.safe_load(file)

    if environment not in lims_config:
        raise ValueError("LIMS environment not found in configuration YAML: " + environment)

    lims_config = lims_config[environment]

    db_con = pymysql.connect(
        user=lims_config['username'],
        password=lims_config['password'],
        host=lims_config['host'],
        database=lims_config['database'],
        ssl_ca=lims_config['sslca'],
        autocommit=True
    )

    return db_con
