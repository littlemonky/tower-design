from asset_config import Unit,CoolingTower,HeatExchanger,Environment,Wet_section,Machanical_tower
import math
import numpy as np
unit = Unit()
CT=CoolingTower()
HE=HeatExchanger()
EN=Environment()
We=Wet_section()
tower = Machanical_tower()
## 基于湿冷塔的干湿联合##
def cooling_tower_main1(h3,d3,h6,d6,h9,d9,d0,Lfi,Afrw,Afrd,l,Lte,ntb,Do,Di,nr,nwp,aj,nb,Ta1,RH,pa1,Tin,mw):
    # TODO
    # tower parameter
    d5=151.93*1.117*1.117

    A6=math.pi * (d6/2) ** 2
    A9 = math.pi * (d9 / 2) ** 2
    A5 = math.pi * (d5 / 2) ** 2
    h8=h6
    # dry section
    Ats = np.pi * Di ** 2 / 4
    Twb1=19.7+273.15

    # opration
    delta_w1 = 0.1
    while abs(delta_w1) > 0.0001:
        # 湿度计算
        if delta_w1 > 0:
            Twb1 += abs(delta_w1)
        else:
            Twb1 -= abs(delta_w1)
        pvwb1,w1,_=EN.Environment_calculate(Twb1,Ta1,pa1)
        pvs1,_,_=EN.Environment_calculate(Ta1,Ta1,pa1)
        RHc = pa1 * w1 / (0.622 + w1) / pvs1
        # 计算下一个迭代的 delta_w1
        delta_w1 = RH - RHc
    cpa1,cpw1,cpv1=EN.cp_calculate(Ta1)
    delta_p134=pa1*(1-((1-(0.00975*(h3+Lfi/2)/Ta1))**(3.5*(1+w1)*(1-w1/(w1+0.62198)))))
    hai = cpa1 * (Ta1 - 273.15) + w1 * (EN.ifgwo + cpv1 * (Ta1 - 273.15))
    rhoav1,rhoa1=EN.rhoa_calculate(Ta1,w1,pa1)
    Ta3,pa3=EN.Tan_calculate(Ta1,pa1,h3,w1)
    nian_a1,nian_v1,nian_av1=EN.nian_calculate(Ta1,w1)
    Ta6,pa6=EN.Tan_calculate(Ta1,pa1,h6,w1)
    cpa6, cpw6, cpv6 = EN.cp_calculate(Ta6)
    w6=w1
    rhoav6, rhoa6 = EN.rhoa_calculate(Ta6, w6, pa6)
    ha6=cpa6*(Ta6-273.15)+w6*(EN.ifgwo+cpv6*(Ta6-273.15))
    w7=w6
    Ta10, pa10 = EN.Tan_calculate(Ta1, pa1, h9, w1)
    rhoav10,_=EN.rhoa_calculate(Ta10,w1,pa10)

    # integration initial
    _,pa8=EN.Tan_calculate(Ta1,pa1,h6,w1)
    pa8=pa8-45
    v06=1.55
    mwd=mw
    mww=mwd
    Tind=Tin
    Twod = (Tind * 3 + Ta6) / 4

    # 循环嵌套
    delta_pf = 0.51
    # 最外侧的大循环，计算 pa8
    while abs(delta_pf) >= 0.5:
        # 更新 pa8 的值
        if delta_pf > 0:
            pa8 += min(0.5, 0.5 * delta_pf)
        else:
            pa8 -= min(0.5, 0.5 * abs(delta_pf))
        # 嵌套第二个循环，计算 v06
        delta_fl_bad = 0.21
        while abs(delta_fl_bad) >= 0.2:
            # 更新 v06 的值
            if delta_fl_bad > 0:
                v06 += min(0.002, abs(delta_fl_bad))
            else:
                v06 -= min(0.002, abs(delta_fl_bad))
            # 嵌套最里侧的第三个循环，计算 Twod
            delta_en_bad = 0.001
            while abs(delta_en_bad) >= 1e-5:
                if delta_en_bad > 0:
                    Twod += min(0.2, 0.1 * abs(delta_en_bad))
                else:
                    Twod -= min(0.2, 0.1 * abs(delta_en_bad))

                Twdm = (Tind + Twod) / 2
                _,cpwdm,_=EN.cp_calculate(Twdm)
                Qwd = mwd * cpwdm * (Tind - Twod)
                ma67 = v06 * Afrd * rhoa6
                Ta7 = Qwd / (ma67 * cpa6) + Ta6
                HA=HE.HA_calculate(Tind,Twod,mw,cpw1,Ats,nb,ntb,nwp,Lte,v06,Afrd)
                Ft,delta_t=HE.Ft_calculate(Tind,Ta7,Twod,Ta6)
                Qhd=Ft*HA*delta_t
                delta_en_bad = (Qwd - Qhd) / Qwd


            Ta67=(Ta6+Ta7)/2
            rhoa7 = pa8 / (EN.R * Ta7)
            rhoa67 = 2 / (1 / rhoa7 + 1 / rhoa6)
            va7 = ma67 / rhoa7 / Afrd
            Hd = pa6 - pa8
            Kheaj=HE.K_dry(v06,aj,rhoa7,rhoa6)
            Zd = Kheaj * (ma67 / Afrd) **2 / (2 * rhoa67) + rhoa7 * va7 ** 2 / 2
            delta_fl_bad = Hd - Zd



        # 更新 delta_fl_bad 为新的误差值
        ## 空冷段计算完，开始计算湿冷段
        Tinw = Twod
        Twow = (Tinw + 2 * Twb1 + Ta1) / 4 #assume
        Twwm = (Tinw + Twow) / 2
        _,cpwm,_=EN.cp_calculate(Twwm)

        Ta5 = (Tinw + Twow) / 2
        Twb5 = Ta5
        pvwb5,w5,_=EN.Environment_calculate(Twb5,Ta5,pa8)
        cpa5, cpw5, cpv5 = EN.cp_calculate(Ta5)
        ha5 = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
        mav15 = mww * cpwm * (Tinw - Twow) / (ha5 - hai)
        epsTa5 = CT.epsTan(Ta5, w5, cpw5, cpv5, cpa5, pa8)
        delta_p348w = pa8 * (1 - (1 + epsTa5 * (h8 - h3 - Lfi / 2) / Ta5) ** (-0.021233 * (1 + w5) / (epsTa5 * (w5 + 0.622))))
        pa5 = pa8 + delta_p348w
        delta_fl_pa8w = 0.51
        while abs(delta_fl_pa8w) >= 0.5:  # 外侧循环计算 pa8
            if delta_fl_pa8w > 0:
                pa5 = pa5 - min(10, delta_fl_pa8w)
            else:
                pa5 = pa5 - max(-10, delta_fl_pa8w)

            delta_fl_baw = 0.21
            while abs(delta_fl_baw) >= 0.2:
                if delta_fl_baw > 0:
                    mav15 = mav15 + min(10000, 300 * delta_fl_baw)
                else:
                    mav15 = mav15 - min(9000, abs(299 * delta_fl_baw))

                delta_en_baw = 0.001
                while abs(delta_en_baw) >= 0.0001:
                    # fill selection (PVC)
                    if delta_en_baw > 0:
                        Twow = Twow - min(0.2, 0.1 * abs(delta_en_baw))
                    else:
                        Twow = Twow + min(0.2, 0.1 * abs(delta_en_baw))

                    Twwm = (Tinw + Twow) / 2
                    _,cpwm,_=EN.cp_calculate(Twwm)
                    rhowo = (1.49343 * 10 ** (-3) - 3.7164 * 10 ** (-6) * Twow + 7.09782 * 10 ** (
                        -9) * Twow ** 2 - 1.90321 * 10 ** (-20) * Twow ** 6) ** (-1)
                    ten_wo = 5.148103 * 10 ** (-2) + 3.998714 * 10 ** (-4) * Twow - 1.4721869 * 10 ** (
                        -6) * Twow ** 2 + 1.21405335 * 10 ** (-9) * Twow ** 3
                    anian = 3.061 * 10 ** (-6) * (rhowo ** 4 * 9.8 ** 9 / ten_wo) ** 0.25
                    aden = 998 / rhowo
                    av = 73.298 * (9.8 ** 5 * ten_wo ** 3 / rhowo ** 3) ** 0.25
                    aL = 6.122 * (9.8 * ten_wo / rhowo) ** 0.25
                    Gw = mww / Afrw
                    vw3 = Gw / rhowo
                    delta_Ta5 = 0.011
                    while abs(delta_Ta5) >= 0.01:
                        if delta_Ta5 > 0:
                            Ta5 = Ta5 - min(0.01, 10 * abs(delta_Ta5))
                        else:
                            Ta5 = Ta5 + min(0.01, 9 * abs(delta_Ta5))

                        hao = mww * cpwm * (Tinw - Twow) / mav15 + hai
                        Twb5 = Ta5
                        pvwb5,_,_ = EN.Environment_calculate(Twb5, Ta5, pa8)
                        w5 = 0.62509 * pvwb5 / (pa5 - pvwb5)
                        ha5c = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
                        delta_Ta5 = (ha5c - hao) / hao

                    ma15 = 2 * mav15 / (2 + w1 + w5)
                    mav1 = ma15 * (1 + w1)
                    Ga = ma15 / Afrw
                    vav3 = mav1 / (rhoav1 * Afrw)
                    Nw=We.Merkel1(pa1, Ta1, Twow,nian_av1,rhoav1,Ga,Gw,vav3,aden,h3,w1,Lfi,anian,rhowo,aL,av)
                    Ncc=We.Merkel2(mww,Twow,Tinw,cpw1,mav15,hai,pa1)
                    delta_en_baw = Nw - Ncc

                rhoav5,_=EN.rhoa_calculate(Ta5,w5,pa5)
                mav5 = ma15 * (1 + w5)
                vav5 = mav5 / (rhoav5 * A5)
                Ga = ma15 / Afrw
                Gav1 = mav1 / Afrw
                Gav5 = mav5 / Afrw
                Gav15 = mav15 / Afrw
                rhoav15 = 2 / (1 / rhoav1 + 1 / rhoav5)
                nian_a5, nian_v5, nian_av5=EN.nian_calculate(Ta5,w5)
                Ktsfi, Kctfi, Krzfi, Kfsfi_Kctcfi, Kfi, Kctefi, Kspfi, Kwdfi, Kdefi=We.K_wet(rhoav15, rhoav1, mav1, mav15, Gav1, Gav5, rhoav5, mav5, Afrw, d3, h3, Lfi, Gw, Ga, aden, anian, nian_av1, nian_av5, aL, av, vw3,Gav15,vav3)
                K_fi =Ktsfi+Kctfi+Krzfi+Kfsfi_Kctcfi+Kfi+Kctefi+Kspfi+Kwdfi+Kdefi
                Hw = pa1 - pa5 - delta_p134
                Zw = K_fi * (mav15 / Afrw) ** 2 / (2 * rhoav15)
                delta_fl_baw = (Hw - Zw)

            epsTa5 = CT.epsTan(Ta5,w5,cpw5,cpv5,cpa5,pa5)
            Ta8w = Ta5 + epsTa5 * (h6 - h3 - Lfi / 2)
            rhoav8w = (1 + w5) * (1 - w5 / (w5 + 0.62198)) * pa8 / (EN.R * Ta8w)
            vav8w = mav5 / (rhoav8w * A6)
            delta_p348w = pa5 * (1 - (1 + epsTa5 * (h8 - h3 - Lfi / 2) / Ta5) ** (
                        -0.021233 * (1 + w5) / (epsTa5 * (w5 + 0.622))))
            pa8w = pa1 - delta_p134 - delta_p348w - K_fi * (mav15 / Afrw) ** 2 / (
                        2 * rhoav15) - rhoav8w * vav8w ** 2 / 2
            delta_fl_pa8w = pa8w - pa8

        cpa7,_,cpv7=EN.cp_calculate(Ta7)
        ha7 = cpa7 * (Ta7 - 273.15) + w7 * (EN.ifgwo + cpv7 * (Ta7 - 273.15))
        mav8 = ma15 * (1 + w5) + ma67 * (1 + w7)
        w8 = (w5 * ma15 + w7 * ma67) / (ma15 + ma67)
        ha8 = (ha5c * ma15 + ha7 * ma67) / (ma15 + ma67)
        Ta8 = Ta5 + 2
        delta_ha8 = 0.1
        while abs(delta_ha8) >= 0.0001:
            cpa8, _, cpv8 = EN.cp_calculate(Ta8)
            ha8c = cpa8 * (Ta8 - 273.15) + w8 * (EN.ifgwo + cpv8 * (Ta8 - 273.15))
            delta_ha8 = ha8c - ha8
            if delta_ha8 > 0:
                Ta8 -= 0.1 * abs(delta_ha8 / ha8c)
            else:
                Ta8 += 0.1 * abs(delta_ha8 / ha8c)
        rhoav8,_ =EN.rhoa_calculate(Ta8,w8,pa8)
        vav8 = mav8 / (rhoav8 * A6)
        cpa8, cpw8, cpv8 = EN.cp_calculate(Ta8)
        epsTa8 = CT.epsTan(Ta8, w8, cpw8, cpv8, cpa8, pa8)
        delta_pa9 = 0.2
        pa9 = pa8 - 30
        while abs(delta_pa9) >= 0.1:
            if delta_pa9 > 0:
                pa9 -= abs(delta_pa9)
            else:
                pa9 += abs(delta_pa9)
            Ta9 = Ta8 + epsTa8 * (h9 - h8)
            rhoav9 = (1 + w8) * (1 - w8 / (w8 + 0.62198)) * pa9 / (EN.R * Ta9)
            rhoav9,_ =EN.rhoa_calculate(Ta9,w8,pa9)
            Frd = (mav8 / A9) ** 2 / rhoav9 / (rhoav10 - rhoav9) / EN.g / d9
            pa9c = pa10 + (0.02 * Frd ** (-1.5) - 0.14 / Frd) * (mav8 / A9) ** 2 / rhoav9
            delta_pa9 = pa9 - pa9c

        # 更新 delta_pf 为新的误差值
        vav9 = mav8 / (rhoav9 * A9)
        delta_p89 = pa8 * (1 - (1 + epsTa8 * (h9 - h8) / Ta8) ** (-0.021233 * (1 + w8) / (epsTa8 * (w8 + 0.622))))
        pa8m = pa9 + (rhoav9 * vav9 ** 2) / 2 - (rhoav8 * vav8 ** 2) / 2 + delta_p89
        delta_pf=pa8m-pa8

    Qaw = (ha5c - hai) * mav15
    mwevap = ma15 * (w5 - w1)
    Qad = (ha7 - ha6) * ma67
    evap = mwevap / (Qaw + Qad) * 1e6
    Qww = mww * cpwm * (Tinw - Twow)
    Qwd = mwd * cpwdm * (Tin - Twod)
    Qtot = Qaw + Qad
    q_tower=Qtot
    mevap=mwevap
    # mevap, q_tower =  #机理模型，代理模型对应unit类的某个函数

    return mevap, q_tower

