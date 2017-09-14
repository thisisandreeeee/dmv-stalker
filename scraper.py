from selenium import webdriver
from settings import PROFILE, URL
from logger import Logger
import time

class Scraper:
    def __init__(self):
        self.logger = Logger()
        self.logger.log("New instance of scraper created")
        browser = webdriver.PhantomJS('phantomjs')
        # browser = webdriver.Chrome('./chromedriver')
        browser.get(URL)
        self.browser = browser
        self.logger.log("Navigated to url")
        time.sleep(5)

    def i_want_an_appointment_at(self, office_id):
        self.logger.log("Start appointment searching process")
        browser = self.form_fill_and_submit(self.browser, office_id)
        browser.switch_to_default_content()
        appt = self.get_appointment(browser)
        if appt and appt[:5] == 'Sorry':
            return None
        return appt

    def form_fill_and_submit(self, browser, office_id):
        browser.find_element_by_xpath('//*[@id="officeId"]/option[{}]'.format(office_id)).click()
        browser.find_element_by_xpath('//*[@id="DT"]').click()
        browser.find_element_by_xpath('//*[@id="first_name"]').send_keys(PROFILE['first_name'])
        browser.find_element_by_xpath('//*[@id="last_name"]').send_keys(PROFILE['last_name'])
        browser.find_element_by_xpath('//*[@id="b_day"]').send_keys(PROFILE['mm'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[8]/div/div/span/input[2]').send_keys(PROFILE['dd'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[8]/div/div/span/input[3]').send_keys(PROFILE['yyyy'])
        browser.find_element_by_xpath('//*[@id="dl_number"]').send_keys(PROFILE['dl_number'])
        browser.find_element_by_xpath('//*[@id="phone_no"]').send_keys(PROFILE['tel_prefix'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[9]/div/span/input[2]').send_keys(PROFILE['tel_suffix1'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[9]/div/span/input[3]').send_keys(PROFILE['tel_suffix2'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/div[10]/input[2]').click()
        self.logger.log("Form filled and submitted for office %s" % office_id)
        return browser

    def get_appointment(self, browser):
        time.sleep(5)
        try:
            element = browser.find_element_by_xpath('//*[@id="app_content"]/div[1]/div[2]/table/tbody/tr/td[2]/p[2]/strong').get_attribute('innerHTML')
            self.logger.log("Valid appointment xpath found")
            return element
        except:
            self.logger.log("No valid appointment xpath found")
            pass
        try:
            element = browser.find_element_by_xpath('//*[@id="app_content"]/table/tbody/tr[2]/td/p').get_attribute('innerHTML')
            self.logger.log("No available appointments")
            return element
        except:
            self.logger.log("Invalid xpath - no element found")
            pass
        return None
