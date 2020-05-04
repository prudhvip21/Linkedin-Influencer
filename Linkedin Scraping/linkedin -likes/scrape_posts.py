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
from selenium.webdriver.common.keys import Keys

class App:
    def __init__(self, username='sahuamanjeet@gmail.com', password='Aman@1997', target_username='prudhvip'):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.driver = webdriver.Chrome('F:\chromedriver') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):

        mydict1= {}
        mydict1['Profile_Link']= self.Profile_Link
        mydict1['profile_name']= self.profile_name
        mydict1['profile_headline']= self.profile_headline
        elem = pd.DataFrame(mydict1)
        elem.to_csv('comments_data.csv', index=False)
        mydict2= {}
        mydict2['comment_content']= self.comment_content
        elem1 = pd.DataFrame(mydict2)
        elem1.to_csv('comments_content.csv', index=False)

    def naviagte_posts(self):
        link_1= 'urn:li:activity:6544087399662739457'
        link= 'https://www.linkedin.com/feed/update/'+ link_1 + '/'
        print(link)
        print(" ------->")
        self.driver.get(link)
        sleep(120)
        self.get_data()
        sleep(10)


    def get_data(self):

        try:
            profile_link= self.driver.find_elements_by_xpath('//article//div[@class="comments-comment-item__post-meta feed-shared-post-meta is-comment feed-shared-post-meta--is-not-sponsored ember-view"]/a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [link.get_attribute("href") for link in profile_link]
            self.Profile_Link = profile_link
        except Exception:
            pass
        sleep(5)
        try:
            profile_name= self.driver.find_elements_by_xpath('//article//div[@class="comments-comment-item__post-meta feed-shared-post-meta is-comment feed-shared-post-meta--is-not-sponsored ember-view"]/a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//span[@class="hoverable-link-text"]')
            profile_name= [name.text for name in profile_name]
            self.profile_name = profile_name
        except Exception:
            pass
        sleep(5)
        try:
            profile_headline= self.driver.find_elements_by_xpath('//article//div[@class="comments-comment-item__post-meta feed-shared-post-meta is-comment feed-shared-post-meta--is-not-sponsored ember-view"]//span[@class="feed-shared-post-meta__headline t-12 t-black--light t-normal"]')
            profile_headline= [head.text for head in profile_headline]
            self.profile_headline= profile_headline
        except Exception:
            pass
        sleep(5)
        try:
            comment_content= self.driver.find_elements_by_xpath('//article//div[@class="comments-comment-item-content-body"]//p/span/span')
            comment_content= [comment.text for comment in comment_content]
            self.comment_content = comment_content
        except Exception:
            pass
        sleep(5)

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
