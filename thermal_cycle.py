import CoolProp.CoolProp as CP
from asset_config import Unit

unit = Unit()
design_data = unit.design_param

def thermal_cycle_main(Pcn, raw_data, design_data):

    # 真实参数结果初始化
    Dh, D34, D45, D56, D67, Dpai, Tc, Dpai, delta_hc, y01_real, y12_real, \
        y23_real, y34_real, y45_real, y56_real, y67_real, y7c_real, b1_real, \
        b2_real, bsep_real, c1_real, c2_real, c6_real, c7_real, cL_real = [None] * 25
    # 预测参数结果初始化
    y01, y12, y23, y34, y45, y56, y67, y7c, b1, b2, bsep, c1, c2, c6, c7, cL = [None] * 16

    #设计值
    D0 = design_data['D0']
    # print(D0)
    Ngd = design_data['Ngd']
    # { := := := := := := := := := := := := := 各压力值 := := := := := := := := := := := := := := := := := :=}
    P0d = design_data['P0d']  # 设计值
    P1d = design_data['P1d']  # 设计值
    P2d = design_data['P2d']  # 设计值
    P3d = design_data['P3d']  # 设计值
    P4d = design_data['P4d']  # 设计值
    P5d = design_data['P5d']  # 设计值
    P6d = design_data['P6d']  # 设计值
    PL = design_data['PL']  # 设计值
    P7d = design_data['P7d']  # 设计值
    Pcnd = design_data['Pcnd']  # 设计值
    pw3b = design_data['pw3b'] # 给水泵出口压力设计值
    Pwc = design_data['Pwc']  # 凝结水泵出口压力设计值
    #:= := := := := := := := := := 各加热器的出口水温 := := := := := := := := := := := := % %
    tw1d = design_data['tw1d']
    tw2d = design_data['tw2d']
    tw3bd = design_data['tw3bd']
    tw3d = design_data['tw3d']
    tw4d = design_data['tw4d']
    tw5d = design_data['tw5d']
    tw6d = design_data['tw6d']
    tw7d = design_data['tw7d']
    twcd = design_data['twcd']
    # := := := := := := := := := := 以下为低加疏水温度 := := := := := := := := := := := % %
    td1d = design_data['td1d']
    td2d = design_data['td2d']
    td4d = design_data['td4d']
    td5d = design_data['td5d']
    td6d = design_data['td6d']
    td7d = design_data['td7d']
    #:= := := := := := := := := := 加热器入口压力设计值 := := := := := := := := := := := % %
    h1_in_P_d = design_data['h1_in_P_d']
    h2_in_P_d = design_data['h2_in_P_d']
    h3_in_P_d = design_data['h3_in_P_d']
    h4_in_P_d = design_data['h4_in_P_d']
    h5_in_P_d = design_data['h5_in_P_d']
    h6_in_P_d = design_data['h6_in_P_d']
    h7_in_P_d = design_data['h7_in_P_d']
    rh1_in_P_d_es_d = design_data['rh1_in_P_d_es_d']
    rh2_in_P_d_es_d = design_data['rh2_in_P_d_es_d']
    rh1_in_P_d_ms_d = design_data['rh1_in_P_d_ms_d']
    rh1_out_P_es_d = design_data['rh1_out_P_es_d']
    rh2_out_P_es_d = design_data['rh2_out_P_es_d']
    rh2_in_P_d_ms_d = design_data['rh2_in_P_d_ms_d']
    rh2_out_P_ms_d = design_data['rh2_out_P_ms_d']
    lp_in_P_d = design_data['lp_in_P_d']
    h3_out_P_fw_d = design_data['h3_out_P_fw_d']
    # := := := := := := := := := := 加热器端差(设计数据) := := := := := := := := := := := % % 取
    sdc1 = design_data['sdc1']
    sdc2 = design_data['sdc2']
    sdc3 = design_data['sdc3']
    sdc4 = design_data['sdc4']
    sdc5 = design_data['sdc5']
    sdc6 = design_data['sdc6']
    sdc7 = design_data['sdc7']
    sdc8 = design_data['sdc8']
    sdc9 = design_data['sdc9']
    xdc1 = design_data['xdc1']
    xdc2 = design_data['xdc2']
    xdc3 = design_data['xdc3']
    xdc4 = design_data['xdc4']
    xdc5 = design_data['xdc5']
    xdc6 = design_data['xdc6']
    xdc7 = design_data['xdc7']
    # := := := := := := := := := := := := 汽轮机侧参数 := := := := := := := := := := := := := := :=}
    # 额定工况下的抽汽焓
    h1d = design_data['h1d']
    h2d = design_data['h2d']
    h3d = design_data['h3d']
    h4d = design_data['h4d']
    h5d = design_data['h5d']
    h6d = design_data['h6d']
    h7d = design_data['h7d']
    hcd = design_data['hcd']
    hsg3 = design_data['hsg3']
    # 额定工况下一至八段抽汽温度
    t1d = design_data['t1d']
    t2d = design_data['t2d']
    t3d = design_data['t3d']
    t4d = design_data['t4d']
    t5d = design_data['t5d']
    t6d = design_data['t6d']
    t7d = design_data['t7d']
    # 小汽水流量
    Dsgh = design_data['Dsgh']
    Dsg1 = design_data['Dsg1']
    DsgL = design_data['DsgL']
    Dsg2 = design_data['Dsg2']
    Dsg3 = design_data['Dsg3']
    Dsg4 = design_data['Dsg4']
    # := := := := := 各加热器出口温度的应达值 := :做了保留两位有效小数处理！！！！！
    Drh2d = design_data['Drh2d']
    Dhd = design_data['Dhd']
    Dpaid = design_data['Dpaid']


    P0 = design_data['P0d']  #迭代初始值
    # P0 = 6.85

    Ng = raw_data['Ng'] #实际值 实际发电功率
    P0r = raw_data['P0']
    P1r = raw_data['P1']
    P2r = raw_data['P2']
    P3r = raw_data['P3']
    P4r = raw_data['P4']
    P5r = raw_data['P5']
    P6r = raw_data['P6']
    P7r = raw_data['P7']
    P8r = raw_data['P8']
    P9r = raw_data['P9']
    P10r = raw_data['P10']
    Pcnr = raw_data['Pcn']
    Prhr = raw_data['Prh']
    P0rh2r = raw_data['P0rh2']
    P1rh1r = raw_data['P1rh1']
    pw1r = raw_data['pw1']
    pw2r = raw_data['pw2']
    pw3br = raw_data['pw3b']
    pw6r = raw_data['pw6']
    pw7r = raw_data['pw7']
    Drhr = raw_data['Drh']
    Drh1r = raw_data['Drh1']
    Drh2r = raw_data['Drh2']
    Dsepr = raw_data['Dsep']
    Dsepwr = raw_data['Dsepw']
    T4r = raw_data['T4']
    t9r = raw_data['t9']
    t10r = raw_data['t10']
    tw1r = raw_data['tw1']
    tw2r = raw_data['tw2']
    tw3br = raw_data['tw3b']
    tw6r = raw_data['tw6']
    tw7r = raw_data['tw7']
    td1r = raw_data['td1']
    td2r = raw_data['td2']
    D0r = raw_data['D0']
    D1r = raw_data['D1']
    D2r = raw_data['D2']
    D3r = raw_data['D3']
    D4r = raw_data['D4']
    D5r = raw_data['D5']
    D6r = raw_data['D6']
    DLr = raw_data['DL']
    D7_wr= raw_data['D7_w']

    #:= := := := := := := := := := 抽汽压损计算值 := := := := := := := := := := := % %
    cqys1 = (P1d - h1_in_P_d) / P1d
    cqys2 = (P2d- h2_in_P_d) / P2d
    cqys3 = (P3d - h3_in_P_d) / P3d
    cqys4 = (P4d - h4_in_P_d) / P4d
    cqys5 = (P5d- h5_in_P_d) / P5d
    cqys6 = (P6d - h6_in_P_d) / P6d
    cqys7 = (P7d - h7_in_P_d) / P7d
    cqys8 = (P1d- rh1_in_P_d_es_d) / P1d
    cqys9 = (P0d - rh2_in_P_d_es_d) / P0d
    cqys10 = (P3d - rh1_in_P_d_ms_d) / P3d
    cqys11 = (rh1_in_P_d_es_d - rh1_out_P_es_d) / rh1_in_P_d_es_d
    cqys12 = (rh2_in_P_d_es_d - rh2_out_P_es_d) / rh2_in_P_d_es_d
    cqys13 = (rh1_in_P_d_ms_d - rh2_in_P_d_ms_d) / rh1_in_P_d_ms_d
    cqys14 = (rh2_in_P_d_ms_d- rh2_out_P_ms_d) / rh2_in_P_d_ms_d
    cqys15 = (rh2_out_P_ms_d - lp_in_P_d) / rh2_out_P_ms_d
    cqys16 = (lp_in_P_d - h3_out_P_fw_d) / lp_in_P_d

    k = Ng / Ngd
    Dpai = Dpaid * k
    Drh2 = Drh2d * k
    Dh = Dhd * k

    delta_Dpai = 1
    while abs(delta_Dpai) >= 0.0001:
        delta_Drh2 = 1
        while abs(delta_Drh2) >= 0.0001:
            P1 = (P0 ** 2 - (P0d ** 2 - P1d ** 2)) ** 0.5
            P2 = P1 * P2d / P1d
            P3 = P2 * P3d / P2d
            P4 = P3 * P4d / P3d
            P5 = P4 * P5d / P4d
            P6 = P5 * P6d / P5d
            P7 = (Pcn ** 2 + ((Dpai / Dpaid) ** 2) * (P7d ** 2 - Pcnd ** 2)) ** 0.5
            tw1 = CP.PropsSI('T', 'P', P1 * (1 - cqys1) * 1e6, 'Q', 1, 'water') - 273.15 - sdc1
            tw2 = CP.PropsSI('T', 'P', P2 * (1 - cqys2) * 1e6, 'Q', 1, 'water') - 273.15 - sdc2
            tw3 = CP.PropsSI('T', 'P', P3 * (1 - cqys3) * (1 - cqys16) * 1e6, 'Q', 1,
                             'water') - 273.15 - sdc3
            tw4 = CP.PropsSI('T', 'P', P4 * (1 - cqys4) * 1e6, 'Q', 1, 'water') - 273.15 - sdc4
            tw5 = CP.PropsSI('T', 'P', P5 * (1 - cqys5) * 1e6, 'Q', 1, 'water') - 273.15 - sdc5
            tw6 = CP.PropsSI('T', 'P', P6 * (1 - cqys6) * 1e6, 'Q', 1, 'water') - 273.15 - sdc6
            tw7 = CP.PropsSI('T', 'P', P7 * (1 - cqys7) * 1e6, 'Q', 1, 'water') - 273.15 - sdc7
            datafw = 1.900
            td1 = tw2 + xdc1
            tw3b = tw3 + datafw
            td2 = tw3b + xdc2
            td4 = tw5 + xdc4
            td5 = tw5 + xdc5
            td6 = tw6 + xdc6
            td7 = tw7 + xdc7
            pw1 = pw3b
            pw2 = pw3b
            pw3 = P3 * (1 - cqys3) * (1 - cqys16)
            pw4 = Pwc
            pw5 = Pwc
            pw6 = Pwc
            pw7 = Pwc
            hw1 = CP.PropsSI('H', 'T', tw1 + 273.15, 'P', pw1 * 1e6, 'water') / 1e3
            hw2 = CP.PropsSI('H', 'T', tw2 + 273.15, 'P', pw2 * 1e6, 'water') / 1e3
            hw3 = CP.PropsSI('H', 'P', pw3 * 1e6, 'Q', 0, 'water') / 1e3
            hw3b = CP.PropsSI('H', 'T', tw3b + 273.15, 'P', pw3b * 1e6, 'water') / 1e3  # 给水泵出口焓值
            hw4 = CP.PropsSI('H', 'T', tw4 + 273.15, 'P', pw4 * 1e6, 'water') / 1e3
            hw5 = CP.PropsSI('H', 'T', tw5 + 273.15, 'P', pw5 * 1e6, 'water') / 1e3
            hw6 = CP.PropsSI('H', 'T', tw6 + 273.15, 'P', pw6 * 1e6, 'water') / 1e3
            hw7 = CP.PropsSI('H', 'T', tw7 + 273.15, 'P', pw7 * 1e6, 'water') / 1e3
            hwc = CP.PropsSI('H', 'P', Pcn * 1e6, 'Q', 0, 'water') / 1e3
            hwcpu = hwc + 2.4  # 凝升泵出口焓值
            hd1 = CP.PropsSI('H', 'T', td1 + 273.15, 'P', P1 * (1 - cqys1) * 1e6, 'water') / 1e3
            hd2 = CP.PropsSI('H', 'T', td2 + 273.15, 'P', P2 * (1 - cqys2) * 1e6, 'water') / 1e3
            hd4 = CP.PropsSI('H', 'T', td4 + 273.15, 'P', P4 * (1 - cqys4) * 1e6, 'water') / 1e3
            hd5 = CP.PropsSI('H', 'P', P5 * (1 - cqys5) * 1e6, 'Q', 0, 'water') / 1e3
            hd6 = CP.PropsSI('H', 'P', P6 * (1 - cqys6) * 1e6, 'Q', 0, 'water') / 1e3
            hd7 = CP.PropsSI('H', 'P', P7 * (1 - cqys7) * 1e6, 'Q', 0, 'water') / 1e3
            gama2 = hd1 - hd2
            gama3 = hd2 - (CP.PropsSI('H', 'P', P3 * (1 - cqys3) * 1e6, 'Q', 0, 'water')) / 1e3
            gama5 = hd4 - hd5
            gama6 = hd5 - hd6
            gama7 = hd6 - hd7
            gamac = hd7 - hwc
            Tao1 = hw1 - hw2
            Tao2 = hw2 - CP.PropsSI('H', 'T', tw3b + 273.15, 'P', pw3b * 1e6, 'water') / 1e3  # % % datafw为给水泵温升
            Tao3 = hw3 - hw4
            Tao4 = hw4 - hw5
            Tao5 = hw5 - hw6
            Tao6 = hw6 - hw7
            Tao7 = hw7 - hwc - 3
            x0 = 0.9950
            h0 = CP.PropsSI('H', 'P', P0 * 1e6, 'Q', x0, 'water') / 1e3

            y01 = unit.y01_predict(Dh)  #train

            x0r = design_data['x0']
            h0r = CP.PropsSI('H', 'P', P0r* 1e6, 'Q', x0r, 'water') / 1e3
            s1r = CP.PropsSI('S', 'H', h0r * 1e3, 'P', P0r * 1e6, 'water')
            x1r = design_data['x1']
            h1r = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', x1r, 'water') / 1e3
            h1sr = CP.PropsSI('H', 'P', P1r * 1e6, 'S', s1r, 'water') / 1e3
            y01_real = (h0r - h1r) / (h0r- h1sr)

            s1 = CP.PropsSI('S', 'H', h0 * 1e3, 'P', P0 * 1e6, 'water')
            h1 = h0 - (h0 - (CP.PropsSI('H', 'P', P1 * 1e6, 'S', s1, 'water')) / 1e3) * y01
            h1_st = CP.PropsSI('H', 'P', P1 * 1e6, 'Q', 1, 'water') / 1e3
            h1_sw = CP.PropsSI('H', 'P', P1 * 1e6, 'Q', 0, 'water') / 1e3
            x1 = (h1 - h1_sw) / (h1_st - h1_sw)
            T1 = CP.PropsSI('T', 'P', P1 * 1e6, 'Q', x1, 'water') - 273.15
            T0 = CP.PropsSI('T', 'P', P0 * 1e6, 'Q', x0, 'water') - 273.15  # 主蒸汽温度


            y12 = unit.y12_predict(Dh) #train
            x1r = design_data['x1']
            h1r = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', x1r, 'water') / 1e3
            s2r = CP.PropsSI('S', 'H', h1r * 1e3, 'P', P1r * 1e6, 'water')
            x2r = design_data['x2']
            h2r = CP.PropsSI('H', 'P', P2r * 1e6, 'Q', x2r, 'water') / 1e3
            h2sr = (CP.PropsSI('H', 'P', P2r * 1e6, 'S', s2r, 'water')) / 1e3
            y12_real = (h1r - h2r) / (h1r - h2sr)

            s2 = CP.PropsSI('S', 'H', h1 * 1e3, 'P', P1 * 1e6, 'water')
            h2 = h1 - (h1 - (CP.PropsSI('H', 'P', P2 * 1e6, 'S', s2, 'water')) / 1e3) * y12
            h2_st = CP.PropsSI('H', 'P', P2 * 1e6, 'Q', 1, 'water') / 1e3
            h2_sw = CP.PropsSI('H', 'P', P2 * 1e6, 'Q', 0, 'water') / 1e3
            x2 = (h2 - h2_sw) / (h2_st - h2_sw)
            T2 = CP.PropsSI('T', 'P', P2 * 1e6, 'Q', x2, 'water') - 273.15

            y23 = unit.y23_predict(Dh) #train
            x2r = design_data['x2']
            h2r = CP.PropsSI('H', 'P', P2r * 1e6, 'Q', x2r, 'water') / 1e3
            s3r = CP.PropsSI('S', 'H', h2r * 1e3, 'P', P2r * 1e6, 'water')
            x3r = design_data['x3']
            h3r = CP.PropsSI('H', 'P', P3r * 1e6, 'Q', x3r, 'water') / 1e3
            h3sr = (CP.PropsSI('H', 'P', P3r * 1e6, 'S', s3r, 'water')) / 1e3
            y23_real = (h2r - h3r) / (h2r - h3sr)

            s3 = CP.PropsSI('S', 'H', h2 * 1e3, 'P', P2 * 1e6, 'water')
            h3 = h2 - (h2 - (
                CP.PropsSI('H', 'P', P3 * 1e6, 'S', s3, 'water')) / 1e3) * y23  # % % h0 - dh * xiaolv
            h3_st = CP.PropsSI('H', 'P', P3 * 1e6, 'Q', 1, 'water') / 1e3
            h3_sw = CP.PropsSI('H', 'P', P3 * 1e6, 'Q', 0, 'water') / 1e3
            x3 = (h3 - h3_sw) / (h3_st - h3_sw)
            T3 = CP.PropsSI('T', 'P', P3 * 1e6, 'Q', x3, 'water') - 273.15
            Prh1 = P1 * (1 - cqys8)

            b1 = unit.b1_predict() #train
            x8r = design_data['x8']
            h8r = CP.PropsSI('H', 'P', P8r * 1e6, 'Q', x8r, 'water') / 1e3
            h9r = CP.PropsSI('H', 'T', t9r + 273.15, 'P', P9r * 1e6, 'water') / 1e3
            x1r = design_data['x1']
            h1r = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', x1r, 'water') / 1e3
            h1rh1_swr = CP.PropsSI('H', 'P', P1rh1r * 1e6, 'Q', 0, 'water') / 1e3
            b1_real = (Drhr * (h9r - h8r)) / (Drh1r * (h1r - h1rh1_swr))

            hrh1_st = CP.PropsSI('H', 'P', Prh1 * 1e6, 'Q', 1, 'water') / 1e3
            hrh1_sw = CP.PropsSI('H', 'P', Prh1 * 1e6, 'Q', 0, 'water') / 1e3
            xrh1 = (h1 - hrh1_sw) / (hrh1_st - hrh1_sw)
            trh1 = CP.PropsSI('T', 'P', Prh1 * 1e6, 'Q', xrh1, 'water') - 273.15
            t9 = trh1 - sdc8
            P9 = P3 * (1 - cqys10) * (1 - cqys13)  # 一级再热器出口压力
            h9 = CP.PropsSI('H', 'T', t9 + 273.15, 'P', P3 * (1 - cqys10) * (1 - cqys13) * 1e6, 'water') / 1e3
            P1rh1 = Prh1 * (1 - cqys11)
            h1rh1_sw = CP.PropsSI('H', 'P', P1rh1 * 1e6, 'Q', 0, 'water') / 1e3
            Dh = D0 - Drh2

            b2 = unit.b2_predict() #train
            h9r = CP.PropsSI('H', 'T', t9r + 273.15, 'P', P9r * 1e6, 'water') / 1e3
            h10r = CP.PropsSI('H', 'T', t10r + 273.15, 'P', P10r * 1e6, 'water') / 1e3
            x0r = design_data['x0']
            h0r = CP.PropsSI('H', 'P', P0r * 1e6, 'Q', x0r, 'water') / 1e3
            h0rh2_swr = CP.PropsSI('H', 'P', P0rh2r * 1e6, 'Q', 0, 'water') / 1e3
            b2_real = (Drhr * (h10r - h9r)) / (Drh2r * (h0r - h0rh2_swr))

            Prh2 = P0 * (1 - cqys9)
            hrh2_st = CP.PropsSI('H', 'P', Prh2 * 1e6, 'Q', 1, 'water') / 1e3
            hrh2_sw = CP.PropsSI('H', 'P', Prh2 * 1e6, 'Q', 0, 'water') / 1e3
            xrh2 = (h0 - hrh2_sw) / (hrh2_st - hrh2_sw)
            trh2 = CP.PropsSI('T', 'P', Prh2 * 1e6, 'Q', xrh2, 'water') - 273.15
            t10 = trh2 - sdc9
            h10 = CP.PropsSI('H', 'T', t10 + 273.15, 'P',
                             P3 * (1 - cqys10) * (1 - cqys13) * (1 - cqys14) * 1e6,
                             'water') / 1e3
            P0rh2 = Prh2 * (1 - cqys12)
            h0rh2_sw = CP.PropsSI('H', 'P', P0rh2 * 1e6, 'Q', 0, 'water') / 1e3
            Drh = Drh2 * b2 * (h0 - h0rh2_sw) / (h10 - h9)
            Psepw = P3 * (1 - cqys10)  # 汽水分离器出口压力

            bsep = unit.bsep_predict() #train
            x3r = design_data['x3']
            bsep_real = Dsepwr / (Dsepr * (1 - x3r))

            Dsepw = (bsep * Drh * (1 - x3)) / (1 - bsep * (1 - x3))
            hsepw = CP.PropsSI('H', 'P', P3 * (1 - cqys10) * 1e6, 'Q', 0, 'water') / 1e3
            Dsep = Dsepw + Drh

            c1 = unit.c1_predict() #train
            hw1r = CP.PropsSI('H', 'T', tw1r + 273.15, 'P', pw1r * 1e6, 'water') / 1e3
            hw2r = CP.PropsSI('H', 'T', tw2r + 273.15, 'P', pw2r * 1e6, 'water') / 1e3
            h10r = CP.PropsSI('H', 'T', t10r + 273.15, 'P', P10r * 1e6, 'water') / 1e3
            h9r = CP.PropsSI('H', 'T', t9r + 273.15, 'P', P9r * 1e6, 'water') / 1e3
            x0r = design_data['x0']
            h0r = CP.PropsSI('H', 'P', P0r * 1e6, 'Q', x0r, 'water') / 1e3
            h0rh2_swr = CP.PropsSI('H', 'P', P0rh2r * 1e6, 'Q', 0, 'water') / 1e3
            hd1r = CP.PropsSI('H', 'T', td1r + 273.15, 'P', P1r * (1 - cqys1) * 1e6, 'water') / 1e3
            # P1 * (1 - cqys1) * 1e6   一级高压加热器入口的压力
            x1r = design_data['x1']
            h1r = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', x1r, 'water') / 1e3
            h1_swr = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', 0, 'water') / 1e3
            c1_real = ((D0r * (hw1r - hw2r) - (Drhr * (h10r - h9r)) / (Drh2r * (h0r - h0rh2_swr)) * Drh2r * (h0rh2_swr - hd1r) - (
                    1 - (Drhr * (h10r - h9r)) / (Drh2r * (h0r - h0rh2_swr))) * Drh2r * (h0r - hd1r)) / D1r - (h1_swr - hd1r)) / (
                             h1r - h1_swr)

            D1 = ((D0) * Tao1 - b2 * Drh2 * (h0rh2_sw - hd1) - (1 - b2) * Drh2 * (h0 - hd1)) / (
                    c1 * (h1 - hd1) + (1 - c1) * (
                    CP.PropsSI('H', 'P', P1 * 1e6, 'Q', 0, 'water') / 1e3 - hd1))
            Drh1 = D1 * 1.4264
            h8 = h9 - (Drh1 * b1 * (h1 - h1rh1_sw)) / Drh   # 汽水分离器出口焓值

            c2 = unit.c2_predict() #train
            hw2r = CP.PropsSI('H', 'T', tw2r + 273.15, 'P', pw2r * 1e6, 'water') / 1e3
            hw3br = CP.PropsSI('H', 'T', tw3br + 273.15, 'P', pw3br * 1e6, 'water') / 1e3
            h9r = CP.PropsSI('H', 'T', t9r + 273.15, 'P', P9r * 1e6, 'water') / 1e3
            x8r = design_data['x8']
            h8r = CP.PropsSI('H', 'P', P8r * 1e6, 'Q', x8r, 'water') / 1e3
            x1r = design_data['x1']
            h1r = CP.PropsSI('H', 'P', P1r * 1e6, 'Q', x1r, 'water') / 1e3
            h1rh1_swr = CP.PropsSI('H', 'P', P1rh1r * 1e6, 'Q', 0, 'water') / 1e3
            hd1r = CP.PropsSI('H', 'T', td1r + 273.15, 'P', P1r * (1 - cqys1) * 1e6, 'water') / 1e3
            # P1 * (1 - cqys1) * 1e6   一级高压加热器入口的压力
            hd2r = CP.PropsSI('H', 'T', td2r + 273.15, 'P', P2r * (1 - cqys2) * 1e6, 'water') / 1e3
            # P2 * (1 - cqys2) * 1e6   二级高压加热器入口的压力
            x2r = design_data['x2']
            h2r = CP.PropsSI('H', 'P', P2r * 1e6, 'Q', x2r, 'water') / 1e3
            h2_swr = CP.PropsSI('H', 'P', P2r * 1e6, 'Q', 0, 'water') / 1e3
            c2_real = ((D0r * (hw2r - hw3br) - (Drhr * (h9r - h8r)) / (Drh1r * (h1r - h1rh1_swr)) * Drh1r * (h1rh1_swr - hd2r) - (
                    1 - (Drhr * (h9r - h8r)) / (Drh1r * (h1r - h1rh1_swr))) * Drh1r * (h1r - hd2r) - (D1r + Drh2r) * (
                               hd1r - hd2r)) / D2r - (h2_swr - hd2r)) / (h2r - h2_swr)

            D2 = ((D0) * Tao2 - b1 * Drh1 * (h1rh1_sw - hd2) - (1 - b1) * Drh1 * (h1 - hd2) - (
                    D1 + Drh2) * gama2) / (
                         c2 * (h2 - hd2) + (1 - c2) * (
                         CP.PropsSI('H', 'P', P2 * 1e6, 'Q', 0, 'water') / 1e3 - hd2))

            D3 = ((D0 - D1 - D2 - Drh1 - Drh2 - Dsepw) * Tao3 - (D1 + D2 + Drh1 + Drh2) * (
                    hd2 - hw3) - Dsepw * (
                          hsepw - hw3)) / (h3 - hw4)

            delta_Drh2 = D3 + D1 + D2 + Drh1 + Drh2 + Drh + Dsepw + Dsg4 + Dsgh + Dsg1 - D0
            if abs(delta_Drh2) > 0.0001:
                Drh2 = Drh2 - delta_Drh2 / 100 * 2

        Dhpai = Dsep + D3 + Dsg3  # 高压缸排汽流量
        D34 = Drh

        y34 = unit.y34_predict(D34) #train
        h10r = CP.PropsSI('H', 'T', t10r + 273.15, 'P', P10r * 1e6, 'water') / 1e3
        s4r = CP.PropsSI('S', 'H', h10r * 1e3, 'P', Prhr * 1e6, 'water')
        h4r = CP.PropsSI('H', 'T', T4r + 273.15, 'P', P4r * 1e6, 'water') / 1e3
        h4sr = (CP.PropsSI('H', 'P', P4r * 1e6, 'S', s4r, 'water')) / 1e3
        y34_real = (h10r - h4r) / (h10r - h4sr)

        Prh = P3 * (1 - cqys10) * (1 - cqys13) * (1 - cqys14) * (1 - cqys15)
        s4 = CP.PropsSI('S', 'H', h10 * 1e3, 'P', Prh * 1e6, 'water')
        h4 = h10 - (h10 - (
            CP.PropsSI('H', 'P', P4 * 1e6, 'S', s4, 'water')) / 1e3) * y34  # % % h0 - dh * xiaolv
        T4 = CP.PropsSI('T', 'H', h4 * 1e3, 'P', P4 * 1e6, 'water') - 273.15
        Dc3 = D0 - D1 - D2 - D3 - Drh1 - Drh2 - Dsepw
        D4 = Dc3 * Tao4 / (h4 - hd4)
        D45 = D34 - D4

        y45 = unit.y45_predict(D45) #train
        # print(y45)
        h4r = CP.PropsSI('H', 'T', T4r + 273.15, 'P', P4r * 1e6, 'water') / 1e3
        s5r = CP.PropsSI('S', 'H', h4r * 1e3, 'P', P4r * 1e6, 'water')
        x5r = design_data['x5']
        h5r = CP.PropsSI('H', 'P', P5r * 1e6, 'Q', x5r, 'water') / 1e3
        h5sr = (CP.PropsSI('H', 'P', P5r * 1e6, 'S', s5r, 'water')) / 1e3
        y45_real = (h4r - h5r) / (h4r - h5sr)

        s5 = CP.PropsSI('S', 'H', h4 * 1e3, 'P', P4 * 1e6, 'water')
        h5 = h4 - (h4 - (
            CP.PropsSI('H', 'P', P5 * 1e6, 'S', s5, 'water')) / 1e3) * y45  # % % h0 - dh * xiaolv
        T5 = CP.PropsSI('T', 'P', P5 * 1e6, 'Q', 1, 'water') - 273.15

        D5 = ((Dc3 - D4) * Tao5 - D4 * gama5) / (h5 - hd5 + hw5 - hw6)
        D56 = D45 - D5

        y56 = unit.y56_predict(D56) #train
        x5r = design_data['x5']
        h5r = CP.PropsSI('H', 'P', P5r * 1e6, 'Q', x5r, 'water') / 1e3
        s6r = CP.PropsSI('S', 'H', h5r * 1e3, 'P', P5r * 1e6, 'water')
        x6r = design_data['x6']
        h6r = CP.PropsSI('H', 'P', P6r * 1e6, 'Q', x6r, 'water') / 1e3
        h6sr = (CP.PropsSI('H', 'P', P6r * 1e6, 'S', s6r, 'water')) / 1e3
        y56_real = (h5r - h6r) / (h5r - h6sr)

        s6 = CP.PropsSI('S', 'H', h5 * 1e3, 'P', P5 * 1e6, 'water')
        h6 = h5 - (h5 - (
            CP.PropsSI('H', 'P', P6 * 1e6, 'S', s6, 'water')) / 1e3) * y56  # % % h0 - dh * xiaolv
        h6_st = CP.PropsSI('H', 'P', P6 * 1e6, 'Q', 1, 'water') / 1e3
        h6_sw = CP.PropsSI('H', 'P', P6 * 1e6, 'Q', 0, 'water') / 1e3
        x6 = (h6 - h6_sw) / (h6_st - h6_sw)
        T6 = CP.PropsSI('T', 'P', P6 * 1e6, 'Q', x6, 'water') - 273.15
        Dc5 = Dc3 - D4 - D5

        c6 = unit.c6_predict() #train
        Dc5r = D0r - D1r - D2r - D3r - Drh1r - Drh2r - Dsepwr - D4r - D5r
        x6r = design_data['x6']
        h6r = CP.PropsSI('H', 'P', P6r * 1e6, 'Q', x6r, 'water') / 1e3
        hw6r = CP.PropsSI('H', 'T', tw6r + 273.15, 'P', pw6r * 1e6, 'water') / 1e3  # 修改2022.9.11
        hw7r = CP.PropsSI('H', 'T', tw7r + 273.15, 'P', pw7r * 1e6, 'water') / 1e3  # 修改2022.9.11
        h6_swr = CP.PropsSI('H', 'P', P6r * 1e6, 'Q', 0, 'water') / 1e3
        hd6r = CP.PropsSI('H', 'P', P6r * (1 - cqys6) * 1e6, 'Q', 0, 'water') / 1e3
        c6_real = (Dc5r * (hw6r - hw7r) / D6r - (h6_swr - hd6r)) / (h6r - h6_swr)

        D6 = Dc5 * Tao6 / (c6 * (h6 - hd6) + (1 - c6) * (h6_sw - hd6))
        D6_w = D6 * (1 - c6)  # H6疏水流量

        cL = unit.cL_predict() #train
        cL_real = DLr / (Drhr - D4r - D5r - D6r)

        DL = cL * (Drh - D4 - D5 - D6)
        hL_sw = CP.PropsSI('H', 'P', PL * 1e6, 'Q', 0, 'water') / 1e3
        D67 = D56 - D6

        y67 = unit.y67_predict(D67) #train
        x6r = design_data['x6']
        h6r = CP.PropsSI('H', 'P', P6r * 1e6, 'Q', x6r, 'water') / 1e3
        s7r = CP.PropsSI('S', 'H', h6r * 1e3, 'P', P6r * 1e6, 'water')
        x7r = design_data['x7']
        h7r = CP.PropsSI('H', 'P', P7r * 1e6, 'Q', x7r, 'water') / 1e3
        h7sr = (CP.PropsSI('H', 'P', P7r * 1e6, 'S', s7r, 'water')) / 1e3
        y67_real = (h6r - h7r) / (h6r - h7sr)

        s7 = CP.PropsSI('S', 'H', h6 * 1e3, 'P', P6 * 1e6, 'water')
        h7 = h6 - (h6 - (CP.PropsSI('H', 'P', P7 * 1e6, 'S', s7, 'water')) / 1e3) * y67
        h7_st = CP.PropsSI('H', 'P', P7 * 1e6, 'Q', 1, 'water') / 1e3
        h7_sw = CP.PropsSI('H', 'P', P7 * 1e6, 'Q', 0, 'water') / 1e3
        x7 = (h7 - h7_sw) / (h7_st - h7_sw)
        T7 = CP.PropsSI('T', 'P', P7 * 1e6, 'Q', x7, 'water') - 273.15
        hwsg = (Dsg3 * (h3 - 415) / (0.1 * Dc5)) + hwc + 2.4
        hdc = (0.1 * Dc5 * hwsg + 0.9 * Dc5 * (hwc + 2.4)) / Dc5
        Tdc = CP.PropsSI('T', 'H', hdc * 1e3, 'P', Pwc * 1e6, 'water') - 273.15
        Tddc = Tdc + 5
        hddc = CP.PropsSI('H', 'T', Tddc + 273.15, 'Q', 0, 'water') / 1e3

        c7 = unit.c7_predict() #train
        D67 = Drhr - D4r - D5r - D6r
        DLr = cL_real * (Drhr - D4r - D5r - D6r)
        c7_real = D7_wr / (D67 - DLr)

        D7_w = c7 * (D67 - DL)
        D7_t = (Dc5 * (hw7 - hdc) - D6 * (hd6 - hddc) - DL * (hL_sw - hddc) - D7_w * (h7_sw - hddc)) / (
                h7 - hddc)
        D7 = D7_w + D7_t
        Dpai_c = Drh - D4 - D5 - D6 - D7 - DL
        delta_Dpai = (Dpai - Dpai_c) / Dpai_c
        if abs(delta_Dpai) > 0.0001:
            Dpai = Dpai * (1 - (delta_Dpai) * 0.1)

    y7c = unit.y7c_predict(Dpai) #train
    x7r = design_data['x7']
    h7r = CP.PropsSI('H', 'P', P7r * 1e6, 'Q', x7r, 'water') / 1e3
    s7cr = CP.PropsSI('S', 'H', h7r * 1e3, 'P', P7r * 1e6, 'water')
    xcr = design_data['xc']
    hcr = CP.PropsSI('H', 'P', Pcnr * 1e6, 'Q', xcr, 'water') / 1e3
    hcsr = (CP.PropsSI('H', 'P', Pcnr * 1e6, 'S', s7cr, 'water')) / 1e3
    y7c_real = (h7r - hcr) / (h7r - hcsr)

    s7c = CP.PropsSI('S', 'H', h7 * 1e3, 'P', P7 * 1e6, 'water')
    hc = h7 - (h7 - (CP.PropsSI('H', 'P', Pcn * 1e6, 'S', s7c, 'water')) / 1e3) * y7c
    hc_st = CP.PropsSI('H', 'P', Pcn * 1e6, 'Q', 1, 'water') / 1e3
    hc_sw = CP.PropsSI('H', 'P', Pcn * 1e6, 'Q', 0, 'water') / 1e3
    xc = (hc - hc_sw) / (hc_st - hc_sw)
    Tc = CP.PropsSI('T', 'P', Pcn * 1e6, 'Q', xc, 'water') - 273.15
    delta_hc = hc - hc_sw

    yg = 0.996
    ym = 0.995

    W = (Dh * h0 - D1 * c1 * h1 - D1 * (1 - c1) * h1_sw - Drh1 * h1 - D2 * c2 * h2 - D2 * (
            1 - c2) * h2_sw - (Dh - D1 - D2 - Drh1) * h3) + (Drh * h10 - D4 * h4 - D5 * h5 - D6 * c6 * h6 - D6 * (
            1 - c6) * h6_sw - DL * hL_sw - D7_t * h7 - D7_w * h7_sw - Dpai * hc)
    W = W / 3.6 * yg * ym
    # Qpai = Dpai * (hc - CP.PropsSI('H', 'P', Pcn * 1e6, 'Q', 0, 'water') / 1e3) + (D7 + D6) * (
    #         hd7 - CP.PropsSI('H', 'P', Pcn * 1e6, 'Q', 0, 'water') / 1e3)
    # zhenjixiaolv = W / (W + Qpai / 3.6)
    # Q0 = D0 * (h0 - hw1)
    # q0 = Q0 / Ng * 1e3
    # q0shiji = Q0 / W * 1e3

    real = {}
    real['Dh'] = Dh
    real['D34'] = D34
    real['D45'] = D45
    real['D56'] = D56
    real['D67'] = D67
    real['Dpai'] = Dpai
    real['Tc'] = Tc
    real['Dpai_real'] = Dpai
    real['delta_hc_real'] = delta_hc
    real['y01_real'] = y01_real
    real['y12_real'] = y12_real
    real['y23_real'] = y23_real
    real['y34_real'] = y34_real
    real['y45_real'] = y45_real
    real['y56_real'] = y56_real
    real['y67_real'] = y67_real
    real['y7c_real'] = y7c_real
    real['b1_real'] = b1_real
    real['b2_real'] = b2_real
    real['bsep_real'] = bsep_real
    real['c1_real'] = c1_real
    real['c2_real'] = c2_real
    real['c6_real'] = c6_real
    real['c7_real'] = c7_real
    real['cL_real'] = cL_real


    pred = {}
    pred['y01_pred'] = y01
    pred['y12_pred'] = y12
    pred['y23_pred'] = y23
    pred['y34_pred'] = y34
    pred['y45_pred'] = y45
    pred['y56_pred'] = y56
    pred['y67_pred'] = y67
    pred['y7c_pred'] = y7c
    pred['b1_pred'] = b1
    pred['b2_pred'] = b2
    pred['bsep_pred'] = bsep
    pred['c1_pred'] = c1
    pred['c2_pred'] = c2
    pred['c6_pred'] = c6
    pred['c7_pred'] = c7
    pred['cL_pred'] = cL

    return real, pred, W