#mevap,q=cooling_tower_main1(18.989,192.6307,60.6255,172.4631,249.091,121.4750,210,2,28021,43056,3.688,31.8909,256,0.0254,0.0234,4,2,27.75,183,296.15,0.81,100000,311,45200)
#print("mevap:", mevap, "q:", q)




# 基于空冷的干湿联合
def cooling_tower_main2(h4,d4,h7,d7,d0,Lfi,Afrw,Afrd,l,Lte,ntb,Do,Di,nr,nwp,aj,nb,Ta1,RH,pa1,Tin,mw):
    ## tower parameter
    A4=math.pi * (d4/2) ** 2
    d3=d4
    d6=152.03
    h3=h4/2
    h6=We.Lsp+h4+Lfi
    A3=math.pi * (d3 / 2) ** 2
    A6 = math.pi * (d6 / 2) ** 2
    A7=math.pi * (d7/2) ** 2
    Ats = np.pi * Di ** 2 / 4

    # operation parameter
    Twb1 = 19.7 + 273.15
    delta_w1 = 0.1
    while abs(delta_w1) > 0.0001:
        # 湿度计算
        if delta_w1 > 0:
            Twb1 += abs(delta_w1)
        else:
            Twb1 -= abs(delta_w1)
        pvwb1, w1,_ = EN.Environment_calculate(Twb1, Ta1, pa1)
        pvs1,_,_ = EN.Environment_calculate(Ta1, Ta1, pa1)
        RHc = pa1 * w1 / (0.622 + w1) / pvs1
        # 计算下一个迭代的 delta_w1
        delta_w1 = RH - RHc

    cpa1, cpw1, cpv1 = EN.cp_calculate(Ta1)
    delta_p134 = pa1 * (1 - ((1 - (0.00975 * (h3 + Lfi / 2) / Ta1)) ** (3.5 * (1 + w1) * (1 - w1 / (w1 + 0.62198)))))
    hai = cpa1 * (Ta1 - 273.15) + w1 * (EN.ifgwo + cpv1 * (Ta1 - 273.15))
    rhoav1, rhoa1 = EN.rhoa_calculate(Ta1, w1, pa1)
    Ta2 = Ta1 - 0.00975 * h3
    pa2 = pa1 * (1 - (0.00975 * h3 / Ta1)) ** 3.5
    _, rhoa2 = EN.rhoa_calculate(Ta2, w1, pa2)
    cpa2, cpw2, cpv2 = EN.cp_calculate(Ta2)
    Ta8, pa8 = EN.Tan_calculate(Ta1, pa1, h7, w1)
    rhoav8, _ = EN.rhoa_calculate(Ta8, w1, pa8)

    # integration initial
    pa4=EN.Tan_calculate(Ta1,pa1,h6,w1)
    t1=1
    v02 = 1.55
    delta_pf = 0.51
    while abs(delta_pf) >= 0.5:  # 外侧循环计算pa8
        if delta_pf > 0:
            # pa4 = pa4 + min(0.5, 0.5 * delta_pf)
            pa4 = pa4 + 10 * 10 ** (-t1 / 100)
        else:
            # pa4 = pa4 - min(0.5, 0.5 * abs(delta_pf))
            pa4 = pa4 - 10 * 10 ** (-t1 / 100)
        pa3 = pa4
        delta_fl_bad = 0.21

        while abs(delta_fl_bad) >= 0.2:  # 干冷段动力平衡
            if delta_fl_bad > 0:
                v02 = v02 + min(0.002, abs(delta_fl_bad))
            else:
                v02 = v02 - min(0.002, abs(delta_fl_bad))

            ma23 = v02 * Afrd * rhoa2

            delta_en_bad = 0.001
            t3 = 1
            while abs(delta_en_bad) >= 1e-5:
                if delta_en_bad > 0:
                    # Twod = Twod + min(0.2, 0.1 * abs(delta_en_bad))
                    Twod = Twod + 1 * 10 ** (-t3 / 100)
                else:
                    # Twod = Twod - min(0.2, 0.1 * abs(delta_en_bad))
                    Twod = Twod - 1 * 10 ** (-t3 / 100)
                Twdm = (Tin + Twod) / 2
                _, cpwdm, _ = EN.cp_calculate(Twdm)
                Qwd = mw * cpwdm * (Tin - Twod)
                Ta3 = Qwd / (ma23 * cpa2) + Ta2
                HA = HE.HA_calculate(Tin, Twod, mw, cpw1, Ats, nb, ntb, nwp, Lte, v02, Afrd)
                Ft, delta_t = HE.Ft_calculate(Tin, Ta3, Twod, Ta2)
                Qhd = Ft * HA * delta_t
                delta_en_bad = (Qwd - Qhd) / Qwd
                t3 = t3 + 1

            Ta23 = (Ta2 + Ta3) / 2
            _, rhoa3 = EN.rhoa_calculate(Ta3, w1, pa3)
            rhoa23 = 2 / (1 / rhoa3 + 1 / rhoa2)
            va3 = ma23 / rhoa3 / Afrd
            Hd = pa2 - pa3
            Kheaj = HE.K_dry(v02, aj, rhoa3, rhoa2)
            Zd = Kheaj * (ma23/ Afrd) ** 2 / (2 * rhoa23) + rhoa3 * va3 ** 2 / 2
            delta_fl_bad = Hd - Zd

        Tinw = Twod
        Twow = Tinw - 2
        Twwm = (Tinw + Twow) / 2
        _, cpwm, _ = EN.cp_calculate(Twwm)
        Ta6 = (Tinw + Twow) / 2
        w3 = w1
        cpa3, cpw3, cpv3 = EN.cp_calculate(Ta3)
        ha3 = cpa3 * (Ta3 - 273.15) + w3 * (EN.ifgwo + cpv3 * (Ta3 - 273.15))
        rhoav3,_ = EN.rhoa_calculate(Ta3, w3, pa4)
        ma36 = ma23
        delta_p46 = pa4 * (1 - ((1 - (0.00975 * (h6 - h4) / Ta3)) ** (3.5 * (1 + w3) * (1 - w3 / (w3 + 0.62198)))))
        pa6 = pa4 - delta_p46 - 21
        delta_fl_pa6w = 0.51
        while abs(delta_fl_pa6w) >= 0.5:  # 外侧循环计算pa6
            if delta_fl_pa6w > 0:
                pa6 = pa6 + max(0.5, min(0.5, 1.01 * delta_fl_pa6w))
            else:
                pa6 = pa6 - max(0.5, min(0.5, 1.01 * abs(delta_fl_pa6w)))

            delta_en_baw = 0.001
            while abs(delta_en_baw) >= 0.0001:
                # fill selection (PVC)
                if delta_en_baw > 0:
                    Twow = Twow - min(0.2, 0.05 * abs(delta_en_baw))
                else:
                    Twow = Twow + min(0.2, 0.05 * abs(delta_en_baw))

                Twwm = (Tinw + Twow) / 2
                _, cpwm, _ = EN.cp_calculate(Twwm)
                rhowo = (1.49343 * 10 ** (-3) - 3.7164 * 10 ** (-6) * Twow + 7.09782 * 10 ** (
                    -9) * Twow ** 2 - 1.90321 * 10 ** (-20) * Twow ** 6) ** (-1)
                ten_wo = 5.148103 * 10 ** (-2) + 3.998714 * 10 ** (-4) * Twow - 1.4721869 * 10 ** (
                    -6) * Twow ** 2 + 1.21405335 * 10 ** (-9) * Twow ** 3
                anian = 3.061 * 10 ** (-6) * (rhowo ** 4 * 9.8 ** 9 / ten_wo) ** 0.25
                aden = 998 / rhowo
                av = 73.298 * (9.8 ** 5 * ten_wo ** 3 / rhowo ** 3) ** 0.25
                aL = 6.122 * (9.8 * ten_wo / rhowo) ** 0.25
                Gw = mw / Afrw
                vw3 = Gw / rhowo
                delta_Ta6 = 0.011
                while abs(delta_Ta6) >= 0.01:
                    if delta_Ta6 > 0:
                        Ta6 = Ta6 - min(0.001, 1 * abs(delta_Ta6))
                    else:
                        Ta6 = Ta6 + min(0.001, 1 * abs(delta_Ta6))


                    Twb6 = Ta6
                    cpa6,cpw6,cpv6=EN.cp_calculate(Ta6)
                    pvwb6, _, _ = EN.Environment_calculate(Twb6, Ta6, pa8)
                    w6 = 0.62509 * pvwb6 / (pa6 - pvwb6)
                    mav36 = ma36 * (2 + w3 + w6) / 2
                    ha6 = mw * cpwm * (Tinw - Twow) / mav36 + ha3
                    ha6c = cpa6 * (Ta6 - 273.15) + w6 * (EN.ifgwo + cpv6 * (Ta6 - 273.15))
                    delta_Ta6 = (ha6c - ha6) / ha6

                mav3 = ma36 * (1 + w3)
                Ga = ma36 / Afrw
                vav3 = mav3 / (rhoav3 * Afrw)
                nian_a3, nian_v3, nian_av3 = EN.nian_calculate(Ta3, w3)
                Nw = We.Merkel1(pa3, Ta3, Twow, nian_av3, rhoav3, Ga, Gw, vav3, aden, h4, w3, Lfi, anian, rhowo, aL, av)
                Ncc = We.Merkel2(mw, Twow, Tinw, cpw3, mav36, ha3, pa3)
                delta_en_baw = Nw - Ncc

            rhoav6, _ = EN.rhoa_calculate(Ta6, w6, pa6)
            mav6 = ma36 * (1 + w6)
            vav6 = mav6 / (rhoav6 * A6)
            Ga = ma36 / Afrw
            Gav3 = mav3 / Afrw
            Gav6 = mav6 / Afrw
            Gav36 = mav36 / Afrw
            rhoav36 = 2 / (1 / rhoav3 + 1 / rhoav6)
            nian_a6,nian_v6,nian_av6=EN.nian_calculate(Ta6,w6)
            Ktsfi, Kctfi, Krzfi, Kfsfi_Kctcfi, Kfi, Kctefi, Kspfi, Kwdfi, Kdefi = We.K_wet(rhoav36, rhoav3, mav3, mav36,Gav3, Gav6, rhoav6, mav6,Afrw, d4, h4, Lfi, Gw, Ga,aden, anian, nian_av3,nian_av6, aL, av, vw3, Gav36,vav3)
            K_fi = Kctfi+Krzfi+Kfsfi_Kctcfi+Kfi+Kctefi+Kspfi+Kwdfi+Kdefi
            delta_p456 = pa4 * (1 - ((1 - (0.00975 * (h6 - (h4 + Lfi / 2)) / Ta3)) ** (3.5 * (1 + w3) * (1 - w3 / (w3 + 0.62198)))))
            Hw = pa4 - pa6 - delta_p456
            Zw = K_fi * (mav36 / Afrw) ** 2 / (2 * rhoav36)
            pa6m = pa4 - delta_p456 - Zw
            delta_fl_pa6w = pa6m - pa6

        epsTa6 = CT.epsTan(Ta6,w6,cpw6,cpv6,cpa6,pa6)
        delta_pa7 = 0.1
        pa7=pa6-30
        while abs(delta_pa7) >= 0.1:
            if delta_pa7 > 0:
                pa7 = pa7 - abs(delta_pa7)
            else:
                pa7 = pa7 + abs(delta_pa7)
            Ta7 = Ta6 + epsTa6 * (h7 - h6)
            rhoav7 = (1 + w6) * (1 - w6 / (w6 + 0.62198)) * pa7 / (EN.R * Ta7)
            Frd = (mav6 / A7) ** 2 / rhoav7 / abs(rhoav8 - rhoav7) / EN.g / d7
            pa7c = pa8 + (0.02 * Frd ** (-1.5) - 0.14 / Frd) * (mav6 / A7) ** 2 / rhoav7
            delta_pa7 = pa7 - pa7c

        delta_p67 = pa6 * (1 - (1 + epsTa6 * (h7 - h6) / Ta6) ** (-0.021233 * (1 + w6) / (epsTa6 * (w6 + 0.622))))
        pa6c = pa7 + delta_p67 + (mav6 / A7) ** 2 / (2 * rhoav7) - (mav6 / A6) ** 2 / (2 * rhoav6)
        delta_pf = pa6c - pa6
        t1=t1+1

    Qaw = (ha6 - ha3) * mav36
    mevap = ma36 * (w6 - w3)
    Qad = ma23 * cpa2 * (Ta3 - Ta2)
    Ta3 = Qwd / (ma23 * cpa2) + Ta2
    evap = mevap / (Qaw + Qad) * 1e6
    Qww = mw * cpwm * (Tinw - Twow)
    Qwd = mw * cpwdm * (Tin - Twod)
    q_tower = Qaw + Qad
    return mevap, q_tower

