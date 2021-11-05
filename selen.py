from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# opts=Options()
# opts.binary_location='/snap/bin/chromium'

# # # driver=webdriver.Chrome(executable_path='var/lib/snapd/snaps')
# # # driver=webdriver.Chrome(executable_path='/snap/bin/chromium')
# driver=webdriver.Chrome(chrome_options=opts, executable_path='/home/ubuntu/drivers/chromedriver')
# # driver=webdriver.Firefox()

# driver.get('https://google.com')
class music():
    def __init__(self):
        self.driver=webdriver.Chrome('/home/ubuntu/drivers/chromium.chromedriver')
        # self.driver.get('https://music.youtube.com')
        # search=self.driver.find_element_by_id('input')
        # search.send_keys('u 2 luv')
        # search.send_keys(Keys.RETURN)
        # self.driver.get('https://accounts.google.com')
        # email=self.driver.find_element_by_id('identifierId')
        # email.send_keys('raspgoat1@gmail.com')
    def play(self,song):
        self.driver.get('https://music.youtube.com/search?q='+song.replace(' ','+'))
        play=self.driver.find_elements_by_id("play-button")
        play[1].click()
a=music()
a.play('u 2 love')