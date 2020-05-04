from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from xlsxwriter import Workbook
import os
import ast
import requests
import shutil
import pandas as pd
import numpy as np
from selenium.webdriver.common.keys import Keys
from html2text import HTML2Text
import re
import gc
from tqdm import tqdm

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997'):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox('.')
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.instantiate_varibales()
        sleep(5)
        self.naviagte_posts()
        sleep(15)
        self.driver.close()

    def instantiate_varibales(self):
        self.post_link= list()
        self.post_date= list()
        self.post_content= list()
        self.likes_count = list()
        self.comments_count= list()
        self.like_names= list()
        self.like_headlines= list()
        self.like_profile_link = list()
        self.comment_names = list()
        self.comment_headlines= list()
        self.comment_profile_link = list()
        self.comment_content = list()

    def write_captions_to_excel_file(self, i):
        mydict = dict()
        mydict['post_link']= self.post_link
        mydict['post_date']= self.post_date
        mydict['post_content']= self.post_content
        mydict['likes_count']= self.likes_count
        mydict['comments_count']= self.comments_count
        mydict['like_names']= self.like_names
        mydict['like_headlines']= self.like_headlines
        mydict['like_profile_link']= self.like_profile_link
        mydict['comment_names']= self.comment_names
        mydict['comment_headlines']= self.comment_headlines
        mydict['comment_profile_link']= self.comment_profile_link
        mydict['comment_content']= self.comment_content
        elem = pd.DataFrame(mydict)
        elem.to_excel(f'Data/posts_data_{i}.xlsx', index=False)
        self.instantiate_varibales()
        gc.collect()

    def naviagte_posts(self):
        dump_df= pd.read_csv("../new_data_dump/Shares.csv")
        dump_df= dump_df.drop_duplicates(subset= 'ShareLink')
        dump_df.reset_index(drop= True ,inplace= True)
        for i in range(30, dump_df.shape[0]):
            print(f"{i+1} out of {len(dump_df.ShareLink)}")
            print(f"{dump_df.ShareLink[i]}------->")
            try:
                self.driver.get(dump_df.ShareLink[i])
            except Exception:
                continue
                pass
            self.post_link.append(dump_df.ShareLink[i])
            self.post_date.append(dump_df.Date[i])
            self.post_content.append(dump_df.ShareCommentary[i])
            sleep(10)
            self.get_data()
            if (i+1)% 5 == 0:
                self.write_captions_to_excel_file((i+1)//5)
        sleep(5)

    def get_data(self):

        try:
            likes_count= self.driver.find_element_by_xpath('//span[@class="v-align-middle social-details-social-counts__reactions-count"]').get_attribute('textContent')
            self.likes_count.append(likes_count)
        except Exception:
            likes_count= 0
            self.likes_count.append('0')
            pass
        print("Likes Count: ", likes_count)
        print("Updated Likes: ", len(self.likes_count))
        try:
            comments_count= self.driver.find_element_by_xpath('//button[@data-control-name="comments_count"]/span').get_attribute('textContent')
            self.comments_count.append(comments_count)
        except  Exception:
            comments_count= 0
            self.comments_count.append('0 Comments')
            pass
        print("Comments Count", comments_count)
        print("Updated Comments: ", len(self.comments_count))
        try:
            like_button = self.driver.find_element_by_xpath('//button[@data-control-name="likes_count"]')
            like_button.click()
            sleep(2)
            no_of_likes= int(likes_count.replace(',', ''))
            no_of_scrolls = int(no_of_likes/6) + 50
            eula = self.driver.find_element_by_xpath('//div[@class="artdeco-modal__content social-details-reactors-modal__content ember-view"]')
            print('Scolling Likes.....')
            for value in tqdm(range(no_of_scrolls)):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
                sleep(3)
            self.driver.execute_script('arguments[0].scrollTop = 0', eula)
            sleep(2)
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
            sleep(5)
            try:
                names= self.driver.find_elements_by_xpath('//h3[@class="name"]/span[@dir="ltr"]')
                names= [name.get_attribute('textContent') for name in names]
                self.like_names.append(names)
                print("Likes Names: ", len(names))
            except Exception:
                self.like_names.append([])
                pass
            sleep(3)
            print("Updated Like Names: ", len(self.like_names))
            try:
                headlines= self.driver.find_elements_by_xpath('//p[@class="headline"]')
                headlines= [headline.get_attribute('textContent') for headline in headlines]
                self.like_headlines.append(headlines)
                print("Likes Headlines :", len(headlines))
            except Exception:
                self.like_headlines.append([])
                pass
            sleep(3)
            print("Updated Like Headlines :", len(self.like_headlines))
            try:
                links= self.driver.find_elements_by_xpath('//li[@class="actor-item"]/a')
                links= [link.get_attribute("href") for link in links]
                self.like_profile_link.append(links)
                print("Likes Links: ", len(links))
            except Exception:
                self.like_profile_link.append([])
                pass
            sleep(3)
            print("Updated Like Links :", len(self.like_profile_link))
        except Exception:
            pass
        try:
            close= self.driver.find_element_by_xpath('//button[@data-test-modal-close-btn]')
            close.click()
            sleep(5)
        except Exception:
            pass
        sleep(4)
        # top_comments= self.driver.find_element_by_xpath('//artdeco-dropdown-trigger[@class="comments-sort-order-toggle__trigger ember-view"]')
        # top_comments.click()
        # sleep(3)
        # sleep(3)
        # recent_comments= self.driver.find_element_by_xpath('//artdeco-dropdown[@class="comments-sort-order-toggle__dropdown ember-view"]//div[@class="artdeco-dropdown__content-inner"]/ul/li[@class="single-line"][2]')
        # self.driver.execute_script("window.scrollBy(0, 500);")
        # recent_comments.click()
        sleep(5)
        for i in range(100):
            try:
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                print("Clicking More Comments")
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except Exception:
                print("Problem in finding the load more comments buttons")
                break
        for i in range(100):
            try:
                more_replies = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_replies.click()
                print("Clicking More Replies")
                sleep(5)
            except Exception:
                print("Problem in finding the load more Replies buttons")
                break
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(5)
        h = HTML2Text()
        h.ignore_links = True
        try:
            profile_links= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor" and @class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view" or @data-control-name="reply_actor"and@class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [link.get_attribute("href") for link in profile_links]
            print("Comments Links:", len(profile_link))
            self.comment_profile_link.append(profile_link)
            profile_name= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor" and @class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view" or @data-control-name="reply_actor"and@class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//h3/span[1]/span[1]')
            profile_name= [name.get_attribute('textContent') for name in profile_name]
            print("Comments Names: ", len(profile_name))
            self.comment_names.append(profile_name)
            headline= self.driver.find_elements_by_xpath('//a[@data-control-name="comment_actor" and @class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view" or @data-control-name="reply_actor"and@class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//h3/span[2]')
            headline= [name.get_attribute('textContent') for name in headline]
            print("Comments Headline: ", len(headline))
            self.comment_headlines.append(headline)
            content= self.driver.find_elements_by_xpath('//div[@class="comments-comment-item-content-body"or@class="comments-reply-item-content-body"]/div/div/p')
            content= [h.handle(con.get_attribute('innerHTML')) for con in content]
            print("Comment Content: ", len(content))
            self.comment_content.append(content)
        except Exception:
            self.comment_profile_link.append(['NA'])
            self.comment_names.append(['NA'])
            self.comment_headlines.append(['NA'])
            self.comment_content.append(['NA'])
            pass
        sleep(2)
        print("Updated Comments Links : ", len(self.comment_profile_link))
        print("Updated Comments Names : ", len(self.comment_names))
        print("Updated Comments Headlines : ", len(self.comment_headlines))
        print("Updated Comments Content : ", len(self.comment_content))

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
