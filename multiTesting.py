from multiprocessing import Process
from backGround import backgroundGenerator
a=backgroundGenerator()
p=Process(target=backgroundGenerator.generate,args=(a,'album.png'))
p.start()
while p.is_alive():
    print('running')
print('done')
p.terminate()