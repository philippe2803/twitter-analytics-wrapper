import os
from datetime import datetime, date as date_, timedelta
from math import ceil
from dateutil import relativedelta
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from twitter_analytics.utils import random_time_sleep, random_small_time_sleep


class ReportDownloader(object):

    """ Twitter Analytics report downloader using Selenium browser interaction """

    def __init__(self, username, password, from_date=None, to_date=None, download_folder=os.getcwd(), proxy=None,
                 show_browser=False):
        """
        Create a browser instance and a fake display. Set up specific preferences for download folder.
        First interaction sent out as visiting the twitter profile of the username given.

        :param username: Twitter username
        :param password: Twitter password
        :param proxy: Proxy in the following string form => IP:PORT or HOST:PORT ("xx.xx.xx.xx:xxxx")
        :param date_from (optional): date from for specific date range report (default is None => last 28 days)
        :param date_to (optional): date to for specific date range report (default is None => last 28 days)
        :param download_folder (optional): where the downloaded report must be downloaded to. Default is working
        directory.
        :param show_browser: Show browser if True (for debugging). Default is False.
        Dates are optional. Without dates, by default it will pull the last 28 days. The range must be maximum 91 days.
        (twitter restriction). The date string for those attributes must follow format 'mm/dd/yyyy'.

        If one is missing, it will only run a last 28 days report instead. BOTH MUST BE INDICATED.
        """

        self.username = username.lower()
        self.password = password

        # Start creating fake display if not show_browser
        self.show_browser = show_browser
        if not self.show_browser:
            self.display = Display(visible=0, size=(1200, 1000))
            self.display.start()

        # Chromedriver settings
        # self.download_folder = os.path.dirname(__file__) + '/data/'
        self.download_folder = download_folder
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.download_folder}
        chrome_options.add_experimental_option("prefs", prefs)

        if proxy is not None:
            chrome_options.add_argument('--proxy-server={}'.format(proxy))

        # Some settings if running for a specific date range
        if from_date is not None and to_date is not None:
            self.has_date_range = True
            self.from_date = from_date
            self.to_date = to_date
        else:
            self.has_date_range = False

        # Create Chrome Browser
        self.browser = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)

        # Login on Twitter
        self.browser.get("http://twitter.com/{}".format(self.username))

    def run(self):
        """
        Main method that will do every interactions necessary to download the report, including picking dates in the
        calendar section.
        :return: Pathname of the report.
        """
        self.login()
        self.go_to_analytics()
        self.go_to_report_page()

        # Pick date range if needed
        if self.has_date_range:
            ranges = self.split_date_range_into_91()
            for rng in ranges:
                date_range = AnalyticsCalendar(
                    from_date=rng[0],
                    to_date=rng[1],
                    browser=self.browser
                )
                date_range.set()
                self.download_report()
        else:
            self.download_report()      # default period download (28 days).

        random_time_sleep()     # to be sure report is fully downloaded
        self.quit()
        reports_downloaded = [self.download_folder + report for report in os.listdir(self.download_folder)]
        return reports_downloaded

    def login(self):
        """
        Login to twitter.
        """
        # Hover over the navigation
        element_to_hover_over = self.browser.find_element_by_xpath('//a[@href="/login"]')
        hover = ActionChains(self.browser).move_to_element(element_to_hover_over)
        hover.perform()
        random_time_sleep()

        # Fills with credentials and click 'Log in'
        self.browser.find_element_by_xpath(
            '//div[@class="LoginForm-input LoginForm-username"]/input[@type="text"]').send_keys(self.username)
        self.browser.find_element_by_xpath(
            '//div[@class="LoginForm-input LoginForm-password"]/input[@type="password"]').send_keys(self.password)
        self.browser.find_element_by_xpath('//input[@value="Log in"]').click()

        random_time_sleep()

    def go_to_analytics(self):
        """
        Goes to the Analytics section
        """
        random_time_sleep()

        # Hover over the navigation (no need to click somehow)
        element_to_hover_over = self.browser.find_element_by_xpath(
            '//li[@class="me dropdown session js-session"]/a[@href="/settings/account"]'
        )
        hover = ActionChains(self.browser).move_to_element(element_to_hover_over)
        hover.perform()
        element_to_hover_over.click()

        random_time_sleep()

        # dropdown-menu
        self.browser.find_element_by_xpath(
            '//li[@role="presentation"]/a[@href="https://analytics.twitter.com/"]').click()
        random_time_sleep()

    def go_to_report_page(self):
        """
        Goes to the analytics page where we can download the report.
        """
        self.browser.get('https://analytics.twitter.com/user/{}/tweets'.format(self.username))
        random_time_sleep()

    def download_report(self):
        """
        Click on the button to launch download. Check number of files in download folder first, and then check if
        number changes to detect when the report is downloaded.
        Check routinely if the download bug occurred, and re-click the download button if it is the case.

        """
        len_download_folder = len(os.listdir(self.download_folder))
        download_button = self.browser.find_element_by_xpath(
            '//div[@id="export"]/button[@class="btn btn-default ladda-button"]'
        )
        download_button.click()

        while len(os.listdir(self.download_folder)) == len_download_folder:
            if self.report_error_occurred():
                download_button.click()

            random_time_sleep()

    def report_error_occurred(self):
        """
        Method to monitor if the twitter analytics bug (see browser screenshot 'twitter_bug_screenshot.png') occurred.
        :return: Boolean: True if bug occurred, False if it did not.
        # error server Callout Callout--danger
        """
        try:
            self.browser.find_element_by_xpath('//div[@class="error server Callout Callout--danger"]')
        except NoSuchElementException:
            return False
        return True

    def split_date_range_into_91(self):
        """
        Split the date range into 91 days segment to batch the scraping of the calendar for period longer than 91 days.
        :return: List of list of 2 items [0] = from and [1] = to.
        """
        from_date = datetime.strptime(self.from_date, '%m/%d/%Y')
        to_date = datetime.strptime(self.to_date, '%m/%d/%Y')
        delta = to_date - from_date
        number_of_batch = ceil(delta.days / 90)

        batches = list()
        start_date = from_date
        for batch in range(0, number_of_batch):
            end_date = start_date + timedelta(days=90)
            batches.append([start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')])
            start_date = end_date + timedelta(days=1)
        return batches

    def quit(self):
        random_time_sleep()
        self.browser.quit()
        if not self.show_browser:
            self.display.stop()


class AnalyticsCalendar(object):

    def __init__(self, browser, from_date, to_date):
        """
        Class that handles the selection of FROM date and TO date in the calendar of twitter analytics.

        :param browser: Selenium driver object
        :param from_date: date string in the format 'mm/dd/yyyy'
        :param to_date: date string in the format 'mm/dd/yyyy'
        """
        self.from_date = from_date
        self.to_date = to_date
        self.browser = browser

    def set(self):
        self.open_calendar()
        self.pick_from_date()
        self.pick_to_date()
        self.click_update_date_button()

    def open_calendar(self):
        calendar_xpath = '//div[@class="btn daterange-button"]'
        self.browser.find_element_by_xpath(calendar_xpath).click()
        random_time_sleep()

    def pick_from_date(self):
        """
        Update the FROM date in analytics calendar.
        """
        from_calendar_element = 'div[@class="calendar left"]'
        date_picker = DatePicker(self.browser, from_calendar_element, self.from_date)
        date_picker.select_date()
        random_time_sleep()

    def pick_to_date(self):
        """
        Update the TO date in analytics calendar.
        """
        to_calendar_element = 'div[@class="calendar right"]'
        date_picker = DatePicker(self.browser, to_calendar_element, self.to_date)
        date_picker.select_date()
        random_time_sleep()

    def click_update_date_button(self):
        """
        Click the 'update' button after a date range is selected.
        """
        update_button = '//button[@class="applyBtn btn btn-sm btn-primary"]'
        self.browser.find_element_by_xpath(update_button).click()
        random_time_sleep()


class DatePicker(object):

    """
    Given a date, and a calendar element, this class handles specifically picking the right date within the
    calendar element given as an attribute
    """

    def __init__(self, browser, xpath_calendar, target_date):
        """
        :param browser: Selenium driver/browser
        :param element: Xpath Selenium element calendar where we need to pick a date from.
        :param date: Date string in the format 'mm/dd/yyyy'
        """
        self.browser = browser
        self.xpath_calendar = xpath_calendar
        self.target_date = target_date

        # date parsing
        self.month, self.day, self.year = self.target_date.split('/')
        self.today = date_.today()

    def select_date(self):
        """
        Main method for selecting a date in the given element calendar attribute.
        """
        months_delta = self.find_months_delta()
        self.pick_month(months_delta)
        self.pick_day()

    def find_months_delta(self):
        """
        Method which compares the displayed month in calendar with targeted month to define the delta in months (=number
        of clicks in prev or next month button within calendar).

        The result delta can be negative (to trigger click to 'previous' month button) or positive ( to trigger click
        to 'next' month button).
        """
        month_xpath = '//{}/div[@class="calendar-date"]/table[@class="table-condensed"]/' \
                      'thead/tr/th[@class="month"]'.format(self.xpath_calendar)

        display_month = datetime.strptime(self.browser.find_element_by_xpath(month_xpath).text, '%b %Y')
        target_month = datetime.strptime('{} {}'.format(self.month, self.year), '%m %Y')
        r = relativedelta.relativedelta(target_month, display_month)

        months_delta = r.years * 12 + r.months
        return months_delta

    def pick_month(self, months_delta):
        """
        Method which will clicks the right button (previous or next) to reach the calendar month targeted.
        :param months_delta: Number of month between the default month displayed in calendar and the targeted month.
        """
        if months_delta > 0:
            for i in range(0, months_delta):
                self.click_next()
                random_small_time_sleep()
        elif months_delta < 0:
            for i in range(0, abs(months_delta)):
                self.click_previous()
                random_small_time_sleep()

    def click_previous(self):
        """
        Previous month button click on a calendar section
        """
        prev_button_xpath = '//{}/div[@class="calendar-date"]/table[@class="table-condensed"]/' \
                            'thead/tr/th[@class="prev available"]/span[@class="Icon Icon--caretLeft Icon--tiny"]'\
            .format(self.xpath_calendar)
        self.browser.find_element_by_xpath(prev_button_xpath).click()

    def click_next(self):
        """
        Next month button click on a calendar section
        """
        next_button_xpath = '//{}/div[@class="calendar-date"]/table[@class="table-condensed"]/' \
                            'thead/tr/th[@class="next available"]/span[@class="Icon Icon--caretRight Icon--tiny"]' \
            .format(self.xpath_calendar)
        self.browser.find_element_by_xpath(next_button_xpath).click()

    def pick_day(self):
        """
        Method that press the right day in the previously selected month.
        """
        day_xpath = '//{}/div[@class="calendar-date"]/table[@class="table-condensed"]/' \
                    'tbody/tr/td[(@class="available" or @class="available in-range" ' \
                    'or @class="available active start-date" or @class="available active end-date") and text()="{}"]'\
            .format(self.xpath_calendar, str(int(self.day)))
        self.browser.find_element_by_xpath(day_xpath).click()
