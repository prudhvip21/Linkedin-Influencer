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
        self.driver = webdriver.Chrome('F:\chromedriver') #Change this to your ChromeDriver path.
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.post_links= []
        self.post_content= []
        self.hastags= []
        self.contains_img= []
        self.timestamp= []
        self.no_of_likes= []
        self.like_names= []
        self.like_headlines= []
        self.like_profile_links= []
        self.no_of_comments= []
        self.comment_names= []
        self.comment_headlines= []
        self.comment_profile_links= []
        self.naviagte_posts()
        sleep(5)
        self.driver.close()


    def write_captions_to_excel_file(self):
        mydict= {}
        mydict['Post_links']= self.post_links
        mydict['Content']= self.post_content
        mydict['Hastags']= self.hastags
        mydict['Contains_img']= self.contains_img
        mydict['Timestamp']= self.timestamp
        mydict['Likes_count']= self.no_of_likes
        mydict['Like_Names']= self.like_names
        mydict['Like_Headlines']= self.like_headlines
        mydict['Like_Profile_Link']= self.like_profile_links
        mydict['Comments_count']= self.no_of_comments
        mydict['Comments_Names']= self.comment_names
        mydict['Comments_Headlines']= self.comment_headlines
        mydict['Comments_Profile_Link']= self.comment_profile_links
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
            post_content= self.driver.find_element_by_xpath('//div[@dir="ltr"]//span[@class= "ember-view"]/span').text
            self.post_content.append(post_content)
        except Exception:
            self.post_content.append('No Content')
            pass
        sleep(2)
        try:
            hastags = self.driver.find_elements_by_xpath('//span[@class= "hashtag-a11y__name"]')
            hastags= [hash.text for hash in hastags]
            self.hastags.append(hastags)
        except Exception:
            self.hastags.append('No Hastags')
            pass
        sleep(2)
        try:
            no_of_comments= self.driver.find_element_by_xpath('//button[@data-control-name="comments_count"]/span').text
            self.no_of_comments.append(no_of_comments)
        except Exception:
            self.no_of_comments.append('Zero Comments')
            pass
        sleep(2)
        try:
            if self.driver.find_element_by_xpath('//div[@class="feed-shared-update-v2__content feed-shared-image feed-shared-image--single-image ember-view"]'):
                contains_img= True
            else:
                contains_img= False
            self.contains_img.append(contains_img)
        except Exception:
            self.contains_img.append('NA')
            pass
        sleep(2)
        try:
            get_attri= self.driver.find_elements_by_xpath('//div[@class="feed-shared-text-view white-space-pre-wrap break-words ember-view"]/span/span/span')
            timestamp= get_attri[1].text
            self.timestamp.append(timestamp)
        except Exception:
            self.timestamp.append('NA')
            pass
        sleep(2)
        try:
            for j in range(5000):
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                sleep(5)
        except Exception:
            print("Problem in finding the load more comments buttons")
            pass
        try:
            for j in range(5000):
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_comments.click()
                sleep(5)
        except Exception:
            print("Problem in finding the load previous comments buttons")
            pass
        try:
            profile_link= self.driver.find_elements_by_xpath('//a[@class="feed-shared-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]')
            profile_link= [ ("www.linkedin.com/" + link.get_attribute("href")) for link in profile_link]
            self.comment_profile_links.append(profile_link)
        except Exception:
            pass
        sleep(2)
        try:
            profile_name= self.driver.find_elements_by_xpath('//h3[@class="feed-shared-post-meta__actor  t-12 t-black--light t-normal"]/span/span[@class="hoverable-link-text"]')
            profile_name= [name.text for name in profile_name]
            self.comment_names.append(profile_name)
        except Exception:
            pass
        sleep(2)
        try:
            profile_headline= self.driver.find_elements_by_xpath('//h3[@class="feed-shared-post-meta__actor  t-12 t-black--light t-normal"]/span[@class="feed-shared-post-meta__headline t-12 t-black--light t-normal"]')
            profile_headline= [head.text for head in profile_headline]
            self.comment_headlines.append(profile_headline)
        except Exception:
            pass
        sleep(2)
        self.driver.execute_script('window.scrollTo(0, 0);')
        sleep(5)
        try:
            no_of_likes = self.driver.find_element_by_css_selector('span.social-details-social-counts__reactions-count').text
            no_of_likes = str(no_of_likes).replace(',', '')
            no_of_likes = int(no_of_likes)
            self.no_of_likes.append(no_of_likes)
        except Exception:
            self.no_of_likes.append('No Likes')
            pass
        sleep(2)
        try:
            like_button = self.driver.find_element_by_xpath('//button[@data-control-name="likes_count"]')
            like_button.click()
            sleep(5)
        except Exception:
            print("Unable to find like button")
            pass
        sleep(5)
        try:
            no_of_scrolls = int(no_of_likes/6) + 40
            eula = self.driver.find_element_by_css_selector('div.social-details-reactors-modal__content')
            for value in range(no_of_scrolls):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
                self.driver.execute_script('arguments[0].scrollBy(0,-250)', eula)
                sleep(3)
        except Exception:
            pass
        sleep(5)
        try:
            names= self.driver.find_elements_by_xpath('//h3[@class="name"]/span[@dir="ltr"]')
            names= [name.text for name in names]
            self.like_names.append(names)
        except Exception:
            self.like_names.append(['No Likes'])
            pass
        sleep(5)
        try:
            headlines= self.driver.find_elements_by_xpath('//p[@class="headline"]')
            headlines= [headline.text for headline in headlines]
            self.like_headlines.append(headlines)
        except Exception:
            self.like_headlines.append(['No Headlines'])
            pass
        sleep(5)
        try:
            links= self.driver.find_elements_by_xpath('//li[@class="actor-item"]/a')
            links= [link.get_attribute("href") for link in links]
            self.like_profile_links.append(links)
        except Exception:
            self.like_profile_links.append(['No Links'])
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
