from usr.aim import *
import st
from data.tools import *
from inspect import isfunction
from data.data_cache import *
import draw

"""主文件
手动运行时运行该代码
"""

if __name__ == '__main__':
    try:
        check_cache_in_memory()
        st.log.reset()
        info = get_info()

        set_date()

        meet_end = False
        info.today = info.start_date
        initialize(context)

        info.earning = {}
        info.benchmark_earning = {}
        benchmark_data = get_data(code=info.benchmark, start_date=info.start_date, end_date=info.end_date)
        benchmark_cost = -1
        benchmark_cost_last = -1

        #print(">>>> benchmark")
        #print(benchmark_data)

        while True:
            if meet_end == True:
                break
            print(">>>>> : ", info.today, info.start_date, info.end_date)
            #print("StockTrain Step A")
            context.update_info()
            #print("StockTrain Step B")
            
            trade(context)

            #print("StockTrain Step C")

            info.earning[info.today] = context.calculate()
            if info.today == info.start_date:
                info.benchmark_earning[info.today] = info.original_cash
                benchmark_cost_last = info.original_cash
            elif benchmark_data[benchmark_data.date == info.today].empty is False:
                if benchmark_cost is -1:
                    #print(">>>> ", float(benchmark_data[benchmark_data.date == info.today]['open']))
                    benchmark_cost = float(benchmark_data[benchmark_data.date == info.today]['open'])
                info.benchmark_earning[info.today] = info.original_cash * float(benchmark_data[benchmark_data.date == info.today]['open']) / benchmark_cost
                benchmark_cost_last = info.benchmark_earning[info.today]
            else:
                info.benchmark_earning[info.today] = benchmark_cost_last

            #print("StockTrain Step D")
            
            if info.today == info.end_date:
                meet_end = True
            info.today = date_tool(info.today, 1)
            #print("StockTrain Step E")
            #print(info.str())
            #print("StockTrain Step F")
        print(info.str())
        
        draw.draw_record(info)
        draw.draw_main(info)
        draw.generate_md(info)
    except:
        update_cache_list_json()
