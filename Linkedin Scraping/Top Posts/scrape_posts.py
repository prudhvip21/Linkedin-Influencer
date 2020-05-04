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
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997', target_username='prudhvip'):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.driver = webdriver.Firefox() #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.post_links= []
        self.post_content= []
        self.no_of_likes= []
        self.naviagte_posts()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Post_links']= self.post_links
        mydict['Content']= self.post_content
        mydict['Likes_count']= self.no_of_likes
        elem = pd.DataFrame(mydict)
        elem.to_csv('linkedin_data_prudhvi.csv', index=False)


    def naviagte_posts(self):
        df= pd.read_csv('post_links.csv', index_col= False, header=None)
        post_links= df.iloc[1:, 0].tolist()
        post_links= list(map(str.strip, post_links))
        index= 1
        for link in post_links:
            link= 'https://www.linkedin.com/feed/update/'+ link + '/'
            self.post_links.append(link)
            print(index , ' Out of ' , len(post_links), ' :')
            print(link)
            self.driver.get(link)
            sleep(10)
            self.get_data()
            sleep(5)
            self.write_captions_to_excel_file()
            index= index+ 1

    def get_data(self):
        try:
            post_content= self.driver.find_elements_by_xpath('//div[@dir="ltr"]//span[@class= "ember-view"]/span')
            self.post_content.append(post_content[0].text)
        except Exception:
            self.post_content.append('No Content')
            pass
        sleep(2)
        try:
            no_of_likes = self.driver.find_element_by_css_selector('span.social-details-social-counts__reactions-count').text
            no_of_likes = str(no_of_likes).replace(',', '')
            no_of_likes = int(no_of_likes)
            self.no_of_likes.append(no_of_likes)
        except Exception:
            self.no_of_likes.append('No Likes')
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
