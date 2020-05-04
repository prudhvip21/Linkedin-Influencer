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

class App:
    def __init__(self, username='prudhvi.potuganti@gmail.com', password='9849027440'):

        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.new_connects= []
        self.log_in()
        sleep(10)
        self.send_msg()
        sleep(5)
        self.write_captions_to_excel_file()
        self.driver.close()

    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['profile_links']= self.new_connects
        df= pd.read_csv('new_connections.csv')
        df = df.append(pd.DataFrame(mydict), ignore_index=True)
        df.to_csv('new_connections.csv', index=False)


    def send_msg(self):
        links_df= pd.read_csv('list.csv')
        links= links_df.profile_links
        i = 1
        for link in links:
            print(f"Sending {i} out of {len(links)}........")
            self.driver.get(str(link))
            i= i + 1
            sleep(10)
            try:
                try:
                    close_conversation= self.driver.find_elements_by_xpath('//button[@data-control-name="overlay.close_conversation_window"]')
                    for j in range(len(close_conversation)):
                        close_conversation[j].click()
                except Exception:
                    pass
                message_button= self.driver.find_element_by_xpath('//button[@class="pv-s-profile-actions pv-s-profile-actions--message ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]')
                message_button.click()
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("Hi, ")
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("I have noticed that you have responded to my status about End to End Data Science course. We are starting our next batch and if interested, share email id for more details.")
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(2)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(" It's a 3 mo course with 100 hours live teaching followed by 6 months mentoring from me. The pricing is 35k INR for 9 months program. Personalized mentoring is our unique offering. Classes will be held every Sat and Sunday - 5:00 PM to 8:00 PM with recordings access.")
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("Reply or send email for more details.")
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
            except Exception:
                self.new_connects.append(link)
                self.write_captions_to_excel_file()
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
