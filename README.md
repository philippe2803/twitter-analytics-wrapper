Twitter analytics downloader
========

This script downloads the tweets report from the analytics section of a twitter account (including impressions). 
You can specify dates for period longer than the last 28 days default period from the Twitter analytics interface.

The twitter analytics platform has a limit of 91 days. For period longer than 91 days, it splits the downloading of reports in multiple downloads.

This was created so we can get impressions data for every tweets as there is no API endpoints specifically for those metrics (as of today).


Installation

Selenium uses a few binaries (Chromedriver, xvfb) that needs to be installed beforehand with the following command:

```commandline
$ sudo apt-get install chromium-chromedriver xvfb
```

Then you can install the library with pip


```commandline
$ pip install twitter-analytics

```


A simple download for the last 28 days (default period) is done as follow:

```python
from twitter_analytics import ReportDownloader


reports = ReportDownloader(
    username='<twitter username>',
    password='<twitter password>',
)

report_filepath = reports.run()
```

For specific date range and/or period over 90 days, you can launch the report download as follow:

```python
from twitter_analytics import ReportDownloader
import csv


reports = ReportDownloader(
    username='<twitter username>',
    password='<twitter password>',
    from_date='03/28/2014',         # must be in string format 'mm/dd/yyyy' and nothing before October 2013 (twitter restriction).
    to_date='12/31/2016'
)

reports_filepath = reports.run()            # list of filepaths of downloaded csv reports

# Then you can parse the csv simply as follow
tweets = list()
for report in reports_filepath:
    with open(report, 'r') as csvfile:
        r = csv.DictReader(csvfile)
        rows = [row for row in r]
        tweets += rows

```

If you encounter issues, submit it on this repo. I also accept pull requests.

## Mac OS install prerequisites

- xvfb: Install XQuartz. Download the installer from [here](https://www.xquartz.org).
- Chromedriver: The easiest way to obtain this is via [Homebrew](https://brew.sh):

    ```commandline
    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    
    $ brew install chromedriver
    ```

# If you are installing from this repository:

1. Clone/Download (and unzip) this repo in a known location in your computer

2. Open a terminal and navigate to the location chosen for step 1

3. In the terminal type the following

   ```
   python setup.py install --force
   ```

   ​