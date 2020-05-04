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
        self.driver = webdriver.Chrome('F:\chromedriver') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.like_names= []
        self.like_headlines= []
        self.like_profile_links= []
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Like_Names']= self.like_names
        mydict['Like_Headlines']= self.like_headlines
        mydict['Like_Profile_Link']= self.like_profile_links
        elem = pd.DataFrame(mydict)
        elem.to_csv('Likes_data.csv', index=False)


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/posts/prudhvip_so-is-data-science-for-everyone-1-million-activity-6546017160911740928-ywr2/'
        print("Scraping: ", link)
        self.driver.get(link)
        sleep(10)
        self.get_data()
        sleep(5)

    def get_data(self):
        try:
            no_of_likes = self.driver.find_element_by_css_selector('span.social-details-social-counts__reactions-count').text
            no_of_likes = str(no_of_likes).replace(',', '')
            no_of_likes = int(no_of_likes)
            print(f"Post has {no_of_likes} Likes")
        except Exception:
            pass
        sleep(2)
        try:
            like_button = self.driver.find_element_by_xpath('//button[@data-control-name="likes_count"]')
            like_button.click()
            sleep(5)
        except Exception:
            print("Unable to find like button")
            pass
        sleep(10)
        try:
            no_of_scrolls = int(no_of_likes/6) + 50
            eula = self.driver.find_element_by_css_selector('div.social-details-reactors-modal__content')
            print("Scrolling.....")
            for value in tqdm(range(no_of_scrolls)):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
                self.driver.execute_script('arguments[0].scrollBy(0,-250)', eula)
                sleep(3)
        except Exception:
            pass
        sleep(5)
        try:
            names= self.driver.find_elements_by_xpath('//h3[@class="name"]/span[@dir="ltr"]')
            names= [name.text for name in names]
            print(f"Scraped {len(names)} Likes")
            self.like_names = names
        except Exception:
            pass
        sleep(5)
        try:
            headlines= self.driver.find_elements_by_xpath('//p[@class="headline"]')
            headlines= [headline.text for headline in headlines]
            self.like_headlines = headlines
        except Exception:
            pass
        sleep(5)
        try:
            links= self.driver.find_elements_by_xpath('//li[@class="actor-item"]/a')
            links= [link.get_attribute("href") for link in links]
            self.like_profile_links = links
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
