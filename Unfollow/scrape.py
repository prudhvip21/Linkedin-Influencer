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
import re
import math

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997'):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox() #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.profile_links= []
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(4)
        self.get_profile_links()


    def get_profile_links(self):
        self.driver.get("https://www.linkedin.com/in/amanjeetsahu/")
        sleep(2)
        connections= self.driver.find_element_by_xpath('//a[@data-control-name="topcard_view_all_connections"]')
        connection_link= connections.get_attribute('href')
        self.driver.get(connection_link)
        sleep(3)
        number= self.driver.find_element_by_xpath('//h3[@class="search-results__total pt4 pb0 t-14 t-black--light t-normal pl5  clear-both"]')
        number= number.get_attribute('innerText')
        temp = re.findall(r'\d+', number)
        iterator= math.ceil(int(temp[0])/10)
        sleep(2)
        for i in range(1,iterator+1):
            link =connection_link + f'&page={i}'
            self.driver.get(link)
            sleep(1)
            self.driver.execute_script("window.scrollTo(0, 50);")
            sleep(1)
            self.driver.execute_script("window.scrollTo(50, 100);")
            sleep(1)
            self.driver.execute_script("window.scrollTo(100, 150);")
            sleep(1)
            self.driver.execute_script("window.scrollTo(150, 200);")
            sleep(1)
            self.driver.execute_script("window.scrollTo(200, 250);")
            sleep(1)
            self.driver.execute_script("window.scrollTo(250, 300);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(300, 350);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(350, 400);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(400, 450);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(450, 500);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(500, 550);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(550, 600);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(600, 650);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(650, 700);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(700, 750);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(750, 800);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(800, 850);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(850, 900);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(900, 950);")
            sleep(2)
            self.driver.execute_script("window.scrollTo(950, 1000);")
            sleep(2)
            profile_links= self.driver.find_elements_by_xpath('//li[@class="search-result search-result__occluded-item ember-view"]/div/div/div[1]/a')
            profile_links= [links.get_attribute('href') for links in profile_links]
            rand1= np.random.randint(1,10)
            rand2= np.random.randint(1,10)
            for i, links in enumerate(profile_links):
                if i == rand1:
                    self.driver.get(self.main_url)
                    sleep(3)
                if i == rand2:
                    self.driver.get(self.main_url)
                    sleep(3)
                self.driver.get(links)
                sleep(3)
                more_button= self.driver.find_element_by_xpath('//button[@class="ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view"]')
                more_button.click()
                unfollow_button= self.driver.find_element_by_xpath('//div[@class="artdeco-dropdown__content-inner"]/ul/li[6]/div/artdeco-dropdown-item')
                unfollow_button.click()
                sleep(3)
            sleep(7)

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
