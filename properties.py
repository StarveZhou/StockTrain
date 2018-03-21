import json

"""读取配置参数模块
"""
def read_properties():
    """读取配置参数"""
    with open('C:\\Users\\StarveZhou\\Desktop\\GitHub\\StockTrain\\properties.json', 'r') as f:
        properties = json.load(f)
    return properties


properties = read_properties()

if __name__ == '__main__':
    properties = read_properties()
    print(properties)