# if __name__ == '__main__':
#     Pcn = 0.0037
    # raw_data =
    # config_path = './config/config.ini'
    # row = thermal_cycle_main(0.0037, raw_data, design_data, error_num)
    # print(row)
    #创建参数数据库
    # conn = sqlite3.connect('./data/dt.db')
    # c = conn.cursor()
    # sql = '''CREATE TABLE dt_thermal_cycle_param (id int primary key not null, date_time CHAR NOT NULL, insert_time char NOT NULL,
    #                          P0 real not null,
    #                          D0 real not null,
    #                          Ngd real not null,
    #                          P0d real not null,
    #                          P1d real not null,
    #                          P2d real not null,
    #                          P3d real not null,
    #                          P4d real not null,
    #                          P5d real not null,
    #                          P6d real not null,
    #                          PL real not null,
    #                          P7d real not null,
    #                          Pcnd real not null,
    #                          pw3b real not null,
    #                          Pwc real not null,
    #                          tw1d real not null,
    #                          tw2d real not null,
    #                          tw3bd real not null,
    #                          tw3d real not null,
    #                          tw4d real not null,
    #                          tw5d real not null,
    #                          tw6d real not null,
    #                          tw7d real not null,
    #                          twcd real not null,
    #                          td1d real not null,
    #                          td2d real not null,
    #                          td4d real not null,
    #                          td5d real not null,
    #                          td6d real not null,
    #                          td7d real not null,
    #                          h1_in_P_d real not null,
    #                          h2_in_P_d real not null,
    #                          h3_in_P_d real not null,
    #                          h4_in_P_d real not null,
    #                          h5_in_P_d real not null,
    #                          h6_in_P_d real not null,
    #                          h7_in_P_d real not null,
    #                          rh1_in_P_d_es_d real not null,
    #                          rh2_in_P_d_es_d real not null,
    #                          rh1_in_P_d_ms_d real not null,
    #                          rh1_out_P_es_d real not null,
    #                          rh2_out_P_es_d real not null,
    #                          rh2_in_P_d_ms_d real not null,
    #                          rh2_out_P_ms_d real not null,
    #                          lp_in_P_d real not null,
    #                          h3_out_P_fw_d real not null,
    #                          sdc1 real not null,
    #                          sdc2 real not null,
    #                          sdc3 real not null,
    #                          sdc4 real not null,
    #                          sdc5 real not null,
    #                          sdc6 real not null,
    #                          sdc7 real not null,
    #                          sdc8 real not null,
    #                          sdc9 real not null,
    #                          xdc1 real not null,
    #                          xdc2 real not null,
    #                          xdc3 real not null,
    #                          xdc4 real not null,
    #                          xdc5 real not null,
    #                          xdc6 real not null,
    #                          xdc7 real not null,
    #                          h1d real not null,
    #                          h2d real not null,
    #                          h3d real not null,
    #                          h4d real not null,
    #                          h5d real not null,
    #                          h6d real not null,
    #                          h7d real not null,
    #                          hcd real not null,
    #                          hsg3 real not null,
    #                          t1d real not null,
    #                          t2d real not null,
    #                          t3d real not null,
    #                          t4d real not null,
    #                          t5d real not null,
    #                          t6d real not null,
    #                          t7d real not null,
    #                          Dsgh real not null,
    #                          Dsg1 real not null,
    #                          DsgL real not null,
    #                          Dsg2 real not null,
    #                          Dsg3 real not null,
    #                          Dsg4 real not null,
    #                          Ng real not null,
    #                          Drh2d real not null,
    #                          Dhd real not null,
    #                          Dpaid real not null,
    #                          )
    # '''
    # c.execute(sql)

