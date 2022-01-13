#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pyCKWConfig.py
    Class file for pyCKWConfig.

    Author: Jeremy Diaz
    Year:   2022
"""

# Python Standard Library general imports
import logging

# pyCKW contants imports
from pyckw.pyCKWConstants import (
    DEFAULT_HOST,
    DEFAULT_SMARTMETER_PATH,
)

class pyCKWConfig(object):
    def __init__(self, pyCKW, meter_point, client_number, **kwargs):
        """The constructor.
        Args:
            kwargs (kwargs): Configuration options.
        """
        self.pyCKW = pyCKW
        self.config = kwargs
        self.config['meter_point'] = meter_point
        self.config['client_number'] = client_number
        self.pyCKW.info("Config loaded.")

    def dump_config(self):
        return {
            'host':             self.host,
            'smartmeter_path':  self.smartmeter_path,
            'meter_point':      self.meter_point,
            'client_number':    self.client_number
        }

    @property
    def host(self):
        return self.config.get("host", DEFAULT_HOST)
    
    @property
    def smartmeter_path(self):
        return self.config.get("smartmeter_path", DEFAULT_SMARTMETER_PATH)

    @property
    def meter_point(self):
        return self.config.get("meter_point")
    
    @property
    def client_number(self):
        return self.config.get("client_number")
