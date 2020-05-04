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
from html2text import HTML2Text
import re
import gc

class App:
    def __init__(self, username='amanjitsahu@gmail.com', password='Aman@1997'):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox('.')
        self.error = False
        self.main_url = 'https://www.linkedin.com'
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        sleep(3)
        self.instantiate_varibales()
        sleep(5)
        self.naviagte_posts()
        sleep(15)
        self.driver.close()

    def instantiate_varibales(self):
        self.post_link= list()
        self.profile_name= list()
        self.profile_headline= list()
        self.likes_count= list()
        self.comments_count= list()
        self.post_content= list()
        self.comment_post_link= list()
        self.comment_content= list()
        self.comment_likes_counts= list()
        self.like_names= list()
        self.like_headlines= list()
        self.like_profile_links= list()
        self.comment_reply_counts= list()
        self.comments_replies_content= list()
        self.comments_replies_names= list()
        self.comments_replies_headlines= list()
        self.comments_replies_links= list()


    def write_captions_to_excel_file(self, i):
        print(f"Saving DataFrame {i}")
        mydict1= {}
        mydict1['post_link']= self.post_link
        mydict1['Profile_Link']= self.profile_name
        mydict1['profile_headline']= self.profile_headline
        mydict1['likes_count']= self.likes_count
        mydict1['comments_count']= self.comments_count
        mydict1['post_content']= self.post_content
        elem = pd.DataFrame(mydict1)
        elem.to_csv(f'Data_New/comments_post_data_{i}.csv', index=False)
        mydict2= {}
        mydict2['comment_post_link']= self.comment_post_link
        mydict2['comment_content']= self.comment_content
        mydict2['comment_likes_counts']= self.comment_likes_counts
        mydict2['like_names']= self.like_names
        mydict2['like_headlines']= self.like_headlines
        mydict2['like_profile_links']= self.like_profile_links
        mydict2['comment_reply_counts']= self.comment_reply_counts
        mydict2['comments_replies_content']= self.comments_replies_content
        mydict2['comments_replies_names']= self.comments_replies_names
        mydict2['comments_replies_headlines']= self.comments_replies_headlines
        mydict2['comments_replies_links']= self.comments_replies_links
        elem = pd.DataFrame(mydict2)
        elem.to_csv(f'Data_New/comments_likes_data_{i}.csv', index=False)
        self.instantiate_varibales()
        gc.collect()

    def naviagte_posts(self):
        dump_df= pd.read_csv("Comments_new.csv")
        unique_post= list(dump_df.Link.unique())
        for i in range(120, len(unique_post)):
            print(f"{i+1} out of {len(unique_post)}")
            print(f"{unique_post[i]}------->")
            try:
                self.driver.get(unique_post[i])
            except Exception:
                continue
                pass
            self.link= unique_post[i]
            self.post_link.append(unique_post[i])
            sleep(10)
            self.get_data()
            if (i+1)% 10 == 0:
                self.write_captions_to_excel_file(((i+1)//10) + 60)
        sleep(10)

    def get_data(self):
        try:
            profile_name= self.driver.find_element_by_xpath('//span[@class="feed-shared-actor__title"]//span[@dir= "ltr"]').get_attribute('textContent')
            self.profile_name.append(profile_name)
        except Exception:
            self.profile_name.append('NA')
            pass
        sleep(1)

        try:
            profile_headline= self.driver.find_element_by_xpath('//div[@class="truncate feed-shared-text-view white-space-pre-wrap break-words ember-view"]/span').get_attribute('textContent')
            self.profile_headline.append(profile_headline)
        except Exception:
            self.profile_headline.append('NA')
            pass
        sleep(1)
        try:
            likes_count= self.driver.find_element_by_xpath('//span[@class="v-align-middle social-details-social-counts__reactions-count"]').get_attribute('textContent')
            self.likes_count.append(likes_count)
        except Exception:
            self.likes_count.append('NA')
            pass
        sleep(1)

        try:
            comments_count= self.driver.find_element_by_xpath('//li[@class="social-details-social-counts__item social-details-social-counts__comments"]/button/span').get_attribute('textContent')
            self.comments_count.append(comments_count)
        except Exception:
            self.comments_count.append('NA')
            pass
        sleep(1)

        try:
            post_content= self.driver.find_element_by_xpath('//div[@class="feed-shared-text relative feed-shared-update-v2__commentary ember-view"]')
            h = HTML2Text()
            h.ignore_links = True
            self.post_content.append(h.handle(post_content.get_attribute('innerHTML')))
        except Exception:
            self.post_content.append('NA')
            pass
        sleep(1)
        for j in range(10):
            try:
                more_comments = self.driver.find_element_by_xpath('//button[@data-control-name= "more_comments" ]')
                more_comments.click()
                sleep(7)
                print(f"Click Number {j+1}.....")
            except Exception:
                pass
        for j in range(10):
            try:
                more_replies = self.driver.find_element_by_xpath('//button[@data-control-name="more_replies"]')
                more_replies.click()
                sleep(7)
                print(f"Click Number {j+1}.....")
            except Exception:
                pass
        sleep(3)
        try:
            h= HTML2Text()
            h.ignore_links =True
            comment_content= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../../../../../div[@class="comments-comment-item-content-body" or @class="comments-reply-item-content-body"]/div/div/p')
            comment_content= [h.handle(content.get_attribute('innerHTML')) for content in comment_content]
            self.comment_content.extend(comment_content)
        except Exception:
            comment_content= ['NA']
            self.comment_content.extend(['NA'])
            pass
        sleep(2)
        print(f'comment_content : {len(self.comment_content)}')
        self.comment_post_link.extend([self.link] * len(comment_content))
        print(f'comment_post_link : {len(self.comment_post_link)}')
        try:
            h= HTML2Text()
            h.ignore_links =True
            likes= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../div[@class="comments-comment-social-bar__action-group"]')
            likes= [h.handle(like.get_attribute('innerHTML')) for like in likes]
            like= [re.search(r'\d+', like) for like in likes[0::2]]
            for i in range(len(like)):
                if like[i] != None:
                    like[i] = int(like[i].group(0))
                else:
                    like[i]= 0
            comment= [re.search(r'\d+', like) for like in likes[1::2]]
            for i in range(len(comment)):
                if comment[i] != None:
                    comment[i] = int(comment[i].group(0))
                else:
                    comment[i]= 0
            self.comment_likes_counts.extend(like)
            self.comment_reply_counts.extend(comment)
        except Exception:
            self.comment_likes_counts.extend(['NA'])
            self.comment_reply_counts.extend(['NA'])
            pass
            sleep(2)
        print(f'comment_likes_counts : {len(self.comment_likes_counts)}' )
        print(f'comment_reply_counts : {len(self.comment_reply_counts)}' )
        sleep(2)
        try:
            self.driver.execute_script('window.scrollTo(0, 0);')
            like_btn = self.driver.find_elements_by_xpath('//a[@href="/in/prudhvip/" and @class="tap-target comments-post-meta__actor-link ember-view"]/../..//div[@class="comments-comment-social-bar__action-group"]/button[@class="comments-comment-social-bar__likes-count hoverable-link-text"]')
            sleep(2)
            profilename= list()
            headline= list()
            profilelinks= list()
            temp_count= [num for num in like if num]
            for i,btn in enumerate(like_btn):
                btn.click()
                sleep(5)
                try:
                    no_of_scrolls = int(temp_count[i]/4)
                    print(no_of_scrolls)
                    eula = self.driver.find_element_by_xpath('//ul[@class="feed-shared-likers-modal__actor-list actor-list ember-view"]')
                    for value in range(no_of_scrolls):
                        self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', eula)
                        self.driver.execute_script('arguments[0].scrollBy(0,-250)', eula)
                        sleep(3)
                except Exception:
                    pass
                names= self.driver.find_elements_by_xpath('//h3[@class="name"]')
                names= [name.get_attribute('textContent') for name in names]
                profilename.append(names)

                headlines= self.driver.find_elements_by_xpath('//p[@class="headline"]')
                headlines= [headline.get_attribute('textContent') for headline in headlines]
                headline.append(headlines)

                links= self.driver.find_elements_by_xpath('//a[@data-control-name="like_actor"]')
                links= [link.get_attribute("href") for link in links]
                profilelinks.append(links)

                close_btn= self.driver.find_element_by_xpath('//button[@class="artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view"]')
                close_btn.click()
                sleep(2)
            n_profilename=[]
            j=0
            for i in range(len(like)):
                if like[i]!= 0:
                    n_profilename.append(profilename[j])
                    j= j + 1
                else:
                    n_profilename.append('NA')

            n_headlines=[]
            j=0
            for i in range(len(like)):
                if like[i]!= 0:
                    n_headlines.append(headline[j])
                    j= j + 1
                else:
                    n_headlines.append('NA')

            n_profilelinks=[]
            j=0
            for i in range(len(like)):
                if like[i]!= 0:
                    n_profilelinks.append(profilelinks[j])
                    j= j + 1
                else:
                    n_profilelinks.append('NA')
            self.like_names.extend(n_profilename)
            self.like_headlines.extend(n_headlines)
            self.like_profile_links.extend(n_profilelinks)
        except Exception:
            self.like_names.extend(['NA'])
            self.like_headlines.extend(['NA'])
            self.like_profile_links.extend(['NA'])
            pass
        print(f'like_names : {len(self.like_names)}' )
        print(f'like_headlines : {len(self.like_headlines)}' )
        print(f'like_profile_links : {len(self.like_profile_links)}' )
        sleep(2)
        try:
            comments_replies_content= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../../../../..//article//div[@class="comments-reply-item-content-body"]')
            comments_replies_content= [comment.get_attribute('innerHTML') for comment in comments_replies_content]
            comments_replies_content= [h.handle(content) for content in comments_replies_content]
            comment_replies= []
            previous_element=0
            for com in comment:
                if com!=0:
                    comment_replies.append(comments_replies_content[previous_element:(com+previous_element)])
                    previous_element= com
                else:
                    comment_replies.append(['NA'])
            self.comments_replies_content.extend(comment_replies)
        except Exception:
            self.comments_replies_content.extend(['NA'])
        print(f'comment_HTML : {len(self.comments_replies_content)}')
        try:
            comments_replies_names= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../../../../..//article//a[@class="comments-post-meta__profile-link t-16 t-black t-bold tap-target ember-view"]//span[@class="hoverable-link-text"]')
            comments_replies_names= [comment.get_attribute('textContent') for comment in comments_replies_names]
            comment_replies= []
            previous_element=0
            for com in comment:
                if com!=0:
                    comment_replies.append(comments_replies_names[previous_element:(com+previous_element)])
                    previous_element= com
                else:
                    comment_replies.append(['NA'])
            self.comments_replies_names.extend(comment_replies)
        except Exception:
            self.comments_replies_names.extend(['NA'])
        print(f'comments_replies_names : {len(self.comments_replies_names)}' )
        try:
            comments_replies_headlines= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../../../../..//article//a[@data-control-name="reply_actor"]/h3/span[@class="comments-post-meta__headline t-12 t-black--light t-normal"]')
            comments_replies_headlines= [comment.get_attribute('textContent') for comment in comments_replies_headlines]
            comment_replies= []
            previous_element=0
            for com in comment:
                if com!=0:
                    comment_replies.append(comments_replies_headlines[previous_element:(com+previous_element)])
                    previous_element= com
                else:
                    comment_replies.append(['NA'])
            self.comments_replies_headlines.extend(comment_replies)
        except Exception:
            self.comments_replies_headlines.extend(['NA'])
        print(f'comments_replies_headlines : {len(self.comments_replies_headlines)}')
        try:
            comments_replies_links= self.driver.find_elements_by_xpath('//button[@aria-label="Like Prudhvi Potuganti’s comment"]/../../../../../..//article//a[@class="tap-target comments-post-meta__actor-link ember-view"]')
            comments_replies_links= [comment.get_attribute('href') for comment in comments_replies_links]
            comment_replies= []
            previous_element=0
            for com in comment:
                if com!=0:
                    comment_replies.append(comments_replies_links[previous_element:(com+previous_element)])
                    previous_element= com
                else:
                    comment_replies.append(['NA'])
            self.comments_replies_links.extend(comment_replies)
        except Exception:
            self.comments_replies_links.extend(['NA'])
        print(f'comments_replies_links : {len(self.comments_replies_links)}')
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
