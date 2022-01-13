#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" pyCKWCLI.py
    CLI Application companion for the pyCKW wrapper.
    It can also be used as an example on how to use the wrapper.

    Author: Jeremy Diaz
    Year:   2022
"""

# Python Standard Library general imports
import time
start_time = time.time()
import logging
import argparse
import pprint

# Python Standard Library specific imports
from datetime import datetime, timedelta

# pyCKW import
from pyckw import pyCKW

def validate_absolute_date(dt):
    """
        Validate the absolute date against a a predefined datetime format.
        It should also create the datetime.datetine object properly directly when specified via cli switches.
    """
    dt_format = pyCKW.valid_format_dates()
    try:
        return datetime.strptime(dt, dt_format)
    except ValueError:
        raise ValueError("Incorrect data format, should be {}.".format(dt_format))

def parse_arguments():
    parser = argparse.ArgumentParser(description='Fetches consumption Data from myCKW. and pretty-prints it.')
    
    # Optional Arguments
    parser.add_argument(
        '-v',
        '--log-verbosity',
        choices=list(logging._levelToName.values()),
        default=logging.WARNING,
        help='Set log verbosity. Default is {}.'.format(logging._levelToName[logging.WARNING]),
        action='store')
    parser.add_argument(
        '-V',
        '--version',
        help='Print version and exit.',
        action='version',
        version=__file__ + ' with ' + pyCKW.name_version())

    # Required Arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-c',
        '--client-number',
        help='The client number. Example 0001234567.',
        action='store',
        required=True)
    required.add_argument(
        '-m',
        '--meter-point',
        help='A 33-chars long string representing the Meter ID. Example CH0009801234500000000000000054321',
        action='store',
        required=True)
    required.add_argument(
        '-r',
        '--resolution',
        help='Data resolution.',
        choices = pyCKW.available_resolutions(),
        action='store',
        required=True)
    required.add_argument(
        '-i',
        '--relative-interval',
        help='An interval expressed in days, relative to now.',
        type=int,
        action='store'
        )
    required.add_argument(
        '--start-date',
        help='Start date for interval',
        type=validate_absolute_date,
        action='store'
        )
    required.add_argument(
        '--end-date',
        help='End date for interval.',
        type=validate_absolute_date,
        action='store'
        )
    args = parser.parse_args()

    ## -i/--interval and (--start-date + --end-date) are mutually exclusive parameters. Due to current limitation in 
    ## mutally-exclusive parameters and groups handling we must implement our own check logic.
    ## We enforce two checks:
    ##    - interval and start/end dates cannot be used together
    ##    - start/end dates are mandatory if interval is not specified.
    # -i/--interval and --start-date --end-date cannot be used together.
    if (args.relative_interval and args.start_date) or (args.relative_interval and args.end_date):
        parser.error('-i/--interval and --start-date --end-date cannot be used together.')
    # --start-date --end-date are required if -i/--interval is not specified
    if (not args.relative_interval and not (args.start_date and args.end_date)):
        parser.error('--start-date --end-date are mandatory if -i/--interval is not speficied.')
    return args

if __name__ == "__main__":
    try:
        arguments = parse_arguments()

        logging.basicConfig(
            level=arguments.log_verbosity,
            format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s',
            datefmt="%Y-%m-%dT%H:%M:%S%z"
        )

        # We have to manage an interval
        if arguments.relative_interval:
            end_date = datetime.now()
            start_date = end_date - timedelta(days = arguments.relative_interval)
        if arguments.start_date and arguments.end_date:
            start_date = arguments.start_date
            end_date = arguments.end_date

        # Instantiate a pyCKW object 
        ckw = pyCKW(
            client_number=arguments.client_number,
            meter_point=arguments.meter_point
        )

        # Get the consumption data
        my_consumption = ckw.get_consumption(
            arguments.resolution,
            start_date,
            end_date
        ) 

        # Pretty-Print the results
        pp = pprint.PrettyPrinter(indent=4, depth=6)
        pp.pprint(my_consumption)
        print('Fetched {} data points in {} seconds.'.format(len(my_consumption), round(time.time() - start_time, 2)))

    finally:
        pass