from matplotlib.pylab import date2num
import datetime
import matplotlib as mpl
import tushare as ts
import matplotlib.pyplot as plt
import properties

"""回测结束后的处理
生成图片和markdown文件
"""

def date_to_num(dates):
    """将日期转换为matplotlib可以识别的日期格式"""
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time

def draw_main(info):
    """绘制收益和基准的回测曲线"""
    filepath = properties.properties["log_info"]["location"]


    fig, ax = plt.subplots(figsize=(15, 5))
    fig.subplots_adjust(bottom=0.5)
    plt.grid = True
    plt.xticks(rotation=30)
    plt.title('StockTrain')
    plt.xlabel('Date')
    plt.ylabel('Amount')

    date = list(info.earning)
    earning = [info.earning[x] for x in date]
    benchmark = [info.benchmark_earning[x] for x in date]
    num_time = date_to_num(date)
    # print(num_time)
    # print(earning)
    # print(benchmark)
    
    plt.plot(num_time, earning, color="red", label="earning")
    plt.plot(num_time, benchmark, color="black", label="benchmark")

    for key in info.record:
        record_value = [info.record[key][x] for x in date]
        plt.plot(num_time, record_value, label=key, linestyle=':', marker='|')

    plt.legend()

    ax.xaxis_date ()
    #plt.show()
    plt.savefig(filepath+"\\"+"main.png", format="png", dpi=300)
    
def draw_record(info):
    """绘制record曲线"""
    filepath = properties.properties["log_info"]["location"]


    fig, ax = plt.subplots(figsize=(15, 5))
    fig.subplots_adjust(bottom=0.5)
    plt.grid = True
    plt.xticks(rotation=30)
    plt.title('StockTrain')
    plt.xlabel('Date')
    plt.ylabel('Price')

    date = list(info.earning)

    num_time = date_to_num(date)


    for key in info.record:
        record_value = [info.record[key][x] for x in date]
        plt.plot(num_time, record_value, label=key)

    plt.legend()

    ax.xaxis_date ()
    #plt.show()
    plt.savefig(filepath+"\\"+"record.png", format="png", dpi=300)

def generate_md(info):
    """生成markdown文件"""
    filepath = properties.properties["log_info"]["location"] + "\\" + properties.properties["log_info"]["usr"] + "_info.md"

    with open(filepath, "w") as f:
        f.write("# Infomation : \n" + info.str() + "\n\n")
        f.write("### main plot : \n\n ![](./main.png)\n\n")
        f.write("### record plot : \n\n ![](./record.png)\n\n")
    f.close()


if __name__ == '__main__':
    draw_main()