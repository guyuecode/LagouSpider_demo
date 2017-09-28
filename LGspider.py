#!/usr/bin/env python
#! _*_ coding:utf-8 _*_

import requests
import json
import time
import mysql.connector
import random

# 搜索的内容
search = "python"

def int_random():
    return random.randint(0, 9)
UA_list = [
            "Mozilla/5.0 ( ; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
           "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
           "Mozilla/5.0 (Windows NT 6.1; rv:1.9) Gecko/20100101 Firefox/4.0",
           "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.3 Safari/534.24",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.0 Safari/534.24",
           "Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.44 Safari/534.13",
           "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.19 Safari/534.13",
           "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0",
           "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
           "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10gin_lib.cc"
           ]


request_url = "https://www.lagou.com/jobs/positionAjax.json?city=上海&needAddtionalResult=false&isSchoolJob=0"
def get_job_json(url,pn,UA,search):
    headers = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "User-Agent":UA,
        "X-Requested-With":"XMLHttpRequest",
        "Referer":"https://www.lagou.com/jobs/list_%s?labelWords=&fromSearch=true&suginput="%search,
        "Host":"www.lagou.com"
    }
    respone = requests.post(request_url,headers=headers,data={'first': 'false', 'pn': pn,'kd':search}).content
    return respone

pageNO = 1
pn = 0
while pageNO != 0:
    pn += 1
    json_data = json.loads(get_job_json(request_url, pn, UA_list[int_random()],search))
    pageNO = json_data['content']["pageNo"]
    pageSize = json_data['content']['pageSize']
    job_data = json_data['content']['positionResult']['result']
    # 数据库连接
    conn = mysql.connector.connect(host='localhost', user='root', password='redhat', database='LagouSpider')

    if pageNO != 0:
        for PS in range(pageSize):
            id = job_data[PS]['positionId']
            JobTitle = job_data[PS]['positionName'].encode('utf-8')
            salary = job_data[PS]['salary'].encode('utf-8')
            education = job_data[PS]['education'].encode('utf-8')
            companyFullName = job_data[PS]['companyFullName'].encode('utf-8')
            try:
              cursor = conn.cursor()
              cursor.execute('insert into search_python_result_list (id, JobTitle, salary, education, companyFullName) values (%s, %s, %s, %s, %s)', [id, JobTitle, salary, education, companyFullName])
              conn.commit()
              cursor.close()
            except Exception:
                print("Mysql Error.")
            time.sleep(1)
        conn.close()
    else:
        print "Every over!"
    time.sleep(10)

