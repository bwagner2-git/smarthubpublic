from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


class backgroundGenerator():
    def __init__(self):
        self.img=None

    def getColors(self, numColors=5):
        clt=KMeans(n_clusters=numColors)
        clt.fit(self.img.reshape(-1,3))
        return(clt.cluster_centers_)

    def generate(self,img):
        self.img=cv2.cvtColor(cv2.imread(img),cv2.COLOR_BGR2RGB)
        try:
            colors=self.getColors(3)
        except:
            colors=self.getColors(numColors=1)
        colors=colors/255
        print(colors)
        color1=colors[0]
        if len(colors)>1:
            color2=colors[1]
        else:
            color2=colors[0]
        brightness1=.21*color1[0]+.72*color1[1]+.07*color1[2]
        brightness2=.21*color2[0]+.72*color2[1]+.07*color2[2]
        if brightness2>brightness1:
            color1,color2=color2,color1
        # fig, ay = plt.subplots(figsize=(8, 5)
        
        fig, ay = plt.subplots(figsize=(8, 8))

        for y in range(301):
            ay.axhline(y, color=mpl.colors.to_hex((1-y/301)*color1 + y/301*color2) , linewidth=4) 

        plt.axis('off')
        plt.margins(0,0)
        # plt.show()
        plt.savefig(fname='backgroundGradient.png',bbox_inches='tight',pad_inches=0)
    

# a=backgroundGenerator()
# a.generate('./pennybacker/4.png')
# a=backgroundGenerator()
# # for i in a.getColors
# #     print(i)
#     # plt.imshow([i])
#     # plt.show()

# # plt.imshow([a.getColors()[0][0],a.getColors()[0][1],a.getColors()[0][2]])
# # plt.imshow(a.getColors())
# # plt.show()
# for i in range(1):
#     a.generate('album.jpg')