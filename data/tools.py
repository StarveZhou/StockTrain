"""工具类
实现了简单但是低效的日期操作
"""

def date_tool(date, type):
    """获得日期的前一天或后一天的日期字符串"""
    def isleap(y):
        """判断年份是否是闰年"""
        return y % 400 ==0 or (y % 4 == 0 and y % 100 != 0)
    
    y = int(date[0:4])
    m = int(date[5:7])
    d = int(date[8:10])
    m31 = [1, 3, 5, 7, 8, 10, 12]
    m30 = [4, 6, 9, 11]

    if type == 1:
        d += 1
        if (d == 31 and m in m30) or (d == 32) or (d == 29 and m == 2 and isleap(y) == False) or (d == 30 and m == 2):
            m += 1
            d = 1
            if m == 13:
                m = 1
                y += 1
    else:
        d -= 1
        if d == 0:
            m -= 1
            if m == 0:
                m = 12
                y -= 1
            if m in m31:
                d = 31
            elif m in m30:
                d = 30
            elif isleap(y) == True:
                d = 29
            else:
                d = 28

    str = "%d-"%y
    if m < 10:
        str += "0%d-"%m
    else:
        str += "%d-"%m

    if d < 10:
        str += "0%d"%d
    else:
        str += "%d"%d
    
    return str

def change_date(date, num):
    while num is not 0:
        if num > 0:
            date = date_tool(date, 1)
            num -= 1
        else:
            date = date_tool(date, -1)
            num += 1
    return date