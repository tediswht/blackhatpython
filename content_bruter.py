from queue import Queue
import urllib.request
import threading

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "C:\\tmp\\all.txt" #需自行调整字典路径
resume = None
user_agent = "Mozilla/5.0 (X11:Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):
    fd =open(wordlist_file,"r")
    raw_words = fd.readlines()
    fd.close()
    found_resume = False
    words = Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from :%s"%resume)
        else:
            words.put(word)
    return words
##实际执行过程中出现中断才需使用

def dir_bruter(word_queue,extension=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list=[]
        if "." not in attempt: #区分文件or路径
            attempt_list.append("/%s/"%attempt)
        else:
            attempt_list.append("/%s"%attempt)
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s"%(attempt,extension))
        for brute in attempt_list:
            url = "%s%s"%(target_url,urllib.request.quote(brute))
            try:
                headers={}
                headers["User-Agent"]=user_agent
                req = urllib.request.Request(url,headers=headers)
                res = urllib.request.urlopen(req)
                if len(res.read()):
                    print("[%d]==>%s"%(res.code,url))
            except urllib.error.URLError as e:
                if hasattr(e,'code') and e.code !=404:
                    print("!!!%d==>%s"%(e.code,url))
                pass

word_queue=build_wordlist(wordlist_file)
extensions = [".php",".bak",".orig",".inc"]
for i in range(threads):
    t = threading.Thread(target = dir_bruter,args=(word_queue,extensions))
    t.start()
