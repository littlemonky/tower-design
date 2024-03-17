import datetime
import numpy as np
import pandas as pd

from cooling_tower import cooling_tower_main

STANDARD_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def main(input_data, **kwargs):
    '''

    :param input_data: 环境参数
    :param kwargs:
    :return:
    '''

    # 读取机组设计参数
    design_data = pd.read_csv("./thermal_cycle_config.csv")
    design_data = {design_data.iloc[i]["param_name"]: design_data.iloc[i]["value"] for i in range(len(design_data))}

    # 读取机组运行投运参数 - 如果实际运行结果出现偏离，会进行自动迭代修正
    raw_data = pd.read_csv("./power_station.csv")
    raw_data = raw_data.iloc[-1].to_dict()

    # 假设初始背压计算电站的功率和排汽流量，输出参数保存格式为dict
    # 1. 模块1
    results1 = cooling_tower_main() #TODO

    # 2
    results2 = cooling_tower_main()  # TODO

    # 3
    results3 = cooling_tower_main()  # TODO

    # 4
    results4 = cooling_tower_main()  # TODO


    results = {}
    results = results | results1
    results = results | results2
    results = results | results3
    results = results | results4

    return results




