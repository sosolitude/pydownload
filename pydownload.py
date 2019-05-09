#coding=utf-8
#import urllib.request
import requests
import re
import os
import threadpool
import threading
from bs4 import BeautifulSoup 

MAX_THREADS=10

url="https://mirrors.tuna.tsinghua.edu.cn/centos/7.6.1810/atomic/x86_64/"
#url="https://mirrors.tuna.tsinghua.edu.cn/centos/7.6.1810/atomic/x86_64/Packages/"
dir="packages/"

def fetch_web(url,savedir,r=True):
    dir_check(savedir)
    req=requests.get(url)
    bs=BeautifulSoup(req.text,"lxml")
    links=bs.find_all('a')
    threads=[]
    for each in links:
        link=each.get('href')
        print(link)
        if link=="../":
            continue
        if link.endswith("/"):
            if r:
                savedir=savedir+link
                fetch_web(url+link,savedir)
            else:
                print(url+link)
                #TODO:save as a file
                continue         
        else :
            print("get file:",url+link)
            #single process
            #get_file(url+link,savedir)
            t = threading.Thread(target=get_file,args=(url+link,savedir))
            threads.append(t)

    for t in threads:
         t.start()
         while True:
             if len(threading.enumerate())<MAX_THREADS :
                 break
            
def get_file(url,savedir):
    r = requests.get(url)
    filename=url.split("/")[-1]
    print(filename)
    savefile=savedir+filename
    print(savefile)
    with open(savefile, 'wb') as f:  
        f.write(r.content)

def dir_check(savedir):
    if os.path.exists(savedir):
        return
    else:
        os.mkdir(savedir)
    
def url_check():
    pass

fetch_web(url,savedir=dir)

#TODO:use getopt() to process args in main function.

