# -*- coding: utf-8 -*-

# @project :xueqiu
# @File    : xueqiu.py
# @Date    : 2020-12-10-19
# @Author  : XRL


import requests
from parsel import Selector
import time
import json
import pymysql
import random



SH_list_URL = 'https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0'
time_stamp_13 = round(time.time() * 1000)
time_stamp_10 = int(time.time())
uuid_list = ['1337025461112426496', '1337038882990084096', '1337040898676117504', '1337040991898722304',
             '1337041113181212672']
#返回 公司名：股票代码 形式的字典
def get_name_code():
    cookie = 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=d314v1z8vf; __utmz=1.1607580577.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); remember=1; xq_a_token=9b54976b6562377d52ef817b219dc5ca129dee66; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjUwOTQyMzkzNDcsImlzcyI6InVjIiwiZXhwIjoxNjEwMTc3ODE5LCJjdG0iOjE2MDc1ODU4MTk3MjgsImNpZCI6ImQ5ZDBuNEFadXAifQ.BsIAal27yi8G4PTwIF4YGdRkGdDhVmb0z_K3P8aFonqw24StxuHZoyYz4pNcm6Ieeqko1Q-8yTaBsP-xNIk4yiHYMdbp6cmTR27lNyIaYCwlh9cqNzKSSX-59MQ1zV78zCBHqLuj8NzPw1QWTubI6N96ZyPR6X8Up7ZwBJGmZ104jYndhStIcTz2ytzHGDPD2lPteVF_VJjwAKm6xFGIyxUQz52O2yp1r8nUtJ-M-NDRzfOSMIIvI36KXbrMnsnLKB65uhs0H5nnQVcyPPvEXKK_eNwFZlVFDbw7eM81lEINDbGZ4nIG84tg3hqFoxUPZkaCygsqBn5Qg8A4y1bXNw; xqat=9b54976b6562377d52ef817b219dc5ca129dee66; xq_r_token=eccccbce5bf740b0e0471cdc2a25e606f8cb18ee; xq_is_login=1; u=5094239347; bid=60286158dbfe89941547796f000d348d_kiij3jh5; acw_tc=2760821516075992440948025e46d25ad80f793bd285221b324be6a0e90702; __utma=1.209470197.1607580577.1607585832.1607599255.3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1607594495,1607594502,1607599244,1607599763; __utmc=1; __utmt=1; __utmb=1.5.10.1607599255; Hm_lpvt_1db88642e346389874251b5a1eded6e3={time}'.format(time=time_stamp_10)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'cache-control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'xueqiu.com',
        'Referer': 'https://xueqiu.com/hq',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'

    }
    co_dict = {}
    for i in range(1,5):
        url = 'https://xueqiu.com/service/v5/stock/screener/quote/list?page={page}&size=90&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_={time13}'.format(page=i,time13=time_stamp_13)
        res = requests.get(url=url,headers=headers,timeout=(2,7))
        data = json.loads(res.text)
        for i in data['data']['list']:
            co_dict[i['name']] = i['symbol']
        time.sleep(2)
    return co_dict

#将今天的评论写入文件
def comment(code):
    cookie = 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=d314v1z8vf; __utmz=1.1607580577.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); remember=1; xq_a_token=9b54976b6562377d52ef817b219dc5ca129dee66; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjUwOTQyMzkzNDcsImlzcyI6InVjIiwiZXhwIjoxNjEwMTc3ODE5LCJjdG0iOjE2MDc1ODU4MTk3MjgsImNpZCI6ImQ5ZDBuNEFadXAifQ.BsIAal27yi8G4PTwIF4YGdRkGdDhVmb0z_K3P8aFonqw24StxuHZoyYz4pNcm6Ieeqko1Q-8yTaBsP-xNIk4yiHYMdbp6cmTR27lNyIaYCwlh9cqNzKSSX-59MQ1zV78zCBHqLuj8NzPw1QWTubI6N96ZyPR6X8Up7ZwBJGmZ104jYndhStIcTz2ytzHGDPD2lPteVF_VJjwAKm6xFGIyxUQz52O2yp1r8nUtJ-M-NDRzfOSMIIvI36KXbrMnsnLKB65uhs0H5nnQVcyPPvEXKK_eNwFZlVFDbw7eM81lEINDbGZ4nIG84tg3hqFoxUPZkaCygsqBn5Qg8A4y1bXNw; xqat=9b54976b6562377d52ef817b219dc5ca129dee66; xq_r_token=eccccbce5bf740b0e0471cdc2a25e606f8cb18ee; xq_is_login=1; u=5094239347; bid=60286158dbfe89941547796f000d348d_kiij3jh5; Hm_lvt_1db88642e346389874251b5a1eded6e3=1607594495,1607594502,1607599244,1607599763; __utmc=1; __utma=1.209470197.1607580577.1607599255.1607608382.4; acw_tc=2760820e16076107543134028efe53b6f280448d47465d3be0ce01c2f6ac46; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3={time}'.format(time=time_stamp_10)
    headers ={
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'cache-control': 'no-cache',

        'Cookie':cookie,
        'elastic-apm-traceparent':'00-7491e7adae6a02888d541fac9acff2d3-f42d73e90e40a280-00',
        'Host':'xueqiu.com',
        'Referer':'https://xueqiu.com/S/'+code,
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    for i in range(1,5):
        url = 'https://xueqiu.com/query/v1/symbol/search/status?u=5094239347&&uuid='+random.choice(uuid_list)+'&count=10&comment=0&symbol='+code+'&hl=0&source=all&sort=&page='+str(i)+'&q=&type=82&session_token=null&access_token=9b54976b6562377d52ef817b219dc5ca129dee66={time}'.format(time=time_stamp_13)
        res = requests.get(url=url,headers=headers,timeout=(2,7))
        data = json.loads(res.text)

        for i in data['list']:
            with open('comment.txt', 'a', encoding='utf-8')as f:
                if '今天' or '前' in i['timebefore']:
                    f.write('描述：'+i['description']+'\n'+'\n'+'正文：'+i['text']+'\n'+'\n')
                    print("评论+1")
            time.sleep(2)

def main():
    co_dict = get_name_code()
    for i in co_dict.keys():
        code = co_dict[i]
        comment(code)
    print('结束')

if __name__ == '__main__':
    main()