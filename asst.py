"""辅助功能
"""


class Info:
    """为服务端储存信息
    用户可以访问，最好不要修改
    最好通过G类中的info字段获取Info的信息字符串
    """
    def __init__(self):
        self.version = '2.1'
        self.option = {}
        self.record = {}

    def str(self, add_info="None"):
        s = ""
        s += "additional info : " + add_info + "\n"
        s += "version : " + self.version + "\n"
        s += "option(num : %d) : \n"%len(self.option)
        for item in list(self.option):
            s += "\t" + item + " : "
            if isinstance(self.option[item], str) == True:
                s += self.option[item]
            else:
                s += str(self.option[item])
            s += '\n'
        s += "benchmark : %s\n"%self.benchmark
        s += "OrderCost : \n"
        s += self.cost.str() + "\n"
        s += "type : " + self.type + "\n"

        s += str(self.earning) + "\n"
        s += str(self.benchmark_earning) + "\n"

        s += "record : \n"
        for key in list(self.record):
            s += "\tkey : " + key + "\n"
            s += "\t\t" + str(self.record[key])
            s += '\n'

        return s
    
    def get_result_box(self):
        s = ""
        s += "version : " + self.version + "\r\n"
        s += "benchmark : %s\r\n"%self.benchmark
        date_set = [x for x, y in self.earning.items()]
        min_date = min(date_set)
        max_date = max(date_set)

        s += "your strategy : \r\n"
        s += "\t" + min_date + " : " + "%.2f"%self.earning[min_date] + "\r\n"
        s += "\t" + max_date + " : " + "%.2f"%self.earning[max_date] + "\r\n"
        earning_rate = self.earning[max_date] - self.earning[min_date]
        earning_rate /= self.earning[min_date]
        earning_rate *= 100
        s += "\tearning rate : %.2f"%earning_rate + "%\r\n"

        date_set = [x for x, y in self.benchmark_earning.items()]
        min_date = min(date_set)
        max_date = max(date_set)

        s += "benchmark : \r\n"
        s += "\t" + min_date + " : " + "%.2f"%self.benchmark_earning[min_date] + "\r\n"
        s += "\t" + max_date + " : " + "%.2f"%self.benchmark_earning[max_date] + "\r\n"
        earning_rate = self.benchmark_earning[max_date] - self.benchmark_earning[min_date]
        earning_rate /= self.benchmark_earning[min_date]
        earning_rate *= 100
        s += "\tearning rate : %.2f"%earning_rate + "%\r\n"

        return s

        # TODO

info = Info()

class G:
    """为用户储存信息
    用户需要保存的信息存在此类中
    服务端不会访问该信息
    info字段保存info的字符串信息
    """
    def __init__(self):
        self.info = info.str




class OrderCost:
    """保存交易数据
    """
    def __init__(self, open_tax, close_tax, open_commission, close_commission, close_today_commission, min_commission):
        self.open_tax = open_tax
        self.close_tax = close_tax
        self.open_commission = open_commission
        self.close_commission = close_commission
        self.close_today_commission = close_today_commission
        self.min_commission = min_commission

    def str(self):
        s = ""
        s += "\topen_tax : " + str(self.open_tax) + "\n"
        s += "\tclose_tax : " + str(self.close_tax) + "\n"
        s += "\topen_commission : " + str(self.open_commission) + "\n" 
        s += "\tclose_commission : " + str(self.close_commission) + "\n"
        s += "\tclose_today_commission : " + str(self.close_today_commission) + "\n"
        s += "\tmin_commission : " + str(self.min_commission)

        return s