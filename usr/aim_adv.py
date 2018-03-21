from st import *

def initialize(context):
    set_benchmark('000300.XSHG')
    set_option('use_true_price', True)
    set_option('order_volume_ratio', 1)
    set_order_cost(OrderCost(open_tax=0, close_tax=0,\
                  open_commission=0.003, close_commission=0.003,\
                  close_today_commission=0, min_commission=5), type="stock")
    g.n1 = 5
    g.n2 = 10
    g.stock_num = 3
    g.stock_list = []
    run_daily(trade, "every_bar")

def trade(context):
    for stock in list(context.portfolio.positions.keys()):
        close_data = attribute_history(stock, g.n2+2, '1d', ['close'], df=false)['close']
        ma1 = close_data[-g.n1:].mean()
        ma2 = close_data[-g.n2:].mean()
        if (ma1<ma2):
            order_target_value(stock, 0)
    
    buy_num = g.stock_num-len(context.portfolio.positions)
    buy_value = context.portfolio.cash/buy_num
    for i in range(buy_num):
        order_value(g.stock_list[i], buy_value)

def ma_factor2(context, stock):
    close_data = attribute_history(stock, g.n2+2, '1d', ['close'], df=false)['close']
    ma = close_data[-g.n2:].mean()
    return (ma - close_data[-1])/ma

def normallize(factor_list):
    Min = min(factor_list)
    Max = max(factor_list)
    return [(x-Min)/(Max-Min) for x in factor_list]

def before_trading_start(context):
    q = query(valuation.code).filter(valuation.market_cap.between(20, 30) & (valuation.pe_ratio>0))
    stock_list = list(get_fundamentals(q)['code'])
    current_data = get_current_data()
    stock_list = [stock for stock in stock_list if not current_data['paused']]

    #ma_f = [ma_factor(context, stock) for stock in stock_list]
    #ma_f2= [ma_factor2(context, stock)for stock in stock_list]
    #ma_f2 = normallize(ma_f2)

    #stock_list = pandas.DataFrame(np.array([[stock_list[i], ma_f[i], ma_f2[i]]] for i in len(stock_list)]))
    #g.stock_list = list(stock_list.sort_values(by= 1, ascending=False)[0])
    g.stock_list = [stock for stock in stock_list if ma_factor(context, stock)]

def ma_factor(context, stock):
    close_data = attribute_history(stock, g.n2+2, '1d', ['close'], df=false)['close']
    ma1 = close_data[-g.n1:].mean()
    ma2 = close_data[-g.n2:].mean()
    ma1_= close_data[-g.n1-1:-1].mean()
    ma2_= close_data[-g.n2-1:-1].mean()
    return (ma1>ma2 and ma1_<ma2_)
