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
import re
from tqdm import tqdm

class App:
    def __init__(self, username='prudhvi.potuganti@gmail.com', password='2121991@Mithil', target_username='prudhvip'):

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.username = username
        self.password = password
        self.target_username = target_username
        self.driver = webdriver.Firefox()
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.email= []
        self.number= []
        self.df= pd.read_csv('Comments_Data.csv')
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        self.df['email']= self.email
        self.df['Contact_number']= self.number
        self.df.to_csv('Comments_Data_info.csv', index=False)

    def naviagte_posts(self):
        i=0
        for link in self.df.Comments_Profile_Link:
            print(f"Scraping {i+1} of {len(self.df.Comments_Profile_Link)}: ", link)
            self.driver.get(link)
            sleep(15)
            self.get_data()
            sleep(7)
            i= i+1

    def get_data(self):
        try:
            more_info= self.driver.find_element_by_xpath('//a[@data-control-name="contact_see_more"]')
            more_info.click()
            sleep(5)
        except Exception:
            pass
        try:
            email= self.driver.find_element_by_xpath('//section[@class="pv-contact-info__contact-type ci-email"]/div/a')
            self.email.append(email.text)
        except Exception:
            self.email.append('NA')
            pass
        print(self.email)
        try:
            number=self.driver.find_element_by_xpath('//section[@class="pv-contact-info__contact-type ci-phone"]//span[@class="t-14 t-black t-normal"]')
            self.number.append(number.text)
        except Exception:
            self.number.append('NA')
            pass
        print(self.number)

    def log_in(self, ):
        try:
            log_in_button = self.driver.find_element_by_link_text('Sign in')
            log_in_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print('Unable to find login button')
            user_name_input = self.driver.find_element_by_xpath('//form//input[@placeholder= "Email"]')
            user_name_input.send_keys(self.username)
            password_input = self.driver.find_element_by_xpath('//form//input[@placeholder= "Password"]')
            password_input.send_keys(self.password)
            user_name_input.submit()
        else:
            try:
                user_name_input = self.driver.find_element_by_xpath('//div[@class="form__input--floating"]/input[@id="username"]')
                user_name_input.send_keys(self.username)
                password_input = self.driver.find_element_by_xpath('//div[@class="form__input--floating"]/input[@id="password"]')
                password_input.send_keys(self.password)
                user_name_input.submit()
            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self.error = True




if __name__ == '__main__':
    app = App()
