import sys
sys.path.append("../")
import st
from data.tools import *

"""Context实现文件
"""


class Context:
    """Context类
    用于储存股票信息
    用户和服务端均可访问
    """
    def __init__(self, cash):
        """初始化资金"""
        self.portfolio = Portfolio(cash)

    def update_stock(self, code, count=0, cost=0):
        """更新持有股票数据"""
        self.portfolio.update_positions(code, count, cost)
        self.update_info()

    def get_stock_count(self, code):
        """获取当前持有的股票数量"""
        #print("In")
        if code in list(self.portfolio.positions):
            #print("Get_stock_count", self.portfolio.positions[code].hold)
            return self.portfolio.positions[code].hold
        else:
            return 0
    def update_info(self):
        """更新持有股票的价格数据和比例数据"""
        self.portfolio.update_price()
        self.portfolio.update_amount()

    def str(self):
        s = ""
        s += "Portfolio : \n"
        s += self.portfolio.str()
        return s

    def calculate(self):
        """计算当前的所有资产总和"""
        sum = self.portfolio.calculate()
        sum += self.portfolio.cash
        return sum

class Portfolio:
    """账户的股票池
    """
    def __init__(self, cash):
        """初始化资金池"""
        self.positions = {}
        self.cash = cash

    def update_positions(self, code, change_hold, cost):
        """更新持有的股票数量"""
        if code in list(self.positions):
            self.positions[code].hold += change_hold
        else:
            self.positions[code] = Position(change_hold)

        self.cash += cost
    
    def update_price(self):
        """更新股票价格"""
        today = st.get_info().today
        for code in list(self.positions):
            while True:
                data = st.get_data(code, today, today)
                if len(data) != 0:
                    break
                today = date_tool(today, -1)
            
            #print ("att")
            #print (float(data['open']))
            self.positions[code].price = float(data['open'])
    
    def update_amount(self):
        """更新股票资金占比"""
        amount = self.cash
        for code in list(self.positions):
            amount += self.positions[code].price * self.positions[code].hold
        
        for code in list(self.positions):
            self.positions[code].closeable_amount = 1.0 * self.positions[code].price * self.positions[code].hold / amount
        
        self.amount = amount
    
    def contain(self, code):
        """判断股票池中是否存在该股票，买过但是持有量为0也算存在"""
        if code in list(self.positions):
            return True
        else:
            return False

    def str(self):
        """返回信息字符串"""
        s = ""
        s += "\tcash : " + str(self.cash) + "\n"
        s += "\tPositions : \n"
        for code in list(self.positions):
            s += "\t\t" + code + " : " + self.positions[code].str() + "\n"
        return s
    
    def calculate(self):
        """计算股票池的价值之和"""
        sum = 0
        for code in list(self.positions):
            sum += self.positions[code].price * self.positions[code].hold
        return sum

        

class Position:
    """单个股票数据
    """
    def __init__(self, hold_num):
        """初始化股票持有量"""
        self.hold = hold_num
        self.closeable_amount = 0
    
    def str(self):
        """返回信息字符串"""
        return "{hold : %f, closable_amount : %f}"%(self.hold, self.closeable_amount)