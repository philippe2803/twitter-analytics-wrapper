from datetime import datetime, date as date_
from dateutil import relativedelta
from twitter_analytics.utils import random_time_sleep, random_small_time_sleep


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

    def set_report_period(self):
        self.open_calendar()
        self.pick_from_date()
        self.pick_to_date()
        self.click_update_date_button()
        self.open_calendar()
        self.click_update_date_button()
        return 'completed'      # used for unit test

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
        Method which will clicks the right button (previous or next) to reach the calenda
r month targeted.
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
