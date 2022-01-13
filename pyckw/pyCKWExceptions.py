#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pyCKWExceptions.py
    Defines custom exception handlers.

    Author: Jeremy Diaz
    Year:   2022
"""

class pyCKWValidationError(Exception):
    """ We need a cusotm Exception handler to manage Input Validation Errors """
    def __init__(self, msg):
        self.msg = msg
