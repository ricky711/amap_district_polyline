# -*- coding: utf-8 -*-
"""
author: 
subject: 调用高德接口查询行政区域的边界坐标点，https://lbs.amap.com/api/webservice/guide/api/district
date: 
"""
import requests
import time
import pymysql

# 高德相关应用的key
key = ''


# 查询行政区域的边界坐标点
def ad_district_polyline(keywords):
    if keywords:
        create_time = time.strftime('%Y-%m-%d %H:%M:%S')
        url = 'https://restapi.amap.com/v3/config/district?parameters'
        params = {
            'key': key,
            'output': 'JSON',
            'keywords': keywords,
            'subdistrict': 1,
            'extensions': 'all'
        }
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'accept': 'application/json, text/javascript, */*; q=0.01'
        }
        output = requests.get(url, headers=headers, params=params).json()
        status = output['status']
        info = output['info']
        infocode = output['infocode']
        count = output['count']
        districts = output['districts']
        if status == '1':
            adcode = districts[0]['adcode']
            name = districts[0]['name']
            polyline = districts[0]['polyline']
            center = districts[0]['center']
            level = districts[0]['level']
            sub_districts = districts[0]['districts']
            output = [adcode, name, level, [[i['adcode'], i['name'], i['level']] for i in sub_districts]]
            result = ('', create_time, str(keywords), status, info, infocode, count, adcode, name, center, level, polyline)
        else:
            output = []
            result = ('', create_time, str(keywords), status, info, infocode, count, '', '', '', '', '')
        connect = pymysql.connect(host='',
                                user='',
                                password='=',
                                db='',
                                port=,
                                charset='utf8')
        sql = 'INSERT INTO crawl.t_ad_district_polyline\
            (findex, fcreate_time, fkeywords, fstatus, finfo, finfocode, fcount, fadcode, fname, fcenter, flevel, fpolyline)\
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        try:
            with connect.cursor() as cursor:
                cursor.execute(sql, result)
                connect.commit()
                cursor.close()
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'insert success:', keywords)
        except Exception as e:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), 'insert failed:', keywords, e)
        connect.close()

        return output
    else:
        return []


if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'main start')
    pool = []
    pool.append('100000')
    relations = []
    while pool:
        ad = pool.pop()
        output = ad_district_polyline(ad)
        if output:
            sub_districts = output[3]
            for i in sub_districts:
                if i[0] != ad:
                    pool.append(i[0])
                relations.append(('', time.strftime('%Y-%m-%d %H:%M:%S'), output[0], output[1], output[2], i[0], i[1], i[2]))
    
    connect = pymysql.connect(host='',
                            user='',
                            password='',
                            db='',
                            port=,
                            charset='utf8')
    sql = 'INSERT INTO crawl.t_ad_relation\
        (findex, fcreate_time, fpadcode, fpname, fplevel, fadcode, fname, flevel)\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        with connect.cursor() as cursor:
            cursor.executemany(sql, relations)
            connect.commit()
            cursor.close()
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'insert success relations')
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'insert failed relations', e)
    connect.close()
    print(time.strftime('%Y-%m-%d %H:%M:%S'), 'main finish')
