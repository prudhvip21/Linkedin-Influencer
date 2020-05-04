def get_data(self):
    df= pd.read_csv('post_links.csv', index_col= False, header=None)
    post_links= df.iloc[:, 0].tolist()
    for link in post_links:
        link = 'www.linkedin.com/feed/update/' + link + '/'
        self.driver.get(link)
        sleep(5)
        #self.find_like()
        #sleep(3)
        #self.scroll_down()
        #sleep(3)


def scroll_down(self):
    try:
        for value in range(13):
            self.driver.execute_script('$("#data-test-modal").scrollTop($("#data-test-modal")[0].scrollHeight);')
            sleep(2)
    except Exception as e:
        self.error = True
        print(e)
        print('Some error occurred while trying to scroll down')
    sleep(5)


def find_like(self):
    like_button = self.driver.find_element_by_xpath('//button[@class="social-details-social-counts__count-value t-12 t-black--light t-normal hoverable-link-text"]')
    like_button.click()
    sleep(5)
