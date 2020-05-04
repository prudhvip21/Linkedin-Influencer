from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil
import pandas as pd


class App:
    def __init__(self, username='sahuamanjeet@gmail.com', password='Aman@1997', target_username='amanjeetsahu',
                 path='/home/lazar/Desktop/instaPhotos'): #Change this to your Instagram details and desired images path
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = webdriver.Chrome('F:\chromedriver') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.open_target_profile()
        sleep(3)
        self.scroll_down()
        sleep(3)
        self.get_post_links()
        sleep(3)
        self.naviagte_posts()
        sleep(2)
        self.driver.close()

    def naviagte_posts(self):
        print(self.post_links[0])
        self.link= 'www.linkedin.com/feed/update/' + self.post_links[0] + '/'
        print(link)
        #sleep(5)
        #self.find_like()
        #sleep(3)

    def find_like(self):
        like_button = self.driver.find_element_by_xpath('//button[@class="social-details-social-counts__count-value"]')
        like_button.click()
        sleep(5)

    def get_post_links(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        all_posts = soup.find_all('div',attrs={"class" : "feed-shared-update-v2"})
        self.post_links= []
        for post in all_posts:
            self.post_links.append(post.attrs['data-id'])
        print(len(self.post_links))
        elem = pd.DataFrame(self.post_links)
        elem.to_csv('post_links.csv', index=False)

    def scroll_down(self):
        try:
            for value in range(15):
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
        except Exception as e:
            self.error = True
            print(e)
            print('Some error occurred while trying to scroll down')
        sleep(5)

    def open_target_profile(self):
            target_profile_url = self.main_url + '/'+ 'in' + '/' + self.target_username + '/' + 'detail/recent-activity/shares/'
            self.driver.get(target_profile_url)
            sleep(5)


    def log_in(self, ):
        try:
            log_in_button = self.driver.find_element_by_link_text('Sign in')
            log_in_button.click()
            sleep(3)
        except Exception:
            self.error = True
            print('Unable to find login button')
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
