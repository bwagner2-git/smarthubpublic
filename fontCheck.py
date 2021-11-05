from jarvdebug import dumbJarvis
from music import musicPlayer

secret=open('/home/ubuntu/spotSecret.txt','r')
secret=secret.read().replace('\n','')
a=musicPlayer(secret=secret)
jarv=dumbJarvis(musicPlayer=a)
jarv.run()