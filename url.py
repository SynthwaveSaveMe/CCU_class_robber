#-*- coding: utf-8 -*-
import time
from datetime import datetime
from requests import post
from requests import get,utils
from requests import Timeout
from requests import ConnectionError
import sys
import json
import cv2
import numpy as np
import webbrowser
json_file_path = "img.json"
json_file = open(json_file_path, 'r')
str_hash = json.load(json_file)
def get_cookie():
    cookie_url = "https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/login.php"
    while 1:
        try:
            response = get(cookie_url,timeout=7)
            break
        except:
            print("get cookie wrong")
            time.sleep(5)
            continue
    cookie = utils.dict_from_cookiejar(response.cookies)
    return cookie
def recap():
    while 1:
        #獲取驗證碼圖片
        cookie = get_cookie()
        try:
            r = get('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/captcha.php',cookies=cookie)
            # print(r.cookies.get_dict())
        except:
            continue
        img = cv2.imdecode(np.frombuffer(r.content, np.uint8), cv2.IMREAD_COLOR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res,img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        start = datetime.now()

        # json_file_path = "img.json"

        # # 比對圖片破解
        # with open(json_file_path, 'r') as json_file:
        #     str_hash = json.load(json_file)
        text2=''
        N=0
        while(N<60):
            x = 3+N # +9N
            y = 6
            # 裁切區域的長度與寬度
            w = 8
            h = 12
            # 裁切圖片
            crop_img = img[y:y+h, x:x+w]
            # cv2.imwrite('crop.jpg', crop_img)
            # cv2.imwrite('output.jpg', img)
            string=''
            for j in range(12):
                for k in range(8):
                    if crop_img[j][k]==0:
                        string=string+'0'
                    else:
                        string=string+'1'
            num=int(string, 2)
            if str(num) in str_hash:
                text2=text2+str_hash[str(num)]
                N=N+9
            else:
                N=N+1
        #傳送驗證碼
        d = {'captcha_input': text2}
        url = 'https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/verify_captcha.php'
        try:
            r = post(url, data=d, timeout=5,cookies=cookie)
            print(r.text)
            if r.text!="success":
                print(text2)
        except:
            continue
        return text2,cookie
def submit(k,id,password,select_num,sleep_time):
    t=k
    while True:
        try:
            time.sleep(t*sleep_time)
            cookie = {"PHPSESSID":"omk1nfnabo7haa6c880rcfgs10"}
            data = [
                    {'session_id':'','dept':'I001','SelectTag':'1','course':'7407014_01','7407014_01':'3'}
                    #(30)人際
                    ]
            url = 'https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi'
            url_log = 'https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/bookmark.php'
            url_log_out = 'https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/logout.php'
            # cap,cookie = recap()
            data_log = {"version":"0",
                    "id":id,
                    "password":password,
                    # "captcha_input":cap,
                    "m":"0"}
            data_log_out = {'session_id':''}
            while True:
                    start = datetime.now()
                    try:
                        r = post(url_log, data = data_log,timeout=7,cookies=cookie)
                    except Timeout:
                        print('log in Timeout ')
                        time.sleep(10)
                        continue
                    except ConnectionError:
                        print('log in ConnectionError ')
                        time.sleep(20)
                        continue
                    except:
                        print('log in wrong ')
                        time.sleep(30)
                        continue
                    # if k==0:
                    #     print(r.text)
                    line = r.text[224:264]
                    index = line.find('"')
                    data[select_num]['session_id'] = line[:index]
                    data_log_out['session_id'] = line[:index]
                    if line[:index].find('/')!=-1 or line[:index].find("\n")!=-1:
                        print('session wrong')
                        break #刪
                        time.sleep(90)
                        continue
                    print('已登入網址:')
                    print('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/bookmark.php?session_id='+line[:index]+'&m=0&e=0')
                    webbrowser.open('https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/bookmark.php?session_id='+line[:index]+'&m=0&e=0')
                    break #刪
        except Exception as e:
            print(e)
            print('something wrong ')
            t=k*1.1
            pass
        break #刪


if  __name__ == '__main__' :
    account = open('account.json','r')  #請先創一個account.json的檔案，內容如右邊所示 {"id" : "你的學號","password" : "你的密碼"}
    f =  account.read()                 #避免傳這個py檔案的時候，導致密碼洩漏
    id_pwd = json.loads(f)
    id_list = list(id_pwd.keys())
    print(id_list)
    sleep_time = 0.1
    k=0
    for id in id_list:
        password = id_pwd[id]
        submit(k,id,password,0,sleep_time)
        k=k+1