#分建式，一个主函数，两个塔分别为子函数
def cooling_tower_main3():
    mevap, q_tower1=cooling_tower_wet()
    q_tower2=cooling_tower_dry()
    Q_tot=q_tower1+q_tower2
    return Q_tot,mevap

def cooling_tower_wet(h3,d3,h9,d9,d0,Lfi,Afrw,Ta1,RH,pa1,Tin,mw):

    A9 = math.pi * (d9 / 2) ** 2
    h5=h3+We.Lsp+Lfi
    d5=152
    A5 = math.pi * (d5 / 2) ** 2
    # opration
    Twb1=20+273.15
    delta_w1 = 0.1
    while abs(delta_w1) > 0.0001:
        # 湿度计算
        if delta_w1 > 0:
            Twb1 += abs(delta_w1)
        else:
            Twb1 -= abs(delta_w1)
        pvwb1, w1, _ = EN.Environment_calculate(Twb1, Ta1, pa1)
        pvs1, _, _ = EN.Environment_calculate(Ta1, Ta1, pa1)
        RHc = pa1 * w1 / (0.622 + w1) / pvs1
        # 计算下一个迭代的 delta_w1
        delta_w1 = RH - RHc
    cpa1, cpw1, cpv1 = EN.cp_calculate(Ta1)
    delta_p134 = pa1 * (1 - ((1 - (0.00975 * (h3 + Lfi / 2) / Ta1)) ** (3.5 * (1 + w1) * (1 - w1 / (w1 + 0.62198)))))
    hai = cpa1 * (Ta1 - 273.15) + w1 * (EN.ifgwo + cpv1 * (Ta1 - 273.15))
    rhoav1, rhoa1 = EN.rhoa_calculate(Ta1, w1, pa1)
    Ta3, pa3 = EN.Tan_calculate(Ta1, pa1, h3, w1)
    nian_a1, nian_v1, nian_av1 = EN.nian_calculate(Ta1, w1)
    Ta10, pa10 = EN.Tan_calculate(Ta1, pa1, h9, w1)
    rhoav10, _ = EN.rhoa_calculate(Ta10, w1, pa10)

    _, pa5 = EN.Tan_calculate(Ta1, pa1, h5, w1)
    pa5 = pa5 - 50
    v06 = 1.55
    Tinw=Tin
    Twow=(Tinw+2*Twb1+Ta1)/4
    Twwm = (Tinw + Twow) / 2
    _, cpwm, _ = EN.cp_calculate(Twwm)

    Ta5 = Twow - 2;
    Twb5 = Ta5
    pvwb5, w5, _ = EN.Environment_calculate(Twb5, Ta5, pa5)
    cpa5, cpw5, cpv5 = EN.cp_calculate(Ta5)
    ha5 = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
    mav15 = mw * cpwm * (Tinw - Twow) / (ha5 - hai)

    delta_pf = 0.51
    while abs(delta_pf) >= 0.5:
        # 更新 pa5 的值
        if delta_pf > 0:
            pa5 += max(0.5,min(0.5,1.01*delta_pf))
        else:
            pa5 -= max(0.5,min(0.5,1.011*abs(delta_pf)))

        delta_fl_baw = 0.21
        while abs(delta_fl_baw) >= 0.2:
            # 更新 v06 的值
            if delta_fl_baw > 0:
                mav15 += min(10000,300*delta_fl_baw)
            else:
                mav15 -= min(9000,abs(299*delta_fl_baw))

            delta_en_baw = 0.001
            while abs(delta_en_baw) >= 0.0001:
                # fill selection (PVC)
                if delta_en_baw > 0:
                    Twow = Twow - min(0.2, 0.1 * abs(delta_en_baw))
                else:
                    Twow = Twow + min(0.2, 0.1 * abs(delta_en_baw))

                Twwm = (Tinw + Twow) / 2
                _, cpwm, _ = EN.cp_calculate(Twwm)
                rhowo = (1.49343 * 10 ** (-3) - 3.7164 * 10 ** (-6) * Twow + 7.09782 * 10 ** (
                    -9) * Twow ** 2 - 1.90321 * 10 ** (-20) * Twow ** 6) ** (-1)
                ten_wo = 5.148103 * 10 ** (-2) + 3.998714 * 10 ** (-4) * Twow - 1.4721869 * 10 ** (
                    -6) * Twow ** 2 + 1.21405335 * 10 ** (-9) * Twow ** 3
                anian = 3.061 * 10 ** (-6) * (rhowo ** 4 * 9.8 ** 9 / ten_wo) ** 0.25
                aden = 998 / rhowo
                av = 73.298 * (9.8 ** 5 * ten_wo ** 3 / rhowo ** 3) ** 0.25
                aL = 6.122 * (9.8 * ten_wo / rhowo) ** 0.25
                Gw = mw / Afrw
                vw3 = Gw / rhowo
                delta_Ta5 = 0.011
                while abs(delta_Ta5) >= 0.01:
                    if delta_Ta5 > 0:
                        Ta5 = Ta5 - min(0.01, 10 * abs(delta_Ta5))
                    else:
                        Ta5 = Ta5 + min(0.01, 9 * abs(delta_Ta5))
                    hao = mw * cpwm * (Tinw - Twow) / mav15 + hai
                    Twb5 = Ta5
                    pvwb5, _, _ = EN.Environment_calculate(Twb5, Ta5, pa5)
                    w5 = 0.62509 * pvwb5 / (pa5 - pvwb5)
                    cpa5, cpw5, cpv5 = EN.cp_calculate(Ta5)
                    ha5c = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
                    delta_Ta5 = (ha5c - hao) / hao

                ma15 = 2 * mav15 / (2 + w1 + w5)
                mav1 = ma15 * (1 + w1)
                Ga = ma15 / Afrw
                vav3 = mav1 / (rhoav1 * Afrw)
                Nw = We.Merkel1(pa1, Ta1, Twow, nian_av1, rhoav1, Ga, Gw, vav3, aden, h3, w1, Lfi, anian, rhowo, aL,
                                av)
                Ncc = We.Merkel2(mw, Twow, Tinw, cpw1, mav15, hai, pa1)
                delta_en_baw = Nw - Ncc

            rhoav5, _ = EN.rhoa_calculate(Ta5, w5, pa5)
            mav5 = ma15 * (1 + w5)
            vav5 = mav5 / (rhoav5 * A5)
            Ga = ma15 / Afrw
            Gav1 = mav1 / Afrw
            Gav5 = mav5 / Afrw
            Gav15 = mav15 / Afrw
            rhoav15 = 2 / (1 / rhoav1 + 1 / rhoav5)
            nian_a5, nian_v5, nian_av5 = EN.nian_calculate(Ta5, w5)
            Ktsfi, Kctfi, Krzfi, Kfsfi_Kctcfi, Kfi, Kctefi, Kspfi, Kwdfi, Kdefi = We.K_wet(rhoav15, rhoav1, mav1,
                                                                                           mav15, Gav1, Gav5,
                                                                                           rhoav5, mav5, Afrw, d3,
                                                                                           h3, Lfi, Gw, Ga, aden,
                                                                                           anian, nian_av1,
                                                                                           nian_av5, aL, av, vw3,
                                                                                           Gav15, vav3)
            K_fi = Ktsfi + Kctfi + Krzfi + Kfsfi_Kctcfi + Kfi + Kctefi + Kspfi + Kwdfi + Kdefi
            Hw = pa1 - pa5 - delta_p134
            Zw = K_fi * (mav15 / Afrw) ** 2 / (2 * rhoav15)
            delta_fl_baw = (Hw - Zw)

        epsTa5 = CT.epsTan(Ta5, w5, cpw5, cpv5, cpa5, pa5)
        delta_pa9 = 0.1
        pa9 = pa5 - 30
        while abs(delta_pa9) >= 0.1:
            if delta_pa9 > 0:
                pa9 -= abs(delta_pa9)
            else:
                pa9 += abs(delta_pa9)
            Ta9 = Ta5 + epsTa5 * (h9 - h5)
            rhoav9, _ = EN.rhoa_calculate(Ta9, w5, pa9)
            Frd = (mav5 / A9) ** 2 / rhoav9 / (rhoav10 - rhoav9) / EN.g / d9
            pa9c = pa10 + (0.02 * Frd ** (-1.5) - 0.14 / Frd) * (mav5 / A9) ** 2 / rhoav9
            delta_pa9 = pa9 - pa9c

        delta_p59 = pa5 * (1 - (1 + epsTa5 * (h9 - h5) / Ta5) ** (-0.021233 * (1 + w5) / (epsTa5 * (w5 + 0.622))))
        pa5c = pa9 + delta_p59 + (mav5 / A9) ** 2 / (2 * rhoav9)
        delta_pf = pa5c - pa5

    Qaw = (ha5c - hai) * mav15
    mwevap = ma15 * (w5 - w1)
    Qww = mw * cpwm * (Tinw - Twow)
    return mwevap, Qww

