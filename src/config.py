__author__ = 'root'
import os
import yaml

class Config:
    cfg = None

    def __init__(self):
        with open(os.environ['STOCKBALL_HOME'] + "config.yaml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    def value(self, levels):
        ret = self.cfg[levels[0]]
        for level in levels[1:]:
            ret = ret[level]
        return ret