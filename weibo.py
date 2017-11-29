# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 20:27:21 2017

@author: mong
"""

import requests
from selenium import webdriver
import re
import time
import random



wd = webdriver.Chrome() #构建浏览器
loginUrl = 'http://www.weibo.com/login.php' 
wd.get(loginUrl) #进入登陆界面
wd.find_element_by_xpath('//*[@id="loginname"]').send_keys('******') #输入用户名
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input').send_keys('*******') #输入密码
wd.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click() #点击登陆
req = requests.Session() #构建Session
cookies = wd.get_cookies() #导出cookie
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value']) #转换cookies
#获取登陆用户uid    
wd.find_element_by_xpath('//*[@id="v6_pl_rightmod_myinfo"]/div/div/div[2]/ul/li[1]/a/strong').click() #点击我的关注  
time.sleep(1)
pat='action-data="fuid=(.*?)&amp'
fuid=re.compile(pat).findall(wd.page_source)
fuid
#获取第一页关注人列表
pat='action-data="uid=(.*?)&amp;'
atts=re.compile(pat).findall(wd.page_source)
atts=list(set(atts))
#创建用户关系网络，对用户进行连边
whole_net=[]
for att in atts:
    whole_net.append((fuid[0],att))
    
for num in range(1,50):
    #从my_atts里随机选择下一个用户作为目标获取其关注列表
    print('正在爬取第'+str(num)+'个用户的关注列表………………')
    fuid=random.choice(atts)
    #获取页数
    
    try:
        url_wb_follow = 'https://weibo.com/p/100505'+str(fuid[0])+'/follow?page=1'
        wd.get(url_wb_follow)
    except:
        print('未找到该用户，将跳过......')
    else:
        pat='page=(.*?)#Pl_Official_.*?\">'
        page=re.compile(pat).findall(wd.page_source)
        page=len(page)
    #获取每一页用户关注列表
    for i in range(2,page+1):  
        pat='uid=(.*?)&amp;'
        atts+=re.compile(pat).findall(wd.page_source)
        atts=list(set(atts))
        url_wb_follow = 'https://weibo.com/p/100505'+str(fuid[0])+'/follow?page='+str(i)    
        wd.get(url_wb_follow)                
    for att in atts:
        whole_net.append((fuid,att))
l=[]        
for link in whole_net:
    l.append(link[0])
    l.append(link[-1])
l=list(set(l))

import pandas as pd
dot=pd.Series(range(132),index=l) 

dot_net=[] 
for link in whole_net:
    link=list(link)
    link[0]=dot[link[0]]
    link[1]=dot[link[1]]
    dot_net.append((link[0],link[1]))
    

with open('E:\数据\weibo_dot_50.txt','w') as fh:
    for link in dot_net:
        link=str(link)
        link=link.replace('[','')
        link=link.replace(']','')
        link=link.replace('(','')
        link=link.replace(')','')
        link=link.replace("'",'')
        link=link.replace(",",'   ')
        fh.write(link+'\n')
