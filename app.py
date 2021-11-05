# from PySimpleGUI.PySimpleGUI import Titlebar, Window, theme_background_color
# from pvporcupine.porcupine import Porcupine
from tkinter import font
from matplotlib.pyplot import margins
from backGround import backgroundGenerator
import PySimpleGUI as sg
from jarvis import jarvis
from music import musicPlayer
import threading
import time
import os
from PIL import Image
import random
from multiprocessing import Process

os.system("xrandr | grep \* | cut -d' ' -f4 > resolution.txt") ##get screen size
###do not know what the gamma is for the output default if things go wrong check the text file to see if something is going wrong
f=open('resolution.txt','r')
screenSize=f.readlines()[0].replace('\n','').split('x')
screenSize[0]=int(screenSize[0])
screenSize[1]=int(screenSize[1])

secret=open('/home/ubuntu/spotSecret.txt','r')
secret=secret.read().replace('\n','')

sg.Window._move_all_windows=True
def makeWindow(dim,musicPlayer):
    try:
        display=musicPlayer.info()
        generator=backgroundGenerator()
        # generator.generate('album.png')
        p=Process(target=backgroundGenerator.generate,args=(generator,'album.png'))
        p.start()
        while p.is_alive():
            time.sleep(1)
        p.terminate()
        background=Image.open('backgroundGradient.png')
        background=background.resize((dim[0],int(dim[1]*.8)))
        albumArt=Image.open('album.png')
        width=albumArt.width
        height=albumArt.height
        ratio=height/width
        albumArt=albumArt.resize(((int(dim[0]*.3),int(ratio*(dim[0]*.3)))))
        background.paste(albumArt,(int(background.width*.5-.5*albumArt.width),int(background.height*.5-.5*albumArt.height)))
        background.save('finalBackground.png')
        col=[[sg.Button(image_filename='./icons/previous.png',image_size=(100,100),image_subsample=12,key='previous',button_color='#21ADA8'),sg.Button(image_filename='./icons/playPause.png',image_size=(100,100),image_subsample=8,key='pausePlay',button_color='#21ADA8'),sg.Button(image_filename='./icons/next.png',image_size=(100,100),image_subsample=12,key='next',button_color='#21ADA8')],[sg.Text(text=display,justification='center',font=('Z003',50),background_color='#21ADA8')]]
        layout = [ [sg.Image(filename='finalBackground.png',pad=(0,0))], 
                # [sg.Text('Some text on Row 1')],
                # [sg.Text('Enter something on Row 2'), sg.InputText()],
                # [sg.Button('Ok'), sg.Button('Exit',key="Exit")],
                [sg.Column(col,element_justification='c',vertical_alignment='center',justification='center',background_color='#21ADA8')]]
        window=sg.Window("welcome",layout,size=(dim[0],dim[1]),no_titlebar=True,grab_anywhere=True,resizable=True,disable_close=False,disable_minimize=False,keep_on_top=False,finalize=True,margins=(0,0),element_padding=(0,0),background_color='#21ADA8')
        return window
    except:
        choice=str(random.randint(1,4))
        background=Image.open('./pennybacker/'+choice+'back.png')
        background=background.resize((dim[0],int(dim[1]*.8)))
        albumArt=Image.open('./pennybacker/'+choice+'.png')
        width=albumArt.width
        height=albumArt.height
        ratio=height/width
        albumArt=albumArt.resize(((int(dim[0]*.3),int(ratio*(dim[0]*.3)))))
        background.paste(albumArt,(int(background.width*.5-.5*albumArt.width),int(background.height*.5-.5*albumArt.height)))
        background.save('finalBackground.png')
        col=[[sg.Text("Welcome to the Lake!",justification='center')]]
        layout = [ [sg.Image(filename='finalBackground.png',pad=(0,0))],
                # [sg.Text("Welcome to the lake!",text_color='black',font=('Z003',50),justification='center',size=(dim[0],1),background_color='#21ADA8')], [sg.Button('Exit',key="Exit")]
                # ]
                [sg.Text("Welcome to the lake!",text_color='black',font=('Z003',50),justification='center',size=(dim[0],1),background_color='#21ADA8')]
                ]
        window=sg.Window("welcome",layout,size=(dim[0],dim[1]),no_titlebar=True,grab_anywhere=True,resizable=True,disable_close=False,disable_minimize=False,keep_on_top=False,finalize=True,background_color='#21ADA8',margins=(0,0),element_padding=(0,0))
        return window

player=musicPlayer(secret)
jarv=jarvis(player)
uweh=threading.Thread(target=jarv.run,args=(jarv,))
uweh.start()
print(jarv.minecraft)


# sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.



# Create the Window
# window = sg.Window('Music', layout,size=(800,400),keep_on_top=True,no_titlebar=True,element_justification='c',finalize=True)
# window = sg.Window('Welcome to the lake!',layout,size=(800,400), keep_on_top=False,disable_minimize=False,disable_close=False,grab_anywhere=True,location=(0,0),titlebar_icon=r'/home/ubuntu/smartHub/icons/waves.png',modal=False,use_custom_titlebar=True)
# window=sg.Window("welcome",layout,size=(800,800),no_titlebar=True,grab_anywhere=True,resizable=True,disable_close=False,disable_minimize=False,keep_on_top=False)
window=makeWindow(screenSize,player)
# window=sg.Window("Welcome to the Lake!",layout,size=(800,800),icon='/home/ubuntu/smartHub/icons/waves.png',titlebar_background_color=sg.theme('light blue'))

# Titlebar=[]
# window.override_custom_titlebar(1)
# Event Loop to process "events" and get the "values" of the inputs

currentSong=None
# restart=False
while True:
    # if restart:
    #     jarv=jarvis(player)
    #     print("new jarv with kill "+ str(jarv.kill))
    #     uweh=threading.Thread(target=jarvis.run,args=(jarv,True))
    #     uweh.start()
    #     restart=False
    event, values = window.read(timeout=5000)
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cancel
        break
    # print('You entered ', values[0])
    if event=='previous':
        player.previous()
    if event=='next':
        player.next()
    if event=='pausePlay':
        player.playPause()

    if jarv.exit==True:
        break
    if jarv.minecraft==True:
        window.close()
        while jarv.minecraft:
            pass
        window=makeWindow(screenSize,player)
    try:
        check=player.currentSong()
        if check and check!=currentSong and check.lower() != 'we show up':
            print(repr(check))
            print('here')
            # jarv.kill=True
            currentSong=check
            print(currentSong)
            window1=window
            window=makeWindow(screenSize,player) 
            window1.close()
            # restart=True
            time.sleep(5)
            # jarv.kill=False
    except:
        print('there was an error')
        pass
window.close()