def cooling_tower_dry(d4,h4,h5,d5,Ta1,pa1,Tin,Afrd,mw,Ats, nb, ntb, nwp, Lte):
    d3 = d4
    d6 = 152.03
    h3 = h4 / 2
    A5 = math.pi * (d5 / 2) ** 2
    w1=0

    cpa1, cpw1, cpv1 = EN.cp_calculate(Ta1)
    Ta2 = Ta1 - 0.00975 * h3
    pa2 = pa1 * (1 - (0.00975 * h3 / Ta1)) ** 3.5
    _, rhoa2 = EN.rhoa_calculate(Ta2, w1, pa2)
    cpa2, cpw2, cpv2 = EN.cp_calculate(Ta2)

    Ta6, _ = EN.Tan_calculate(Ta1, pa1, h5, w1)
    pa6 = pa1 * (1 - (0.00975 * h5 / Ta1)) ** 3.5
    _, rhoa6 = EN.rhoa_calculate(Ta6, w1, pa1)

    # integration initial
    pa3 = pa1 * (1 - (0.00975 * h3 / Ta1)) ** 3.5 - 15
    v02 = 1.55
    Twod = (Tin * 3 + Ta6) / 4
    delta_pf = 0.51
    while abs(delta_pf) >= 0.5:  # 外侧循环计算pa8
        if delta_pf > 0:
            # pa4 = pa4 + min(0.5, 0.5 * delta_pf)
            pa3 = pa3 + min(0.5,0.5*delta_pf)
        else:
            # pa4 = pa4 - min(0.5, 0.5 * abs(delta_pf))
            pa3 = pa3 - min(0.5,0.5*abs(delta_pf))

        delta_fl_bad = 0.21
        while abs(delta_fl_bad) >= 0.2:  # 干冷段动力平衡
            if delta_fl_bad > 0:
                v02 = v02 + min(0.002, abs(delta_fl_bad))
            else:
                v02 = v02 - min(0.002, abs(delta_fl_bad))

            ma23 = v02 * Afrd * rhoa2

            delta_en_bad = 0.001
            while abs(delta_en_bad) >= 1e-5:
                if delta_en_bad > 0:
                    # Twod = Twod + min(0.2, 0.1 * abs(delta_en_bad))
                    Twod = Twod + min(0.01,0.01*abs(delta_en_bad))
                else:
                    # Twod = Twod - min(0.2, 0.1 * abs(delta_en_bad))
                    Twod = Twod - min(0.01,0.01*abs(delta_en_bad))

                Twdm = (Tin + Twod) / 2
                _, cpwdm, _ = EN.cp_calculate(Twdm)
                Qwd = mw * cpwdm * (Tin - Twod)
                Ta3 = Qwd / (ma23 * cpa2) + Ta2
                HA = HE.HA_calculate(Tin, Twod, mw, cpwdm, Ats, nb, ntb, nwp, Lte, v02, Afrd)
                Ft, delta_t = HE.Ft_calculate(Tin, Ta3, Twod, Ta2)
                Qhd = Ft * HA * delta_t
                delta_en_bad = (Qwd - Qhd) / Qwd

            _, rhoa3 = EN.rhoa_calculate(Ta3, w1, pa3)
            rhoa23 = 2 / (1 / rhoa3 + 1 / rhoa2)
            va3 = ma23 / rhoa3 / Afrd
            Hd = pa2 - pa3
            Kheaj = HE.K_dry(v02, aj, rhoa3, rhoa2)
            Zd = Kheaj * (ma23 / Afrd) ** 2 / (2 * rhoa23) + rhoa3 * va3 ** 2 / 2
            delta_fl_bad = Hd - Zd

        Ta5 = Ta3 - 0.00975 * (h5 - h3)
        delta_pa5 = 0.2
        pa5 = pa3 - 30
        while abs(delta_pa5) >= 0.1:
            if delta_pa5 > 0:
                pa5 = pa5 - abs(delta_pa5)
            else:
                pa5 = pa5 + abs(delta_pa5)
            _, rhoa5 = EN.rhoa_calculate(Ta5, w1, pa5)
            Frd = (ma23 / A5) ** 2 / rhoa5 / (rhoa6 - rhoa5) / g / d5
            Kto = -0.129 * (Frd * d5 / d3) ** (-1) + 0.0144 * (Frd * d5 / d3) ** (-1.5)
            ae5 = 1.004 + 5.8 * (d5 / d3) ** 9 + (0.007 + 0.043 * (d5 / d3) ** 2.5) * Frd ** (-1.5)
            pa5c = pa6 + (Kto + ae5) * (ma23 / A5) ** 2 / rhoa5 / 2
            delta_pa5 = pa5 - pa5c

        va5 = ma23 / (rhoa5 * A5)
        delta_p35 = pa3 - pa3 * (1 - (0.00975 * (h5 - h3) / Ta3)) ** 3.5
        pa3m = pa5 + (rhoa5 * va5 ** 2) / 2 - (rhoa3 * va3 ** 2) / 2 + delta_p35
        delta_pf = pa3m - pa3

    Qad = ma23 * cpa2 * (Ta3 - Ta2)
    Qwd = mw * cpwdm * (Tin - Twod)
    return Qwd


