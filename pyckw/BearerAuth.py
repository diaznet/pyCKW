#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" BearerAuth.py
    Class file for handling Bearer authentication

    Author: Jeremy Diaz
    Year:   2024
"""

# Python Standard Library general imports
import requests

# pyCKW contants imports
from pyckw.pyCKWConstants import (
    TOKEN_TYPE
)

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = TOKEN_TYPE + ' ' + self.token
        return r