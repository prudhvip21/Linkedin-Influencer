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
    def __init__(self, username='prudhvi.potuganti@gmail.com', password='9849027440', target_username='prudhvip'):

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
        #self.comment_profile_links= []
        self.log_in()
        sleep(7)
        self.naviagte_posts()
        sleep(15)
        self.driver.close()


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/posts/prudhvip_datascience-machinelearning-ai-activity-6567639554063458304-2s-k'
        print("Scraping: ", link)
        self.driver.get(link)
        sleep(10)
        self.get_data()
        sleep(5)


    def get_data(self):
        try:
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            badges= self.driver.find_elements_by_xpath('//a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//span[@class="feed-shared-post-meta__distance-badge distance-badge separator ember-view"]//span[@class="dist-value"]')
            #reply_button= find_elements_by_xpath('//button[@data-control-name="reply"]')
            print([badge.text for badge in badges])
            #print(reply_button)
            '''i = 0
            for badge in badges:
                if badge.text != '1st':
                    reply_button[i].click()
                    sleep(10)
                i=i+1
            self.comment_profile_links = profile_link'''
        except Exception:
            print("Not able to click")
            pass
        sleep(30)

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
