import sys
sys.path.append("../")

import properties
import os
import json
import tushare as ts
import time
import data.tools as tools
import pandas

""" data_cache
用来从 tushare 获取数据，由于网络连接可能较慢，所以实现一个简单的本机cache
"""

stock_cache_in_memory = {}

def get_cache_list_from_disk():
    """获取 cache_list.json 中的内容"""
    data_cache_location = properties.properties["data_cache_location"]
    cache_list_location = data_cache_location + "\\cache_list.json"

    with open(cache_list_location, "r") as f:
        cache_list = json.load(f)
    cache_list["update-time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    return cache_list

def check_cache_list():
    """检查是否存在 cache_list.json"""
    data_cache_location = properties.properties["data_cache_location"]
    file_dir = os.listdir(data_cache_location)
    cache_list_filename = data_cache_location + "\\cache_list.json"
    
    if cache_list_filename not in file_dir:
        stock_cache_in_memory['cache_list'] = {"update-time" : time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}
        with open(cache_list_filename, "w") as f:
            json.dump(stock_cache_in_memory['cache_list'], f)
    else:
        print("??")
        stock_cache_in_memory['cache_list'] = get_cache_list_from_disk()


def check_cache_in_memory():
    if 'cache_list' not in list(stock_cache_in_memory):
        check_cache_list() 


def get_cache_list():
    check_cache_in_memory()
    return stock_cache_in_memory['cache_list']
    



def update_cache_list_json():
    """更新 cache_list.json"""

    data_cache_location = properties.properties["data_cache_location"]
    cache_list_location = data_cache_location + "\\cache_list.json"
    # print(">>>", cache_list_location)
    with open(cache_list_location, "w") as f:
        # print("><><>", stock_cache_in_memory['cache_list'])
        json.dump(stock_cache_in_memory['cache_list'], f)

def update_cache_list(cache_list):
    stock_cache_in_memory['cache_list'] = cache_list

def update_cache(location, data):
    # print(">>> is updated", location)
    data.to_csv(location, index = False)

def get_data_from_cache(location):
    data = pandas.read_csv(location)
    return data

# ['open', 'close', 'high', 'low', 'volume'] from aim
# ['date', 'open', 'close', 'high', 'low', 'volume', 'code']
def get_data_from_tushare(code, start_date='2018-01-01', end_date='2018-03-21'):
    """从 tushare 上下载数据"""
    data = ts.get_k_data(code, start=start_date, end=end_date, autype='qfq')
    # print(code, start_date, end_date, sep=", ")
    # print(data)
    data = data.drop(['code'], axis=1)
    return data
  

def update_memory_cache(code, data):
    stock_cache_in_memory[code] = data

def get_data(code, start_date='2018-01-01', end_date='2018-03-21'):
    """实现一个封装的 get_data"""
    # print("get_data A")
    cache_list = get_cache_list()
    # 从内存中读取数据
    if code in list(stock_cache_in_memory):
        ori_data = stock_cache_in_memory[code]
        cache_info = cache_list[code]
        if start_date <= cache_info['start_date'] and end_date >= cache_info['end_date']:
           #  print(">>")
            return ori_data[ori_data['date'] >= start_date & ori_data['date'] <= end_date]


    
    # 从硬盘中读取数据
    data_location = properties.properties["data_cache_location"] + "\\" + code + ".csv"

    if code not in cache_list:
        data = get_data_from_tushare(code, start_date, end_date)
        cache_list[code] = {'start_date' : start_date, 'end_date' : end_date}
        update_memory_cache(code, data)
        update_cache(data_location, data)
        update_cache_list_json()
    else:
        original_data = get_data_from_cache(data_location)
        
        #print(original_data[original_data['date'] <= end_date])

        cache_info = cache_list[code]

        dataUpdate = False

        if end_date > cache_info['end_date']:
            nstart_date = tools.date_tool(cache_info['end_date'], 1)
            data = get_data_from_tushare(code, nstart_date, end_date)
            original_data = original_data.append(data)
            cache_info['end_date'] = end_date
            dataUpdate = True
        
        if start_date < cache_info['start_date']:
            nend_date = tools.date_tool(cache_info['start_date'], -1)
            data = get_data_from_tushare(code, start_date, nend_date)
            original_data = data.append(original_data)
            cache_info['start_date'] = start_date
            dataUpdate = True

        # print("orig\n", original_data)

        if dataUpdate == True:
            update_cache(data_location, original_data)
            update_memory_cache(code, original_data.copy())
            update_cache_list(cache_list)
            update_cache_list_json()
        
        data = original_data[(original_data['date'] >= start_date) & (original_data['date'] <= end_date)]

        
        
        
        
    
    # print(cache_list)
    # print(data)
    
    return data


if __name__ == '__main__':
    check_cache_in_memory()

    print(stock_cache_in_memory)
    data = get_data('hs300', start_date="2018-01-04", end_date="2018-01-05")
    data = get_data('hs300', start_date="2018-01-02", end_date="2018-01-03")
    

    print(stock_cache_in_memory)
    print(data)
    # data = get_data('hs300', start_date="2018-01-01", end_date="2018-03-01")
    # print(data)
    # check_cache_list()