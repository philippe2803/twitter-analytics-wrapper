import os
import platform
SYST = platform.system().lower()
from datetime import datetime, timedelta
from math import ceil
from twitter_analytics.calendar import AnalyticsCalendar
if SYST != 'windows':
    from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from twitter_analytics.utils import random_time_sleep


class ReportDownloader(object):

    """ Twitter Analytics report downloader using Selenium browser interaction """

    def __init__(self, username, password, from_date=None, to_date=None, download_folder=os.getcwd(), proxy=None,
                 show_browser=False, section='tweets'):
        """
        Create a browser instance and a fake display. Set up specific preferences for download folder.
        First interaction sent out as visiting the twitter profile of the username given.

        :param username: Twitter username
        :param password: Twitter password
        :param proxy: Proxy in the following string form => IP:PORT or HOST:PORT ("xx.xx.xx.xx:xxxx")
        :param date_from (optional): date from for specific date range report (default is None => last 28 days). Must be
        in the following string format 'mm/dd/yyyy'

        :param date_to (optional): date to for specific date range report (default is None => last 28 days). Must be
        in the following string format 'mm/dd/yyyy'.

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
        if not self.show_browser and SYST != 'windows':
            self.display = Display(visible=0, size=(1200, 1000))
            self.display.start()

        self.section = section

        # Chromedriver settings
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
        if SYST == 'darwin':
            self.browser = webdriver.Chrome(r"/usr/local/bin/chromedriver", chrome_options=chrome_options)
        elif SYST == 'linux':
            self.browser = webdriver.Chrome(r"/usr/lib/chromium-browser/chromedriver",chrome_options=chrome_options)
        else:
            windriver = os.environ.get('chromedriver') # get environment variable
            if 'chromedriver.exe' in os.listdir() or windriver == None:
                 self.browser = webdriver.Chrome(chrome_options=chrome_options)
            else:
                self.browser = webdriver.Chrome(windriver,chrome_options=chrome_options)

        # Login on Twitter
        # self.browser.get("http://twitter.com/{}".format(self.username))
        twitter_url = "https://twitter.com/login?redirect_after_login=https%3A%2F%2Fanalytics.twitter.com%2Fabout&hide_message=1"
        self.browser.get(twitter_url)

    def run(self):
        """
        Main method that will do every interactions necessary to download the report, including picking dates in the
        calendar section.
        :return: Pathname of the report.
        """
        self.login()
        self.go_to_analytics()

        if self.section == 'tweets':
            self.go_to_report_page()
        elif self.section == 'videos':
            self.go_to_video_page()
        else:
            raise Exception('Unknown section')

        # Pick date range if needed
        if self.has_date_range:
            ranges = self.split_date_range_into_91(from_date=self.from_date, to_date=self.to_date)
            for rng in ranges:
                date_range = AnalyticsCalendar(
                    from_date=rng[0],
                    to_date=rng[1],
                    browser=self.browser
                )
                date_range.set_report_period()
                self.download_report()
        else:
            self.download_report()      # default period download (28 days).

        random_time_sleep()     # to be sure report is fully downloaded
        self.quit()
        reports_downloaded = [os.path.join(self.download_folder,'') + report for report in os.listdir(self.download_folder)
                              if '.csv' in report]
        return reports_downloaded

    def login(self):
        """
        Login to twitter.
        """
        # # Hover over the navigation
        # element_to_hover_over = self.browser.find_element_by_xpath('//a[@href="/login"]')
        # hover = ActionChains(self.browser).move_to_element(element_to_hover_over)
        # hover.perform()
        random_time_sleep()

        # Fills with credentials and click 'Log in'
        self.browser.find_element_by_xpath(
            '//input[@class="js-username-field email-input js-initial-focus"]').send_keys(self.username)
        self.browser.find_element_by_xpath('//input[@class="js-password-field"]').send_keys(self.password)
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()

        random_time_sleep()

        # NOT NEEDED ANY MORE
        # =======================================================
        # self.browser.find_element_by_xpath(
        #     '//div[@class="LoginForm-input LoginForm-username"]/input[@type="text"]').send_keys(self.username)
        # self.browser.find_element_by_xpath(
        #     '//div[@class="LoginForm-input LoginForm-password"]/input[@type="password"]').send_keys(self.password)
        # self.browser.find_element_by_xpath('//input[@value="Log in"]').click()
        # =======================================================

    def go_to_analytics(self):
        """
        Goes to the Analytics section
        """
        random_time_sleep()

        # Going directly to the analytics page
        self.browser.get("https://analytics.twitter.com/")

        # THE FOLLOWING CODE IS NO LONGER NEEDED
        # AS TWITTER HAS CHANGED THEIR PAGE LAYOUT
        # =======================================================
        # Hover over the navigation (no need to click somehow)
        # element_to_hover_over = self.browser.find_element_by_xpath(
        #     '//li[@class="me dropdown session js-session"]/a[@href="/settings/account"]'
        # )
        # hover = ActionChains(self.browser).move_to_element(element_to_hover_over)
        # hover.perform()
        # element_to_hover_over.click()
        #
        # random_time_sleep()
        #
        # # dropdown-menu
        # self.browser.find_element_by_xpath(
        #     '//li[@role="presentation"]/a[@href="https://analytics.twitter.com/"]').click()
        # =======================================================

        random_time_sleep()

    def go_to_report_page(self):
        """
        Goes to the analytics page where we can download the report.
        """
        self.browser.get('https://analytics.twitter.com/user/{}/tweets'.format(self.username))
        random_time_sleep()

    def go_to_video_page(self):
        """
        Goes to the page with video statistics
        """
        self.browser.get('https://analytics.twitter.com/user/{}/videos'.format(self.username))
        random_time_sleep()

    def download_report(self):
        """
        Click on the button to launch download. Check number of files in download folder first, and then check if
        number changes to detect when the report is downloaded.
        Check routinely if the download bug occurred, and re-click the download button if it is the case.

        """
        random_time_sleep()
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

    @staticmethod
    def split_date_range_into_91(from_date, to_date):
        """
        Split the date range into 91 days segment to batch the scraping of the calendar for period longer than 91 days.
        :return: List of list of 2 items [0] = from and [1] = to.
        """
        from_date = datetime.strptime(from_date, '%m/%d/%Y')
        to_date = datetime.strptime(to_date, '%m/%d/%Y')
        delta = to_date - from_date
        number_of_batch = ceil(float(delta.days) / 90)

        batches = list()
        start_date = from_date
        for batch in range(0, int(number_of_batch)):
            end_date = start_date + timedelta(days=90)
            batches.append([start_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')])
            start_date = end_date + timedelta(days=1)
        return batches

    def quit(self):
        random_time_sleep()
        self.browser.quit()

        if not self.show_browser and SYST != 'windows':
            self.display.stop()
