#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pyCKWConstants.py
    Define constants for the wrapper.
    In case some values need to be added/removed/updated, this is a central point to perform changes.

    Author: Jeremy Diaz
    Year:   2022
"""

# Constants for Data resolutions and their respective paths
RESOLUTIONS = {
    'year' : '/year',
    'month' : '/month',
    'week' : '/week',
    'day' : '/day',
    'hour' : '/hour',
    'minute' : '/minute'
}

# Translation for datapoint items in English
# Also we define here the datapoint items we're only interested in.
# Not included as of today are:
#   anzahl_linien_fb
#   anzahl_linien_fw
#   anzahl_linien_p

DATA_TRANSLATIONS = {
    'betrag_ht': 'qty_peak',
    'betrag_nt': 'qty_offpeak',
    'betrag_blind_ht': 'qty_reactive_peak',
    'betrag_blind_nt': 'qty_reactive_offpeak',
    'menge_fakturiert_ht': 'qty_invoiced_peak',
    'menge_fakturiert_nt': 'qty_invoiced_offpeak',
    'menge_fakturiert_blind_ht': 'qty_reactive_invoiced_peak',
    'menge_fakturiert_blind_nt': 'qty_reactive_invoiced_offpeak',
    'menge_physikalisch': 'qty_measured', 
    'max_leistung_faktura': 'max_power',
    'max_leistung_physisch': 'max_physical_power',
    'zeitstempel_bis_utc': 'end_date',
    'zeitstempel_von_utc': 'start_date',
}

# The date format as accepted by the myCKW API
FORMAT_DATES = '%Y%m%d'

## User-configurable defaults via configurable values
# Connection Defaults
DEFAULT_HOST = "https://etility.ckw.ch"
DEFAULT_SMARTMETER_PATH = "/etility/proxy/ckw/serviceDA"

# The token type to be included in API calls
TOKEN_TYPE = "Bearer"
