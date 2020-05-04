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
    def __init__(self, username='prudhvi.potuganti@gmail.com', password='9849027440', target_username='prudhvip'):
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
        self.comment_profile_links= []
        self.log_in()
        sleep(3)
        self.naviagte_posts()
        sleep(15)
        self.driver.close()


    def naviagte_posts(self):
        link= 'https://www.linkedin.com/posts/prudhvip_endtoend-activity-6564027612602167296-a51V/'
        print("Scraping: ", link)
        self.driver.get(link)
        sleep(10)
        self.get_data()
        sleep(5)

    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Comments_Profile_Link']= self.comment_profile_links
        df= pd.read_csv('Comments_Data_regression.csv')
        df = df.append(pd.DataFrame(mydict), ignore_index=True)
        df.to_csv('Comments_Data_regression.csv', index=False)


    def get_data(self):
        try:
            for j in range(5):
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                print(f"Click Number {j+1}.......")
                self.driver.execute_script('window.scrollBy(0,-450)')
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(5)
            for j in range(5):
                more_replies = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_replies.click()
                sleep(5)
        except Exception:
            print("Problem in finding the load more comments buttons")
            pass
        try:
            profile_link= self.driver.find_elements_by_xpath('//a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [link.get_attribute("href") for link in profile_link]
            self.comment_profile_links = profile_link
        except Exception:
            pass
        sleep(2)
        self.write_captions_to_excel_file()
        sleep(3)

        for i in range(len(profile_link)):
            try:
                delete_comments_btn = self.driver.find_element_by_xpath('//artdeco-dropdown-trigger[@class="comment-options-trigger ember-view"]')
                delete_comments_btn.click()
                print(f"Delete Number {j+1}.......")
            except Exception:
                print("Problem in finding dots button")
            else:
                try:
                    close_conversation= self.driver.find_elements_by_xpath('//button[@data-control-name="overlay.close_conversation_window"]')
                    for j in range(len(close_conversation)):
                        close_conversation[j].click()
                except Exception:
                    pass
            sleep(3)
            try:
                delete_comments = self.driver.find_elements_by_xpath('//li[@class="single-line"]/artdeco-dropdown-item[@class="option-button ember-view"]')
                if len(delete_comments) == 4:
                    delete_comments[3].click()
                else:
                    delete_comments[2].click()
            except Exception:
                print("Problem in finding button delete_comments")
                pass
            sleep(3)
            try:
                confirm_delete= self.driver.find_element_by_xpath('//div[@class="artdeco-modal__actionbar text-align-right ember-view"]/button[@class="artdeco-button artdeco-button--2 artdeco-button--primary ember-view"]')
                confirm_delete.click()
            except Exception:
                print("Problem in finding button confirm_delete")
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
