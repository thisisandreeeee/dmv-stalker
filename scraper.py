from selenium import webdriver
from settings import PROFILE, URL
import time

class Scraper:
    def __init__(self):
        browser = webdriver.PhantomJS('phantomjs')
        # browser = webdriver.Chrome('./chromedriver')
        browser.get(URL)
        self.browser = browser

    def i_want_an_appointment_at(self, office_id):
        browser = self.form_fill_and_submit(self.browser, office_id)
        browser.switch_to_default_content()
        appt = self.get_appointment(browser)
        if appt[:5] == 'Sorry':
            return None
        return appt

    def form_fill_and_submit(self, browser, office_id):
        browser.find_element_by_xpath('//*[@id="officeId"]/option[{}]'.format(office_id)).click()
        browser.find_element_by_xpath('//*[@id="DT"]').click()
        browser.find_element_by_xpath('//*[@id="first_name"]').send_keys(PROFILE['first_name'])
        browser.find_element_by_xpath('//*[@id="last_name"]').send_keys(PROFILE['last_name'])
        browser.find_element_by_xpath('//*[@id="b_day"]').send_keys(PROFILE['mm'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/table/tbody/tr[14]/td[2]/input[2]').send_keys(PROFILE['dd'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/table/tbody/tr[14]/td[2]/input[3]').send_keys(PROFILE['yyyy'])
        browser.find_element_by_xpath('//*[@id="dl_number"]').send_keys(PROFILE['dl_number'])
        browser.find_element_by_xpath('//*[@id="phone_no"]').send_keys(PROFILE['tel_prefix'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/table/tbody/tr[16]/td[2]/input[2]').send_keys(PROFILE['tel_suffix1'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/fieldset/table/tbody/tr[16]/td[2]/input[3]').send_keys(PROFILE['tel_suffix2'])
        browser.find_element_by_xpath('//*[@id="app_content"]/form/table/tbody/tr/td[1]/input[2]').click()
        return browser

    def get_appointment(self, browser):
        time.sleep(2)
        try:
            element = browser.find_element_by_xpath('//*[@id="app_content"]/table/tbody/tr[3]/td[1]/p').get_attribute('innerHTML')
            return element
        except:
            pass
        try:
            element = browser.find_element_by_xpath('//*[@id="app_content"]/table/tbody/tr[2]/td/p').get_attribute('innerHTML')
        except:
            pass
        return element
