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

class App:
    def __init__(self):
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
        self.profile_name= []
        self.headline= []
        self.content= []
        self.likes= []
        self.replies= []
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Comments_Profile_name']= self.profile_name
        mydict['Comments_Profile_headline']= self.headline
        mydict['Comments_Profile_Link']= self.comment_profile_links
        mydict['comments_content']= self.content
        mydict['Comments_likes']= self.likes
        mydict['Comments_replies']= self.replies
        elem = pd.DataFrame(mydict)
        elem.to_csv('Comments_Data_app.csv', index=False)


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/posts/warikoo_warikooasks-activity-6594495435333828608-f6FZ'
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
        for j in range(40):
            try:
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                print(f"Click Number {j+1}.....")
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except Exception:
                print("Problem in finding the load more comments buttons")
                pass
        try:
            for j in range(40):
                more_replies = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_replies.click()
                sleep(5)
        except Exception:
            print("Problem in finding the load more Replies buttons")
            pass
        sleep(5)
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(5)
        try:
            profile_links= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor"  and @class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [link.get_attribute("href") for link in profile_links]
            self.comment_profile_links = profile_link
            profile_name= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor"  and @class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//span[@class="hoverable-link-text"]')
            profile_name= [name.text for name in profile_name]
            self.profile_name = profile_name
            headline= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor"  and @class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//span[@class="feed-shared-post-meta__headline t-12 t-black--light t-normal"]')
            headline= [name.text for name in headline]
            self.headline= headline
            content= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor"  and @class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]/../..//div[@class="comments-comment-item-content-body"]//p')
            content= [con.get_attribute('innerHTML') for con in content]
            self.content=content
        except Exception:
            pass
        sleep(2)
        new_likes= []
        for link in profile_link:
            try:
                link= link[24:]
                num_likes= self.driver.find_element_by_xpath(f'//a[@data-control-name="comment_actor"  and @href=\"{link}\"]/../..//div[@class="comments-comment-item__social-actions "]//button[@class="comments-comment-social-bar__likes-count hoverable-link-text"]/span[@aria-hidden="true"]')
                new_likes.append(num_likes.text)
            except Exception:
                new_likes.append("No Likes")
        print(len(new_likes))
        self.likes=new_likes
        new_replies= []
        for link in profile_link:
            try:
                link= link[24:]
                num_likes= self.driver.find_element_by_xpath(f'//a[@data-control-name="comment_actor"  and @href=\"{link}\"]/../..//div[@class="comments-comment-item__social-actions "]//button[@class="comments-comment-social-bar__replies-count hoverable-link-text"]/span[@aria-hidden="true"]')
                new_replies.append(num_likes.text)
            except Exception:
                new_replies.append("No Replies")
        print(len(new_replies))
        self.replies=new_replies
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
