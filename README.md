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


A simple download for the last 28 days is done as follow:


```python
from twitter_analytics import ReportDownloader


reports = ReportDownloader(
    username='<twitter username>',
    password='<twitter password>',
)

reports.run()

```

If you encounter issues, submit it on this repo.
