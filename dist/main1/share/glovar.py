# 存放全局变量的模块

def _init():
    """ 初始化 """

    global global_dict
    global_dict = {}


def set_value(key,value):
    """ 定义一个全局变量 """

    global_dict[key] = value


def get_value(key,defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """

    try:
        return global_dict[key]
    except KeyError:  # 查找字典的key不存在的时候触发
        return defValue