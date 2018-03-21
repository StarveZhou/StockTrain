from st import *

def initialize(context):
    g.security = '000002'
    set_date(start_date='2018-01-01', end_date='2018-03-01')
    set_benchmark('hs300')
    set_option('use_real_price', True)
    set_option('order_volume_ratio', 1)
    set_order_cost(OrderCost(open_tax=0, close_tax=0.001,\
                             open_commission=0.0003, close_commission=0.003,\
                             close_today_commission=0, min_commission=5), type='stock')
    run_daily(trade, 'every_bar')

def trade(context):
    #print("Trade A")
    security = g.security
    n1 = 5
    n2 = 10
    close_data = attribute_history(security, n2+2, '1d', ['close'], df=False)
    # print("slice error : ", n1, n2)
    # print(close_data['close'])
    #print("Trade B")
    ma_n1 = close_data['close'][-n1:].mean()
    ma_n2 = close_data['close'][-n2:].mean()

    
    cash = context.portfolio.cash
    #print("Trade C")

    #print(context.portfolio.positions)

    #print(context.str() + "\n\n\n")
    #print("Trade D")
    if ma_n1 > ma_n2:
        order_value(security, cash)
        log.info('Buying %s'%(security))
    elif ma_n1 < ma_n2 and context.portfolio.positions[security].closeable_amount > 0:
        #print("Trade D-")
        order_target(security, 0)
        log.info('Selling %s' % (security))
    #print("Trade E")
    
    record(ma_n1=ma_n1)
    record(ma_n2=ma_n2)
    #print(close_data['close'])
    record(close=close_data['close'][-1])