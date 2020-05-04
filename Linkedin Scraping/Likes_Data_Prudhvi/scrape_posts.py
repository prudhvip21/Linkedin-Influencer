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
from tqdm import tqdm

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997'):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox() #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.post_links= []
        self.post_date= []
        self.no_of_likes= []
        self.no_comments= []
        self.naviagte_posts()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['post_link']= self.post_links
        mydict['post_date']= self.post_date
        mydict['Likes_count']= self.no_of_likes
        mydict['Comments_count']= self.no_comments
        elem = pd.DataFrame(mydict)
        elem.to_csv('Likes_data.csv', index=False)


    def naviagte_posts(self):
        df= pd.read_csv('Shares.csv')
        post_links= df.ShareLink.to_list()
        index= 1
        for link,date in zip(df.ShareLink.to_list(), df.Date.to_list()):
            self.post_links.append(link)
            self.post_date.append(date)
            print(index , ' Out of ' , len(post_links), ' :')
            print(link)
            self.driver.get(link)
            sleep(6)
            self.get_data()
            if index % 2 == 0:
                self.write_captions_to_excel_file()
            index= index+ 1

    def get_data(self):
        like_comments = self.driver.find_elements_by_xpath('//button[@class="social-details-social-counts__count-value t-12 t-black--light t-normal hoverable-link-text"]/span[@aria-hidden="true"]')
        like_comments= [comments.get_attribute('innerText') for comments in like_comments]
        try:
            print(f"Post has {like_comments[0]} Likes")
            self.no_of_likes.append(like_comments[0])
        except Exception:
            self.no_of_likes.append('0')
            pass
        try:
            print(f"Post has {like_comments[1]} comments")
            self.no_comments.append(like_comments[1])
        except Exception:
            self.no_comments.append('0 Comments')
            pass
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
