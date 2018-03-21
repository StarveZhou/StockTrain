from asst import *
from context import context
from data.data_cache import *
from data.tools import *
from properties import *
import datetime
import os

"""API模块
主要为用户的回测程序提供API
回测程序通过加载该模块
    from st import *
获取能够使用的API
"""

g = G()
info.original_cash = 100000
context = context.Context(info.original_cash)

def get_info():
    """获取info指针"""
    return info

def set_benchmark(code):
    """设定基准股票数据"""
    info.benchmark = code
    context.update_stock(code)

def set_order_cost(cost, type, ref=None):
    """设定交易参数"""
    info.cost = cost
    info.type = type

def set_option(op_name, op_value):
    """设定option(暂时什么参数)"""
    if isinstance(op_name, str) == False:
        raise Exception("option name need to be str type")
    info.option[op_name] = op_value

def run_daily(trade, run_tp="every_bar"):
    """设定回测方式，目前只支持每日回测"""
    info.trade = trade
    info.run_tp = "every_bar"

def set_date(start_date='2018-01-01', end_date='2018-03-01'):
    """设置回测的起止日期"""
    info.start_date = start_date
    info.end_date = end_date


def attribute_history(security, count, unit="1d", fields=['open', 'close', 'high', 'low', 'volume'], skip_pause=True, df=True, fq='pre'):
    """获得股票历史数据"""
    # print("Attribute_history : Step A")
    
    if context.portfolio.contain(security) is False:
        _ = get_data(code=security, start_date=info.start_date, end_date=info.end_date)
        context.update_stock(security)
    
    
    
    ed_d = date_tool(info.today, -1)
    st_d = change_date(ed_d, -count+1)

    # print("Attribute_history : Step B")

    while True:
        data = get_data(code=security, start_date=st_d, end_date=ed_d)[fields]
        if len(data) == count:
            break
        st_d = date_tool(st_d, -1)
        # print("Attribute_history : Step C")
        #print(st_d, ed_d, len(data), sep=', ')
    
    #print(type(data['close']))
    if df == False:
        data_dict = {}
        for name in fields:
            data_dict[name] = data[name].values
        data = data_dict
    # print("Attribute_history : Step D")
    #print(data)
    return data


def order_value(security, value, style=None, side='long', pindex=0):
    """买卖股票，value为正时买入，为负时卖出"""
    #print("Order_value A")
    data = get_data(code=security, start_date=info.today, end_date=info.today)
    #print("Order_value B")
    if (data.empty):
        log.info("Warning! " + " stock : " + security + " reason : no infomation today")
        return
    #print("Order_value C")
    # print(data, info.today)
    price = float(data['open'])
    #print("Order_value D", price)
    if value > 0:
        count = value / price
        context.update_stock(security, count, -value)
    else:
        count = -value / price
        context.update_stock(security, -count, value)
    #print("Order_value E")

def order_target(security, value, style=None, side='long', pindex=0):
    """买卖股票，将当前持有的股票价值调整为value"""
    #print("Order_target_value A")
    data = get_data(code=security, start_date=info.today, end_date=info.today)
    if (data.empty):
        log.info("Warning! date : " + info.today + " stock : " + security + " reason : no infomation today")
        return
    #print("Order_target_value B")
    price = float(data['open'])
    original_count = context.get_stock_count(security)
    original_value = original_count * price
    #print("Order_target_value C")
    if value > original_value:
        value -= original_value
        count = value / price
        context.update_stock(security, count, -value)
    else:
        value = original_value - value
        count = value / price
        context.update_stock(security, -count, value)
    #print("Order_target_value D")

def record(**kwargs):
    """记录参数，最后会单独绘制为一张表格"""
    for key in kwargs:
        if key not in list(info.record):
            info.record[key] = {}
        info.record[key][info.today] = kwargs[key]

class log:
    """日志类
    结果将会储存在log文件夹下
    """
    @staticmethod
    def info(s):
        """向日志中输出一条记录"""
        usr = properties["log_info"]["usr"]
        log_file_path = properties["log_info"]["location"]
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        filename = log_file_path + "\\log_" + usr + ".txt"
        if os.path.exists(filename):
            with open(filename, "a") as f:
                f.write(time_now + "(real)\t" + info.today + "(sim)" + " : \n\t" + s + "\n")
                f.close()
        else:
            with open(filename, "w") as f:
                f.write(time_now + "(real)\t" + info.today + "(sim)" + " : \n\t" + s + "\n")
                f.close()
    @staticmethod
    def reset():
        """重置日志"""
        usr = properties["log_info"]["usr"]
        log_file_path = properties["log_info"]["location"]
        filename = log_file_path + "\\log_" + usr + ".txt"
        if os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("")
                f.close()