#  机械通风干湿联合
def cooling_tower_main4(H11, H3, Wfi, Bfi, Ntower, dc, P_F_d, fin_efficiency, Lfi, Hsp, H6, nrf, Lt, nbf, Hf, ntf,mw,Ta1,pa1,RH,Tin):
    H6 = (H11 - 3 - Hf / 2)
    H8 = H6
    ntrf, Afr, Ac, Af, Aaf, Apf=Machanical_tower.fin_tube(Lt,Hf)
    Afr_fill = Wfi * Bfi
    mww=mw/Ntower

    mavi_f_hybrid = 267.8392 # assume
    mav15 = 400 # assume
    Twb1=19.7+273.15 # assume
    delta_w1 = 0.1
    while abs(delta_w1) > 0.0001:
        # 湿度计算
        if delta_w1 > 0:
            Twb1 += abs(delta_w1)
        else:
            Twb1 -= abs(delta_w1)
        pvwb1, w1, _ = EN.Environment_calculate(Twb1, Ta1, pa1)
        pvs1, _, _ = EN.Environment_calculate(Ta1, Ta1, pa1)
        RHc = pa1 * w1 / (0.622 + w1) / pvs1
        # 计算下一个迭代的 delta_w1
        delta_w1 = RH - RHc

    cpa1 = 1.045356e3 - 3.161783e-1 * Ta1 + 7.083814e-4 * Ta1 ^ 2 - 2.705209e-7 * Ta1 ^ 3
    cpa1_h, cpw1_h, cpv1_h = EN.cp_calculate(Ta1)
    rhoav1, rhoa1 = EN.rhoa_calculate(Ta1, w1, pa1)
    miua1=Machanical_tower.miua(Ta1)
    ha1 = cpa1_h * (Ta1 - 273.15) + w1 * (EN.ifgwo + cpv1_h * (Ta1 - 273.15))
    Ta6, pa6 = EN.Tan_calculate(Ta1, pa1, H6, w1)

    # 计算干扰和回流
    L = H3 * 4
    num = 4
    l = Bfi * num
    Ra = 0.24 * l / (1 + 0.013 * l) * 0.01
    Re = 0.073 * L / (1 + 0.004 * L) * 0.01
    pa7 = pa6 - 30
    aa=1
    delta_Ta1=0
    delta_Twb1=0
    while aa < 3:
        Ta1 = Ta1 + delta_Ta1
        Twb1 = Twb1 + delta_Twb1
        miua1 = Machanical_tower.miua(Ta1)
        pvwb1, w1, _ = EN.Environment_calculate(Twb1, Ta1, pa1)
        pvs1, _, _ = EN.Environment_calculate(Ta1, Ta1, pa1)
        RH = pa1 * w1 / (0.622 + w1) / pvs1
        rhoav1, rhoa1 = EN.rhoa_calculate(Ta1, w1, pa1)
        cpa1_h, cpw1_h, cpv1_h = EN.cp_calculate(Ta1)
        ha1 = cpa1_h * (Ta1 - 273.15) + w1 * (EN.ifgwo + cpv1_h * (Ta1 - 273.15))

        Twow = Tin - 5
        delta_power = 1
        t3 = 1
        while abs(delta_power) >= 0.1 :
            if delta_power > 0:
                pa7 += 1 * 10 ** (-t3 / 100)
            else:
                pa7 -= 1 * 10 ** (-t3 / 100)

            delta_p = 1.01
            t2 = 1
            while abs(delta_p) >= 0.005:  # Since 0.5% is 0.005 in decimal
                if delta_p > 0:
                    mavi_f_hybrid -= 100 * 10 ** (-t2 / 100)
                else:
                    mavi_f_hybrid += 100 * 10 ** (-t2 / 100)
                Tpfi = Tin
                Tpfo = (Tpfi + 3 * Ta1) / 4
                delta_q = 0.001
                delta_Tpfo = 0.001
                while abs(delta_Tpfo) >= 1e-5:
                    if delta_q > 0:
                        Tpfo += min(0.01, 0.01 * abs(delta_Tpfo))
                    else:
                        Tpfo -= min(0.01, 0.01 * abs(delta_Tpfo))
                    Tpfm = (Tpfi + Tpfo) / 2
                    cpwpmf = 8.15599e3 - 2.80627e1 * Tpfm + 5.11283e-2 * Tpfm ** 2 - 2.17582e-13 * Tpfm ** 6
                    Qwf = mww * cpwpmf * (Tpfi - Tpfo)
                    mai_f_hybrid = mavi_f_hybrid / (1 + w1)
                    ha7 = ha1 + Qwf / mai_f_hybrid
                    Taof = Qwf / (mai_f_hybrid * cpa1) + Ta1
                    delta_Taof = 0.0001
                    while abs(delta_Taof) >= 1e-8:
                        if delta_Taof > 0:
                            Taof = Taof - min(0.1, 10 * abs(delta_Taof))
                        else:
                            Taof = Taof + min(0.1, 9 * abs(delta_Taof))

                        cpa7, _, cpv7 = EN.cp_calculate(Taof)
                        haofc = cpa7 * (Taof - 273.15) + w1 * (EN.ifgwo + cpv7 * (Taof - 273.15))
                        delta_Taof = (haofc - ha7) / ha7
                    Tamf = (Ta1 + Taof) / 2
                    cpamf, _, cpvmf = EN.cp_calculate(Tamf)
                    miuamf = 2.287973 * 10 ** (-6) + 6.259793 * 10 ** (-8) * Tamf - 3.131956 * 10 ** (
                        -11) * Tamf ** 2 + 8.15038 * 10 ** (-15) * Tamf ** 3
                    kamf = -4.937787e-4 + 1.1018087e-4 * Tamf - 4.627937e-8 * Tamf ** 2 + 1.250603e-11 * Tamf ** 3
                    miuvmf = 2.562435 * 10 ** (-6) + 1.816683 * 10 ** (-8) * Tamf + 2.579066 * 10 ** (
                        -11) * Tamf ** 2 - 1.067299 * 10 ** (-14) * Tamf ** 3
                    kvmf = 1.3046e-2 - 3.756191e-5 * Tamf + 2.217964e-7 * Tamf ** 2 - 1.111562e-10 * Tamf ** 3
                    rhoavmf,_ =EN.rhoa_calculate(Tamf,w1,pa1)
                    cpavmf = (cpamf + w1 * cpvmf) / (1 + w1)
                    Pravmf=Machanical_tower.Pravmf(w1,miuamf, miuvmf, kamf, kvmf, cpavmf)

                    miuw_f = 2.414 * 1e-5 * 10 ** (247.8 / (Tpfm - 140))
                    Lamdawf = -6.14255e-1 + 6.9963e-3 * Tpfm - 1.01075e-5 * Tpfm ** 2 + 4.74737e-12 * Tpfm ** 4
                    Prwf = miuw_f * cpwpmf / Lamdawf
                    Rhowf = 1 / (1.49343 * 1e-3 - 3.7164 * 1e-6 * ((Tpfi + Tpfo) / 2) + 7.09782 * 1e-9 * (
                                (Tpfi + Tpfo) / 2) ** 2 - 1.90321 * 1e-20 * ((Tpfi + Tpfo) / 2) ** 6)
                    Ats_tubef = math.pi * Machanical_tower.ditf ** 2 / 4
                    vbf = mww / Rhowf / Ats_tubef / (nbf * ntrf * nrf / ntf)
                    Rewf = mww / (nbf * ntrf * nrf / ntf) / miuw_f / math.pi / Machanical_tower.ditf * 4
                    fbf = (1.82 * math.log10(Rewf) - 1.64) ** -2
                    Nuwfi = (fbf / 8) * Rewf * Prwf / (1.07 + 12.7 * (fbf / 8) ** 0.5 * (Prwf ** (2 / 3) - 1))
                    Nuwf = (fbf / 8) * (Rewf - 1000) * Prwf * (1 + (Machanical_tower.ditf / Hf) ** 0.67) / (
                                1.07 + 12.7 * (fbf / 8) ** 0.5 * (Prwf ** (2 / 3) - 1))
                    hwf = Nuwf * Lamdawf / Machanical_tower.ditf

                    # air-side heat transfer coefficient related calculation
                    fi = (Machanical_tower.df / Machanical_tower.dr - 1) * (1 + 0.35 * math.log(Machanical_tower.df / Machanical_tower.dr))
                    ha = 49  # Assumed value
                    delta_ha = 0.001
                    while abs(delta_ha) >= 1e-5:
                        if delta_ha > 0:
                            ha += min(0.5, abs(delta_ha))
                        else:
                            ha -= min(0.5, abs(delta_ha))

                        b = (2 * ha / Machanical_tower.kf / Machanical_tower.tf) ** 0.5
                        yitaf = math.tanh(b * Machanical_tower.dr * fi / 2) / (b * Machanical_tower.dr * fi / 2)
                        efAa = Aaf - Af * (1 - yitaf)
                        ef = efAa / Aaf  # the corresponding fin effectiveness
                        Gc = mavi_f_hybrid / Ac
                        mav67 = mavi_f_hybrid
                        vav67c = mav67 / (Ac * rhoavmf)  # vav67c calculation

                        A_Ar = (0.5 * (Machanical_tower.df ** 2 - Machanical_tower.dr ** 2) + Machanical_tower.df * Machanical_tower.tft + Machanical_tower.dr * (
                                    Machanical_tower.Pff - Machanical_tower.tfr)) / Machanical_tower.Pff / Machanical_tower.dr  # Total air side area to the root area ratio
                        Rec = Gc * Machanical_tower.dr / miua1

                        hac = 0.38 * Rec ** 0.6 * Pravmf ** 0.333 * A_Ar ** (-0.15) * (kamf / Machanical_tower.dotf)
                        hae = ha * ef  # effective heat transfer coefficient
                        delta_ha = hac - ha

                    Aw = math.pi * (nbf * ntrf * nrf) * Hf * Machanical_tower.ditf
                    # Now, directly use the attributes from the tower instance in calculations
                    Rthf = 1 / (tower.ntrf * tower.nrf * Hf) * (
                                math.log(tower.dotf / tower.ditf) / (2 * math.pi * tower.ktf) + math.log(
                            tower.dr / tower.dotf) / (2 * math.pi * tower.ktf) + tower.Rc / (math.pi * tower.dotf))

                    Uaf = 1 / (Aaf / hwf / Apf + Aaf * Rthf + Aaf / ha / efAa)
                    Cav = mavi_f_hybrid * cpavmf
                    Cw = mww * cpwpmf
                    C = min(Cav, Cw) / max(Cav, Cw)
                    Ntu = Uaf * Aaf / min(Cav, Cw) / tower.ntf
                    e = 1 - math.exp(Ntu ** 0.22 * (math.exp(-C * Ntu ** 0.78) - 1) / C)
                    Qua = e * min(Cav, Cw) * (Tpfi - Ta6)
                    delta_q = Qwf - Qua
                    delta_Tpfo = (Qwf - Qua) / Qwf

                rhoavof = (1 + w1) * (1 - w1 / (w1 + 0.62198)) * pa7 / (R * Taof)
                mav67 = mavi_f_hybrid
                Ta67 = (Ta6 + Taof) / 2
                pa67 = (pa6 + pa7) / 2
                rhoav67 = (1 + w1) * (1 - w1 / (w1 + 0.62198)) * pa67 / (
                            EN.R * Ta67)  # density of air-vapor mixture at elevation 1

                vav67 = mav67 / rhoav67 / Afr
                vav7 = mav67 / rhoavof / Afr
                vavof = vav7

                rhoav6 = (1 + w1) * (1 - w1 / (w1 + 0.62198)) * pa6 / (EN.R * Ta6)
                delta_pt_fin = 2 * tower.nrf * (1 + 2 * math.exp((tower.df - tower.Ptf) / 4 / tower.dr) / (
                            1 + (tower.Ptf - tower.df) / tower.dr)) * \
                               (0.021 + 13.6 * (tower.df - tower.dr) / Rec / (tower.Pff - tower.tf) + 0.25246 * (
                                           (tower.df - tower.dr) / Rec / (tower.Pff - tower.tf)) ** 0.2) * \
                               (mavi_f_hybrid / Ac) ** 2 * (1 / rhoavmf) + rhoavof * vavof ** 2 / 2 + \
                               tower.Kna * rhoav67 ** 2 / rhoav6 * vav67 ** 2 / 2

                delta_p = delta_pt_fin + pa7 - pa6
                t2 = t2 + 1

            pa5 = pa1 - 140
            delta_p5 = 1
            delta_p5 = 0.5  # Initial condition to enter the loop
            while abs(delta_p5) >= 0.5:  # Outer loop for calculating pa8
                pa15 = (pa1 + pa5) / 2
                if delta_p5 > 0:
                    pa5 = pa5 + max(0.5, min(0.5, 1.01 * delta_p5))
                else:
                    pa5 = pa5 - max(0.5, min(0.5, 1.011 * abs(delta_p5)))

                delta_pa7 = 1
                wi_hybrid = w1
                while abs(delta_pa7) >= 0.5:  # Inner loop 1 for calculating mai_b_hybrid
                    if delta_pa7 > 0:
                        mav15 = mav15 + min(0.1, 0.1 * abs(delta_pa7))
                    else:
                        mav15 = mav15 - min(0.1, 0.11 * abs(delta_pa7))
                    mai_b_hybrid = mav15 / (1 + wi_hybrid)

                    delta_Tpo = 0.001
                    t1 = 1
                    while abs(delta_Tpo) >= 1e-4:  # Inner loop 2 for temperature adjustments
                        if delta_Tpo > 0:
                            Twow = Twow - 10 ** (-t1 / 100)
                        else:
                            Twow = Twow + 10 ** (-t1 / 100)
                        Tpm = (Tpfo + Twow) / 2
                        _, cpwpm, _ = EN.cp_calculate(Tpm)
                        Qwb_hybrid = mww * cpwpm * (Tpfo - Twow)
                        Tai_hybrid = Ta1
                        cpai_hybrid,_,cpvi_hybrid=EN.cp_calculate(Tai_hybrid)
                        miuai_hybrid,miuvi_hybrid,miuavi=EN.nian_calculate(Tai_hybrid,wi_hybrid)
                        rhoavi_hybrid,_ =EN.rhoa_calculate(Tai_hybrid,wi_hybrid,pa1)
                        hai_hybrid = cpai_hybrid * (Tai_hybrid - 273.15) + wi_hybrid * (
                                    EN.ifgwo + cpvi_hybrid * (Tai_hybrid - 273.15))
                        D1 = 0.04357 * Tai_hybrid ** 1.5 * (1 / EN.Ma + 1 / EN.Mv) ** 0.5 / pa1 / (
                                    EN.Va ** 0.333 + EN.Vv ** 0.333) ** 2
                        Sc1 = miuavi / (rhoavi_hybrid * D1)

                        #  Wfie 的计算
                        Wfie = 1.0487 - 0.17408 * math.log(Wfi / H3) + 0.09 * math.log(Khe)
                        if Wfie > Wfi:
                            Wfie = Wfi

                        Ga = mai_b_hybrid / Afr_fill  # Ga calculation
                        Gw = mww / Afr_fill  # Gw calculation
                        rhowo_hybrid = 1 / (1.49343 * 10 ** (-3) - 3.7164 * 10 ** (-6) * Twow + 7.09782 * 10 ** (
                            -9) * Twow ** 2 - 1.90321 * 10 ** (-20) * Twow ** 6)
                        ten_wo = 5.148103 * 10 ** (-2) + 3.998714 * 10 ** (-4) * Twow - 1.4721869 * 10 ** (
                            -6) * Twow ** 2 + 1.21405335 * 10 ** (-9) * Twow ** 3
                        pvwo,wsw3,_=EN.Environment_calculate(Twow,Twow,pa1)
                        vw3 = mww / rhowo_hybrid / Afr_fill
                        vav3 = mav15 / rhoavi_hybrid / Afr_fill

                        alpha_Rhow = 998 / rhowo_hybrid
                        alpha_miu = 3.061e-6 * (rhowo_hybrid ** 4 * g ** 9 / ten_wo) ** 0.25
                        alpha_v = 73.298 * (9.8 ** 5 * ten_wo ** 3 / rhowo_hybrid ** 3) ** 0.25
                        alpha_L = 6.122 * (9.8 * ten_wo / rhowo_hybrid) ** 0.25

                        # 计算Merkel·
                        if 0.9 < Lfi <= 1.125:
                            ka = 1319 * (Ga * 3.6) ** 0.69 * (Gw * 3.6) ** 0.40 / 3600  # 1m S
                        elif 1.125 < Lfi <= 1.375:
                            ka = 1447 * (Ga * 3.6) ** 0.66 * (Gw * 3.6) ** 0.35 / 3600  # 1.25m S wave
                        elif 1.375 < Lfi <= 1.75:
                            ka = 1483 * (Ga * 3.6) ** 0.69 * (Gw * 3.6) ** 0.30 / 3600  # 1.5m S wave
                        elif 1.75 < Lfi <= 2.1:
                            ka = 1690 * (Ga * 3.6) ** 0.70 * (Gw * 3.6) ** 0.23 / 3600  # 2m S wave

                        Nw = ka * Afr_fill * Lfi / mww
                        Ncc= We.Merkel2(mww,Twow,Tpfo,cpwpm,mav15,ha1,pa1)
                        if Ncc < 0:
                            Twow = Twow + 2

                        delta_Tpo = Nw - Ncc
                        t1 = t1 + 1

                        if t1 > 1000:
                            t1 = 1
                    hao = Qwb_hybrid / mai_b_hybrid + hai_hybrid
                    Tao = (Tin + Twow) / 2 # assume
                    delta_Tao = 0.001
                    while abs(delta_Tao) >= 1e-6:
                        if delta_Tao > 0:
                            Tao = Tao - min(0.1, 1 * abs(delta_Tao))
                        else:
                            Tao = Tao + min(0.1, 1 * abs(delta_Tao))

                        Twbo = Tao
                        pvwbo,wo,_ =EN.Environment_calculate(Twbo,Tao,pa1)
                        cpao,cpwo,cpvo=EN.cp_calculate(Tao)
                        haoc = cpao * (Tao - 273.15) + wo * (EN.ifgwo + cpvo * (Tao - 273.15))
                        cpav5m = cpao + wo * cpvo
                        delta_Tao = (haoc - hao) / hao

                    rhoav5,_ =EN.rhoa_calculate(Tao,wo,pa1)
                    rhoav15 = 2 / (1 / rhoavi_hybrid + 1 / rhoav5)
                    mavo_b_hybrid = mai_b_hybrid * (1 + wo)
                    mavm_b_hybrid = (mav15 + mavo_b_hybrid) / 2
                    mav1 = mai_b_hybrid * (1 + w1)
                    mav5 = mai_b_hybrid * (1 + wo)
                    vav34 = mavm_b_hybrid / rhoav15 / Afr_fill
                    Ana = 2 * H3 * Bfi
                    vav5 = mav5 / rhoav5 / Afr_fill
                    miuao, miuvo, miuavo = Environment.nian_calculate(Tao, wo)
                    Ry = mavo_b_hybrid / (miuavo * Afr_fill)

                    Knafi, Krzfi, Kfs_Kctcfi, Kfi, Kspfi=tower.K_wet(rhoav15, rhoavi_hybrid, Afr_fill, Ana, mav1, mavm_b_hybrid, alpha_miu, miuavi, alpha_Rhow, alpha_L,
                    Wfi, vav3, EN.Kfs_Kctc, mav5, rhoav5, Gw, Ga, Lfi, Hsp, mavo_b_hybrid, H3, alpha_v,mav15,vav5)






                    Ana = 2 * H3 * Bfi;
    return mevap,q_woer



















