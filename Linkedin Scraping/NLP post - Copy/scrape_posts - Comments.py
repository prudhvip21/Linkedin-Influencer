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
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997', target_username='prudhvip'):

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
        self.comment_profile_links= []
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Comments_Profile_Link']= self.comment_profile_links
        elem = pd.DataFrame(mydict)
        elem.to_csv('Comments_Data4.csv', index=False)


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/posts/prudhvip_on-the-occasion-of-kalams-anniversary-activity-6589736185776693248-xBCv/'
        print("Scraping: ", link)
        self.driver.get(link)
        sleep(20)
        self.get_data()
        sleep(5)

    def get_data(self):
        top_comments= self.driver.find_element_by_xpath('//artdeco-dropdown-trigger[@class="artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view"]')
        top_comments.click()
        recent_comments= self.driver.find_elements_by_xpath('//button[@class="feed-shared-sort-comments__list-item-button t-12"]')
        recent_comments[1].click()
        sleep(3)
        for j in range(33):
            try:
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                print(f"Click Number {j+1}.....")
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except Exception:
                print("Problem in finding the load more comments buttons")
                pass
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(5)
        try:
            profile_link= self.driver.find_elements_by_xpath('//a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [link.get_attribute("href") for link in profile_link]
            self.comment_profile_links = profile_link
        except Exception:
            pass
        sleep(2)

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
