#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pyCKW.py
    Main class file for the pyCKW wrapper.

    Author: Jeremy Diaz
    Year:   2022
"""

# Python Standard Library general imports
import logging
import requests

# Python Standard Library specific imports
from datetime import datetime

# pyCKW class imports
from pyckw.pyCKWConfig import pyCKWConfig
from pyckw.pyCKWExceptions import pyCKWValidationError

# pyCKW contants imports
from pyckw.pyCKWConstants import (
    WRAPPER_NAME,
    WRAPPER_VERSION,
    RESOLUTIONS,
    DATA_TRANSLATIONS,
    FORMAT_DATES
)

__version__ = WRAPPER_VERSION
logger = logging.getLogger(WRAPPER_NAME)

class pyCKW(object):
    """Constructor"""
    def __init__(self, meter_point, client_number, **kwargs):
        self.info(f"{WRAPPER_NAME} {__version__} started.")
        self._config = pyCKWConfig(self, meter_point, client_number, **kwargs)
        if self.effective_level == logging.DEBUG:
            self.debug('Loaded Config:')
            for item in self._config.dump_config().items():
                self.debug(item)

    def get_consumption(self, resolution, start_date, end_date):
        # Check resolution validity
        if not RESOLUTIONS.get(resolution, None): raise pyCKWValidationError('Resolution value is not valid. Use {}.'.format(', '.join(RESOLUTIONS.keys())))
        self.debug('Resolution value \'{}\' is valid.'.format(resolution))

        # Check interval validity
        if not (start_date.strftime(FORMAT_DATES)): raise pyCKWValidationError('start_date is not valid. Use {}'.format(FORMAT_DATES))
        if not (end_date.strftime(FORMAT_DATES)): raise pyCKWValidationError('start_date is not valid. Use {}'.format(FORMAT_DATES))
        self.debug('Interval values start_date:\'{}\' and end_date:\'{}\' are valid.'.format(start_date.strftime(FORMAT_DATES), end_date.strftime(FORMAT_DATES)))

        response = requests.get(
            url = self.full_path + '/' + start_date.strftime('%Y%m%d') + '/' + end_date.strftime('%Y%m%d') + RESOLUTIONS.get(resolution)
        )
        response.raise_for_status()

        # We get in return a list of dict object parsed from the json response.
        # We will keep only the keys we need and translate them into english.
        consumption_data = []
        for consumption in response.json():
            consumption_data_point = {}
            for data_point in DATA_TRANSLATIONS:
                consumption_data_point[DATA_TRANSLATIONS[data_point]] = consumption[data_point]
            consumption_data.append(consumption_data_point)
        return(consumption_data)

    @property
    def config(self):
        """ Return loaded config """
        return self._config

    @property
    def full_path(self):
        """ The full path to the configured API """
        return self.config.host + self.config.smartmeter_path + '/' + self.config.client_number + '/' + self.config.meter_point

    def available_resolutions():
        """ Returns valid resolutions """
        return list(RESOLUTIONS.keys())

    def valid_format_dates():
        """ Returns valid date format"""
        return FORMAT_DATES

    def warning(self, msg):
        """ WARNING logging level"""    
        logger.warning(msg)

    def info(self, msg):
        """ INFO logging level"""
        logger.info(msg)

    def debug(self, msg):
        """ DEBUG logging level"""
        logger.debug(msg)

    def name_version():
        return WRAPPER_NAME + ' ' + __version__

    @property
    def effective_level(self):
        """ Return the effective logging level """
        return logger.getEffectiveLevel()
