# pyCKW
Access your myCKW smartmeter data.

> ⚠️ **Warning:** This project is in its current form not working anymore as CKW migrated to a new portal and API in Azure. A new version will be released soon.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Companion CLI Application](#companion)
- [Notes](#notes)
- [Todo's](#todos)
- [Disclaimer](#disclaimer)
- [Credits](#credits)

<a name="introduction"></a>

## Introduction

If you have a new Smart Meter installed by CKW you can pull fresh consumption and power data from it through their API.  
This package is a wrapper to ease the retrieval of this data.  
I wrote this package to inegrate my electricity usage data into my home automation tools.

<a name="requirements"></a>

## Requirements

  - Be a customer at CKW
  - Have a Smart Meter already installed. See [Zählerwechsel](https://www.ckw.ch/lp/zaehlerwechsel.html).
  - Know your customer number and meter ID. These information can be found on your last invoice:
    - Customer Number = "Kunden-Nr.", a 7-digits ID.
    - Meter ID = "Zählpunkt", a 33-digits ID.


<a name="installation"></a>

## Installation

### PIP

The simplest way is to use pip.

```bash
pip install pyCKW
```

### Manual Installation

If for some reason you prefer to manually install the package you can download a fresh copy of the code with git clone.

```bash
git clone https://github.com/diaznet/pyCKW.git
```

There is also the possibility to download the releases from Github. See [Releases page](https://github.com/diaznet/pyCKW/releases).

<a name="usage"></a>

## Usage

You create an object from class `pyCKW` and use the supported methods to fetch structured data from the API.

| Method | Description |
| - | - |
| `get_consumption(resolution = str, start_date=datetime.datetime, end_date=datetime.datetime) | Returns a list of dictionaries with currently supported consumption data |


```python
# Import datetime.datetime
from datetime import datetime

# pyCKW import
from pyckw import pyCKW

# We want to retrieved data with a resolution of a day between the 11th and 12th of January 2022
resolution = 'day'
start_date = datetime.strptime('20211211', '%Y%m%d')
end_date = datetime.strptime('20211212', '%Y%m%d')

# Instantiate a pyCKW object 
ckw = pyCKW(
    client_number='0001234567',
    meter_point='CH0009801234500000000000000054321',
    token='bmljZV90cnk='
)

# Get the consumption data
consumption_data = ckw.get_consumption(
    resolution,
    start_date,
    end_date
)
```

Example data object returned from the code snippet above:

```json
[
    {   
        "end_date": "Tue, 11 Jan 2022 23:00:00 GMT",
        "max_physical_power": 2.5360000133514404,
        "max_power": 2.5360000133514404,
        "qty_invoiced_offpeak": 5.169999994337559,
        "qty_invoiced_peak": 11.194000013172626,
        "qty_measured": 16.364000007510185,
        "qty_reactive_invoiced_offpeak": null,
        "qty_reactive_invoiced_peak": null,
        "qty_reactive_offpeak": null,
        "qty_reactive_peak": null,
        "start_date": "Mon, 10 Jan 2022 23:00:00 GMT"
    },
    {   
        "end_date": "Wed, 12 Jan 2022 23:00:00 GMT",
        "max_physical_power": 11.64799976348877,
        "max_power": 11.64799976348877,
        "qty_invoiced_offpeak": 9.262999959290028,
        "qty_invoiced_peak": 12.256000146269798,
        "qty_measured": 21.519000105559826,
        "qty_reactive_invoiced_offpeak": null,
        "qty_reactive_invoiced_peak": null,
        "qty_reactive_offpeak": null,
        "qty_reactive_peak": null,
        "start_date": "Tue, 11 Jan 2022 23:00:00 GMT"
    }
]
```

`start_date` and `end_date` are `datetime.datetime` object and are used to determine the day/month/year only, as the API doesn't allow more precise spans.  
Therefore it is not necessary to specify the hour/minutes/seconds when creating the datetime.datetime object, at it will always resolve to 00:00:00 CET or CEST.  
Data times are local to Europe/Zuricn

<a name="companion"></a>

## Companion CLI application

A CLI application is provided to demonstrate how to use the library.  
It can also be used to fetch the data by yourself if you do not want to rewrite the wheel.

### CLI Application usage

```bash
[user@host ~]$ python pyCKWCLI.py -h
usage: pyCKWCLI.py [-h] [-v {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}] [-V] -c CLIENT_NUMBER
                   -m METER_POINT -r {year,month,week,day,hour,minute} [-i RELATIVE_INTERVAL]
                   [--start-date START_DATE] [--end-date END_DATE]

Fetches consumption Data from myCKW and pretty-prints it.

optional arguments:
  -h, --help            show this help message and exit
  -v {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}, --log-verbosity {CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET}
                        Set log verbosity. Default is WARNING.
  -V, --version         Print version and exit.

required arguments:
  -c CLIENT_NUMBER, --client-number CLIENT_NUMBER
                        The client number. Example 0001234567.
  -m METER_POINT, --meter-point METER_POINT
                        A 33-chars long string representing the Meter ID.
                        Example CH0009801234500000000000000054321
  -r {year,month,week,day,hour,minute}, --resolution {year,month,week,day,hour,minute}
                        Data resolution.
  -i RELATIVE_INTERVAL, --relative-interval RELATIVE_INTERVAL
                        An interval expressed in days, relative to now.
  --start-date START_DATE
                        Start date for interval
  --end-date END_DATE   End date for interval.

[user@host ~]$ 
```

### API Token

The CLI companion app expects to find an environnement variable named `MYCKW_API_TOKEN`. Set this environnement variable with your API token.
See note below.

### Example

```bash
[user@host ~]$ python pyCKWCLI.py                       \
                -c 0001234567                           \
                -m CH0009801234500000000000000054321    \
                -r day                                  \
                --start-date 20241113                   \
                --end-date 20241114
[
    {
        "qty_peak": 1.8070140036493543,
        "qty_offpeak": 4.028123970359564,
        "qty_reactive_peak": null,
        "qty_reactive_offpeak": null,
        "qty_invoiced_peak": 7.467000015079975,
        "qty_invoiced_offpeak": 19.553999856114388,
        "qty_reactive_invoiced_peak": null,
        "qty_reactive_invoiced_offpeak": null,
        "qty_measured": 27.020999871194363,
        "max_power": 12.076000213623047,
        "max_physical_power": 12.076000213623047,
        "end_date": "2024-11-14T23:00:00",
        "start_date": "2024-11-13T23:00:00"
    },
    {
        "qty_peak": 2.583592028617859,
        "qty_offpeak": 1.0736720056235791,
        "qty_reactive_peak": null,
        "qty_reactive_offpeak": null,
        "qty_invoiced_peak": 10.676000118255615,
        "qty_invoiced_offpeak": 5.212000027298927,
        "qty_reactive_invoiced_peak": null,
        "qty_reactive_invoiced_offpeak": null,
        "qty_measured": 15.888000145554543,
        "max_power": 2.01200008392334,
        "max_physical_power": 2.01200008392334,
        "end_date": "2024-11-13T23:00:00",
        "start_date": "2024-11-12T23:00:00"
    }
]
Fetched 2 data points in 3.56 seconds.
[user@host ~]$
```

<a name="notes"></a>

## Notes

### Delays
There seems to be still at the time of writing (April 2025) a delay of 7 hours between the measures from your smart meter and the actual time they are returned by the API.
Hopefully the utility provider improves this gap soon!

### API Token
Since 2023 the utility provider has implemented authentication via JWT / Bearer token. This is a good move as this allows your data to remain private.
Version 0.3 of the library now supports token specified via class instantiation, see [Usage](#usage).

CLI Companion app supports it currently only via environment variable.
To get this token, go to [MyCKW Consumption] page, Developer Tools with your browser , Network tab and check for a 'day' request. In the Headers tab, in Requests headers, look for 'Authorization'. The string after "Bearer" is your token. Note that the token is valid for 5 minutes.


<a name="todos"></a>

## Todo's
  - Finish documentation
  - Improve logging in various places
  - Handle OAUTH in CLI companion app

<a name="disclaimer"></a>

## Disclaimer

This application comes without warranty.
Please use with care. Any damage cannot be related back to the author.
I am not affiliated in any way to CKW and its subsidiaries.

<a name="credits"></a>

## Credits
Author: Jeremy Diaz  
