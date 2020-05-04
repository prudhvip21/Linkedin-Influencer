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
        for link in links:
            self.driver.get(link)
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
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("Thanks a lot for reaching out and supporting our initiative of providing free tutorials.Steps to Access the regression tutorial as you have asked for. In case you have requested, freedom bundle as well, we will send another message in a week.")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(7)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("1. Click the link - https://www.supervisedlearning.com/course/course-v1:SupervisedLearning.com+ML_Reg+July_2019")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(5)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("2. Please register with your email id and verify email id")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("3. Once done, you can see - 'view course' click it.")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("4. Click 'course' tab and enjoy the tutorial.")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("5. Please provide feedback at the end to get more free stuff.")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(3)
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys("6. Reach out to us - learn@supervisedlearning.com")
                self.driver.find_element_by_xpath('//div[@class="msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1 notranslate"]').send_keys(Keys.ENTER)
                sleep(7)
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
