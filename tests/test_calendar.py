from twitter_analytics.calendar import AnalyticsCalendar
from twitter_analytics import ReportDownloader
from selenium import webdriver
from pyvirtualdisplay import Display
import os


def NOtest_calendar_date_picking():
    # Creating driver and virtual display
    display = Display(visible=0, size=(1200, 1000))
    display.start()
    browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")

    # Actual test
    fixture_page = os.path.join(os.path.dirname(__file__), 'fixtures/report_page_dump.html')
    calendar = AnalyticsCalendar(browser=browser, from_date='01/01/2015', to_date='02/28/2015')
    browser.get('file://' + fixture_page)

    # Checking there is no error during the calendar picking
    assert calendar.set_report_period() == 'completed'

    # Stoping driver and display
    browser.quit()
    display.stop()

