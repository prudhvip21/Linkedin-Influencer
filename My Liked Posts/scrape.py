from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        self.like_link= list()
        self.like_date= list()
        self.corp= list()
        self.like_type= list()
        self.like_name= list()
        self.like_headline= list()
        self.like_profile_link= list()
        self.like_content = list()

    def write_captions_to_excel_file(self, i):
        mydict = dict()
        mydict['like_link']= self.like_link
        mydict['like_date']= self.like_date
        mydict['corp']= self.corp
        mydict['like_type']= self.like_type
        mydict['like_name']= self.like_name
        mydict['like_headline']= self.like_headline
        mydict['like_profile_link']= self.like_profile_link
        mydict['like_content']= self.like_content
        elem = pd.DataFrame(mydict)
        elem.to_excel(f'New Data/likes_data_{i}.xlsx', index=False)
        self.instantiate_varibales()
        gc.collect()

    def naviagte_posts(self):
        dump_df= pd.read_csv("../new_data_dump/Reactions.csv")
        dump_df= dump_df.drop_duplicates(subset= 'Link')
        dump_df.reset_index(drop= True ,inplace= True)
        dump_df['corp']= dump_df.Link.apply(lambda x: 'Comment' if 'comment' in str(x) else 'post')
        for i in range(dump_df.shape[0]):
            print(f"{i+1} out of {len(dump_df.Link)}")
            print(f"{dump_df.Link[i]}------->")
            print(dump_df['corp'][i])
            try:
                self.driver.get(dump_df.Link[i])
            except Exception:
                continue
                pass
            self.like_link.append(dump_df.Link[i])
            self.like_date.append(dump_df.Date[i])
            self.like_type.append(dump_df.Type[i])
            self.corp.append(dump_df.corp[i])
            sleep(10)
            if dump_df.corp[i] == 'Comment':
                self.get_comment_data(dump_df.Link[i])
            else:
                self.get_post_data(dump_df.Link[i])
            if (i+1)% 50 == 0:
                self.write_captions_to_excel_file((i+1)//50)
        sleep(5)

    def get_comment_data(self, link):
        for i in range(40):
            try:
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                print("Clicking More Comments")
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            except Exception:
                print("Problem in finding the load more comments buttons")
                break
        for i in range(20):
            try:
                more_replies = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_replies.click()
                print("Clicking More Replies")
                sleep(5)
            except Exception:
                print("Problem in finding the load more Replies buttons")
                break
        sleep(2)
        try:
            comment= link
            comment= [com[2:] for com in re.findall('[A-Za-z0-9]{2}[0-9]{19}', comment)]
            res = []
            for i in comment:
                if i not in res:
                    res.append(i)
            comment= res
            xp = f'//article[@data-id="urn:li:comment:(activity:{comment[0]},{comment[1]})"]'
            comment= self.driver.find_element_by_xpath(xp)
            name= self.driver.find_element_by_xpath(f'{xp}/div[1]/a[2]/h3/span/span[1]').get_attribute('textContent')
            headline= self.driver.find_element_by_xpath(f'{xp}/div[1]/a[2]/h3/span[2]').get_attribute('textContent')
            link= self.driver.find_element_by_xpath(f'{xp}/div[1]/a[1]').get_attribute('href')
            content= self.driver.find_element_by_xpath(f'{xp}/div[3]/div/div/p').get_attribute('innerHTML')
            h= HTML2Text()
            h.ignore_links =True
            content= h.handle(content)
            self.like_name.append(name)
            self.like_headline.append(headline)
            self.like_profile_link.append(link)
            self.like_content.append(content)
        except Exception:
            name= 'NA'
            headline= 'NA'
            link= 'NA'
            content= 'NA'
            self.like_name.append('NA')
            self.like_headline.append('NA')
            self.like_profile_link.append('NA')
            self.like_content.append('NA')
            pass
        print('like_name: ', name)
        print('like_headline: ', headline)
        print('like_profile_link: ', link)
        print('like_content: ', content)


    def get_post_data(self, link):
        try:
            name= self.driver.find_element_by_xpath('//a[@data-control-name="actor_container"]//span[@class="feed-shared-actor__title"]/span/span').get_attribute('textContent')
            headline= self.driver.find_element_by_xpath('//a[@data-control-name="actor_container"]//span[@class="feed-shared-actor__description t-12 t-black--light t-normal"]/div/span').get_attribute('textContent')
            link= self.driver.find_element_by_xpath('//a[@data-control-name="actor_container"]').get_attribute('href')
            content= self.driver.find_element_by_xpath('//div[@class="feed-shared-text__text-view feed-shared-text-view white-space-pre-wrap break-words ember-view"]').get_attribute('innerHTML')
            h= HTML2Text()
            h.ignore_links =True
            content= h.handle(content)
            self.like_name.append(name)
            self.like_headline.append(headline)
            self.like_profile_link.append(link)
            self.like_content.append(content)
        except Exception:
            name= 'NA'
            headline= 'NA'
            link= 'NA'
            content= 'NA'
            self.like_name.append('NA')
            self.like_headline.append('NA')
            self.like_profile_link.append('NA')
            self.like_content.append('NA')
            pass
        print('like_name: ', name)
        print('like_headline: ', headline)
        print('like_profile_link: ', link)
        print('like_content: ', content)

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
