import config
from influxdb import InfluxDBClient

config = config.Config().cfg["database"]


def initialize():
    client = InfluxDBClient(config["host"], config["port"], config["username"], config["password"], config["name"])
    client.create_database(config["name"])
    return client
