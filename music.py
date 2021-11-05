from selenium import webdriver
# import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


# opts=Options()
# opts.binary_location='/snap/bin/chromium'

# # # driver=webdriver.Chrome(executable_path='var/lib/snapd/snaps')
# # # driver=webdriver.Chrome(executable_path='/snap/bin/chromium')
# driver=webdriver.Chrome(chrome_options=opts, executable_path='/home/ubuntu/drivers/chromedriver')
# # driver=webdriver.Firefox()

# secret=open('/home/ubuntu/spotSecret.txt','r')
# secret=secret.read().replace('\n','')
class musicPlayer():
    def __init__(self,secret):
        self.driver=webdriver.Chrome('/home/ubuntu/drivers/chromium.chromedriver')
        self.spotify=spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='57bcaf6958f8456a82c03183367fe768',client_secret=secret))
        self.playing=False
    def play(self,song):
        self.driver.get('https://music.youtube.com/search?q='+song.replace(' ','+'))
        try:
            alert=self.driver.switch_to.alert
            alert.accept()
        except:
            pass
        play=self.driver.find_elements_by_id("play-button")
        count=0
        while len(play)==0 and count<=20:
            play=self.driver.find_elements_by_id("play-button")
            count+=1
            time.sleep(1)            
        print(play)
        play[1].click()
        self.playing=True
    def next(self):
        next=self.driver.find_element_by_class_name("next-button")
        next.click()
    def previous(self):
        next=self.driver.find_element_by_class_name("previous-button")
        next.click()
        time.sleep(1)
        next.click()
    def playPause(self):
        next=self.driver.find_element_by_class_name("play-pause-button")
        next.click()
        self.playing=not(self.playing) #maybe move to front
    def currentSong(self):
        try:
            current=self.driver.find_elements_by_tag_name('span.advertisement.style.scope.ytmusic-player-bar')[0].text
            return None
        except:    
            current=self.driver.find_elements_by_tag_name('yt-formatted-string.title.style-scope.ytmusic-player-bar')[0].text
            return current
    # def artist(self):
    #     # try: 
    #     artist=self.driver.find_elements_by_tag_name('a.yt-simple-endpoint.style-scope.yt-formatted-string')
    #     return str(len(artist))
    #     # except:
        #     return 'asldjf'
    def info(self):
        if self.currentSong():
            try:
                song=self.spotify.search(self.currentSong(),limit=1)
            except:
                return None
            with requests.Session() as session:
                try:
                    r=session.get(song['tracks']['items'][0]['album']['images'][1]['url'])
                except:
                    r=session.get(song['tracks']['items'][0]['album']['images'][0]['url'])
                file=open('album.png','wb')
                file.write(r.content)
                file.close()
            #image try images 1 except images 0 song[tracks][items][0][images][1][url]
            artists=''
            for artist in song['tracks']['items'][0]['artists']:
                artists+=artist['name']+' '
            return self.currentSong()+' by '+artists
        else:
            return None
# a=musicPlayer(secret=secret)
# a.play('u 2 love')
# while(True):
#     time.sleep(2)
#     print(a.currentSong())
# while True:
#     time.sleep(15)
#     while True:
#         time.sleep(2)
#         # try:
#         print(a.currentSong()+a.artist())
#         # except:
#         #     pass