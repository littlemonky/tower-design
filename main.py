import datetime
import numpy as np
import pandas as pd
import thermal_cycle
import cooling_tower
import condenser

STANDARD_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
# 参数输入
h3 = 18.989
d3 = 192.6307
h6 = 60.6255
d6 = 172.4631
h9 = 249.091
d9 = 121.4750
d0 = 210
Lfi = 2
Afrw = 28021
Afrd = 43056
l = 3.688
Lte = 31.8909
ntb = 256
Do = 0.0254
Di = 0.0234
nr = 4
nwp = 2
aj = 27.75
nb = 183
Ta1 = 296.15
RH = 0.81
pa1 = 100000
mw = 45200




#def main(input_data, **kwargs):
def main(h3,d3,h6,d6,h9,d9,d0,Lfi,Afrw,Afrd,l,Lte,ntb,Do,Di,nr,nwp,aj,nb,Ta1,RH,pa1,mw):
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
    Pcn=0.0033
    delta_Q=1
    while abs(delta_Q) > 0.001:
        if delta_Q > 0:
            Pcn = Pcn + min(0.0001, 0.001 * abs(delta_Q))
        else:
            Pcn = Pcn - min(0.0001, 0.001 * abs(delta_Q))


        real, pred, W, xpai, Qpai=thermal_cycle.thermal_cycle_main(Pcn,raw_data,design_data)
        Tin,Tc=condenser.condenser_main(mw,xpai,Pcn,Qpai)
        mwevap,Qtot=cooling_tower.cooling_tower_main1(h3,d3,h6,d6,h9,d9,d0,Lfi,Afrw,Afrd,l,Lte,ntb,Do,Di,nr,nwp,aj,nb,Ta1,RH,pa1,Tin,mw)
        delta_Q = (Qpai - Qtot) / Qpai
    # 1. 模块1
    # results1 = cooling_tower_main() #TODO
    #
    # # 2
    # results2 = cooling_tower_main()  # TODO
    #
    # # 3
    # results3 = cooling_tower_main()  # TODO
    #
    # # 4
    # results4 = cooling_tower_main()  # TODO
    #
    #
    # results = {}
    # results = results | results1
    # results = results | results2
    # results = results | results3
    # results = results | results4
    return Pcn,W,mwevap,Qtot

Pcn,W,mwevap,Qtot= main (h3,d3,h6,d6,h9,d9,d0,Lfi,Afrw,Afrd,l,Lte,ntb,Do,Di,nr,nwp,aj,nb,Ta1,RH,pa1,mw)
print("mevap:", mwevap, "q:", Qtot, "Pcn:", Pcn, "W:", W)




