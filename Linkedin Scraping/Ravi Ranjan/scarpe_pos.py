from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import ast
import requests
import shutil
import pandas as pd
import numpy as np
import ssl
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997'):

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.error = False
        self.main_url = 'https://cowork.91springboard.com/login'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.text= []
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['text']= self.text
        elem = pd.DataFrame(mydict)
        elem.to_csv('stat_posts.csv', index=False)


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/in/ravi-ranjan-prasad-karn/detail/recent-activity/shares/'
        print("Scraping: ", link)
        self.driver.get(link)
        sleep(20)
        self.get_data()
        sleep(5)

    def get_data(self):
        try:
            for value in range(15):
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(3)
        except Exception as e:
            self.error = True
            print(e)
            print('Some error occurred while trying to scroll down')
        sleep(5)
        try:
            see_more = self.driver.find_elements_by_xpath('//button[@class="feed-shared-inline-show-more-text__see-more-less-toggle see-more t-14 t-black--light t-normal hoverable-link-text"]')
            for s in see_more:
                s.click()
                sleep(1)
            sleep(5)
        except Exception:
            pass

        try:
            text = self.driver.find_elements_by_xpath('//div[@class="feed-shared-text__text-view feed-shared-text-view white-space-pre-wrap break-words ember-view"]')
            text= [t.get_attribute('innerHTML')  for t in text]
            self.text= text
            sleep(5)
        except Exception:
            pass


    def log_in(self, ):
        try:
            user_name_input = self.driver.find_element_by_xpath('//form//input[@placeholder= "Email"]')
            user_name_input.send_keys(self.username)
            password_input = self.driver.find_element_by_xpath('//form//input[@placeholder= "Password"]')
            password_input.send_keys(self.password)
            user_name_input.submit()
        except Exception:
            print('Some exception occurred while trying to find username or password field')
            self.error = True




if __name__ == '__main__':
    app = App()
