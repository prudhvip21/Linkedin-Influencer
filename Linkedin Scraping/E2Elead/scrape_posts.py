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
import codecs

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
        self.log_in()
        sleep(3)
        #self.comment_names= []
        #self.comment_headlines= []
        #self.comment_profile_links= []
        self.naviagte_posts()
        sleep(15)
        self.driver.close()


    def write_captions_to_excel_file(self):
        print("Writing to text.............")
        file_object = codecs.open('rawtext.txt', "a+", "utf-8")
        html = self.driver.page_source
        file_object.write(html)


    def naviagte_posts(self):
        links= ['https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6553842331328573440',
                'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6544087399163625472',
                'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6546611976464855041',
                  'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6547341269402775553',
                  'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6549168346590433280',
                  'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6549872035160522752',
                  'https://www.linkedin.com/feed/update/urn%3Ali%3Ashare%3A6552411042381697024']
        for link in links:
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
        no_of_comments= self.driver.find_element_by_xpath('//button[@data-control-name="comments_count"]/span').text
        no_of_comments= no_of_comments.replace(" Comments", "")
        print("Comments: ", no_of_comments)
        for j in range(int(no_of_comments)):
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
        self.write_captions_to_excel_file()

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
