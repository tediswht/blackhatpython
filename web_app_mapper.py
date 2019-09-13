from queue import Queue
import threading
import os
import urllib.request

target = "http://ddfangmeng.ycway.cn/"
directory = "D:\Program Files (x86)\joomla"
filters = [".jpg",".gif",".png",".css"]

os.chdir(directory)

web_path = Queue()

for r,d,f in os.walk("."):
    for files in f:
        remote_path = "%s/%s"%(r,files)
        if remote_path.startswith("."):
            remote_path=remote_path[1:]
        if os.path.splitext(files)[1] not in filters:
            web_path.put(remote_path)

def test_remote():
    while not web_path.empty():
        path = web_path.get()
        url = "%s%s"%(target,path)
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
            content = response.read()
            print("[%d]==>%s"%(response.code,path))
            response.close()
        except urllib.error.URLError as error:
            pass

for i in range(5):
                  print("Spawning thread:%d" %i)
                  t=threading.Thread(target=test_remote)
                  t.start()
                  
