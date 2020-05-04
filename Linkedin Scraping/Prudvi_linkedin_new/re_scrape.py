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

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997', target_username='prudhvip'):
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

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
        self.names= []
        self.badges= []
        self.headlines= []
        self.links= []
        self.naviagte_posts()
        sleep(15)
        self.write_captions_to_excel_file()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Names']= self.names
        mydict['Badges']= self.badges
        mydict['Headlines']= self.headlines
        mydict['Profile_Link']= self.links
        elem = pd.DataFrame(mydict)
        elem.to_csv('re_likes_data.csv', index=False)

    def naviagte_posts(self):
        df= pd.read_csv('amb_links.csv', index_col= False, header=None)
        post_links= df.iloc[1:, 0].tolist()
        post_links= list(map(str.strip, post_links))
        index= 1
        for link in post_links:
            print(index , ' Out of ' , len(post_links), ' :')
            print(link)
            self.driver.get(link)
            sleep(2)
            self.get_data()
            sleep(3)
            index= index+ 1
        sleep(2)
    def get_data(self):
        try:
            no_of_likes = self.driver.find_element_by_css_selector('span.social-details-social-counts__reactions-count').text
            no_of_likes = str(no_of_likes).replace(',', '')
            no_of_likes = int(no_of_likes)
        except Exception:
            pass
        sleep(2)
        try:
            like_button = self.driver.find_element_by_xpath('//button[@data-control-name="likes_count"]')
            like_button.click()
            sleep(5)
        except Exception:
            pass
        sleep(120)
        #try:
            #no_of_scrolls = int(no_of_likes/6) + 30
            #eula = self.driver.find_element_by_css_selector('div.social-details-reactors-modal__content')
            #for value in range(no_of_scrolls):
                #self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
                #sleep(5)
        #except Exception:
            #pass
        print('Scraping Profile Data')
        try:
            names= self.driver.find_elements_by_xpath('//h3[@class="name"]/span[@dir="ltr"]')
            names= [name.text for name in names]
            self.names.append(names)
        except Exception:
            self.names.append(['No Likes'])
            pass
        sleep(3)
        try:
            badges= self.driver.find_elements_by_xpath('//h3[@class="name"]//span[@class= "dist-value"]')
            badges= [badge.text for badge in badges]
            self.badges.append(badges)
        except Exception:
            self.badges.append(['No Badges'])
            pass
        sleep(3)
        try:
            headlines= self.driver.find_elements_by_xpath('//p[@class="headline"]')
            headlines= [headline.text for headline in headlines]
            self.headlines.append(headlines)
        except Exception:
            self.headlines.append(['No Headlines'])
            pass
        sleep(3)
        try:
            links= self.driver.find_elements_by_xpath('//li[@class="actor-item"]/a')
            links= [link.get_attribute("href") for link in links]
            self.links.append(links)
        except Exception:
            self.links.append(['No Links'])
            pass
        sleep(3)


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
