from asset_config import Unit, CoolingTower, HeatExchanger, Environment, Wet_section
import math
import numpy as np

unit = Unit()
CT = CoolingTower()
HE = HeatExchanger()
EN = Environment()
We = Wet_section()


## 基于湿冷塔的干湿联合##
def cooling_tower_main1(h3, d3, h6, d6, h9, d9, d0, Lfi, Afrw, Afrd, l, Lte, ntb, Do, Di, nr, nwp, aj, nb, Ta1, RH, pa1,
                        Tin, mw):
    # TODO
    # tower parameter
    d5 = 151.93 * 1.117 * 1.117

    A6 = math.pi * (d6 / 2) ** 2
    A9 = math.pi * (d9 / 2) ** 2
    A5 = math.pi * (d5 / 2) ** 2
    h8 = h6
    # dry section
    Ats = np.pi * Di ** 2 / 4
    Twb1 = 19.7 + 273.15

    # opration
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
    Ta6, pa6 = EN.Tan_calculate(Ta1, pa1, h6, w1)
    cpa6, cpw6, cpv6 = EN.cp_calculate(Ta6)
    w6 = w1
    rhoav6, rhoa6 = EN.rhoa_calculate(Ta6, w6, pa6)
    ha6 = cpa6 * (Ta6 - 273.15) + w6 * (EN.ifgwo + cpv6 * (Ta6 - 273.15))
    w7 = w6
    Ta10, pa10 = EN.Tan_calculate(Ta1, pa1, h9, w1)
    rhoav10, _ = EN.rhoa_calculate(Ta10, w1, pa10)

    # integration initial
    _, pa8 = EN.Tan_calculate(Ta1, pa1, h6, w1)
    pa8 = pa8 - 45
    v06 = 1.55
    mwd = mw
    mww = mwd
    Tind = Tin
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
                _, cpwdm, _ = EN.cp_calculate(Twdm)
                Qwd = mwd * cpwdm * (Tind - Twod)
                ma67 = v06 * Afrd * rhoa6
                Ta7 = Qwd / (ma67 * cpa6) + Ta6
                HA = HE.HA_calculate(Tind, Twod, mw, cpw1, Ats, nb, ntb, nwp, Lte, v06, Afrd)
                Ft, delta_t = HE.Ft_calculate(Tind, Ta7, Twod, Ta6)
                Qhd = Ft * HA * delta_t
                delta_en_bad = (Qwd - Qhd) / Qwd

            Ta67 = (Ta6 + Ta7) / 2
            rhoa7 = pa8 / (EN.R * Ta7)
            rhoa67 = 2 / (1 / rhoa7 + 1 / rhoa6)
            va7 = ma67 / rhoa7 / Afrd
            Hd = pa6 - pa8
            Kheaj = HE.K_dry(v06, aj, rhoa7, rhoa6)
            Zd = Kheaj * (ma67 / Afrd) ** 2 / (2 * rhoa67) + rhoa7 * va7 ** 2 / 2
            delta_fl_bad = Hd - Zd

        # 更新 delta_fl_bad 为新的误差值
        ## 空冷段计算完，开始计算湿冷段
        Tinw = Twod
        Twow = (Tinw + 2 * Twb1 + Ta1) / 4  # assume
        Twwm = (Tinw + Twow) / 2
        _, cpwm, _ = EN.cp_calculate(Twwm)

        Ta5 = (Tinw + Twow) / 2
        Twb5 = Ta5
        pvwb5, w5, _ = EN.Environment_calculate(Twb5, Ta5, pa8)
        cpa5, cpw5, cpv5 = EN.cp_calculate(Ta5)
        ha5 = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
        mav15 = mww * cpwm * (Tinw - Twow) / (ha5 - hai)
        epsTa5 = CT.epsTan(Ta5, w5, cpw5, cpv5, cpa5, pa8)
        delta_p348w = pa8 * (
                    1 - (1 + epsTa5 * (h8 - h3 - Lfi / 2) / Ta5) ** (-0.021233 * (1 + w5) / (epsTa5 * (w5 + 0.622))))
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
                    _, cpwm, _ = EN.cp_calculate(Twwm)
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
                        pvwb5, _, _ = EN.Environment_calculate(Twb5, Ta5, pa8)
                        w5 = 0.62509 * pvwb5 / (pa5 - pvwb5)
                        ha5c = cpa5 * (Ta5 - 273.15) + w5 * (EN.ifgwo + cpv5 * (Ta5 - 273.15))
                        delta_Ta5 = (ha5c - hao) / hao

                    ma15 = 2 * mav15 / (2 + w1 + w5)
                    mav1 = ma15 * (1 + w1)
                    Ga = ma15 / Afrw
                    vav3 = mav1 / (rhoav1 * Afrw)
                    Nw = We.Merkel1(pa1, Ta1, Twow, nian_av1, rhoav1, Ga, Gw, vav3, aden, h3, w1, Lfi, anian, rhowo, aL,
                                    av)
                    Ncc = We.Merkel2(mww, Twow, Tinw, cpw1, mav15, hai, pa1)
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
            Ta8w = Ta5 + epsTa5 * (h6 - h3 - Lfi / 2)
            rhoav8w = (1 + w5) * (1 - w5 / (w5 + 0.62198)) * pa8 / (EN.R * Ta8w)
            vav8w = mav5 / (rhoav8w * A6)
            delta_p348w = pa5 * (1 - (1 + epsTa5 * (h8 - h3 - Lfi / 2) / Ta5) ** (
                    -0.021233 * (1 + w5) / (epsTa5 * (w5 + 0.622))))
            pa8w = pa1 - delta_p134 - delta_p348w - K_fi * (mav15 / Afrw) ** 2 / (
                    2 * rhoav15) - rhoav8w * vav8w ** 2 / 2
            delta_fl_pa8w = pa8w - pa8

        cpa7, _, cpv7 = EN.cp_calculate(Ta7)
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
        rhoav8, _ = EN.rhoa_calculate(Ta8, w8, pa8)
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
            rhoav9, _ = EN.rhoa_calculate(Ta9, w8, pa9)
            Frd = (mav8 / A9) ** 2 / rhoav9 / (rhoav10 - rhoav9) / EN.g / d9
            pa9c = pa10 + (0.02 * Frd ** (-1.5) - 0.14 / Frd) * (mav8 / A9) ** 2 / rhoav9
            delta_pa9 = pa9 - pa9c

        # 更新 delta_pf 为新的误差值
        vav9 = mav8 / (rhoav9 * A9)
        delta_p89 = pa8 * (1 - (1 + epsTa8 * (h9 - h8) / Ta8) ** (-0.021233 * (1 + w8) / (epsTa8 * (w8 + 0.622))))
        pa8m = pa9 + (rhoav9 * vav9 ** 2) / 2 - (rhoav8 * vav8 ** 2) / 2 + delta_p89
        delta_pf = pa8m - pa8

    Qaw = (ha5c - hai) * mav15
    mwevap = ma15 * (w5 - w1)
    Qad = (ha7 - ha6) * ma67
    evap = mwevap / (Qaw + Qad) * 1e6
    Qww = mww * cpwm * (Tinw - Twow)
    Qwd = mwd * cpwdm * (Tin - Twod)
    Qtot = Qaw + Qad
    q_tower = Qtot
    mevap = mwevap
    # mevap, q_tower =  #机理模型，代理模型对应unit类的某个函数

    return mevap, q_tower


# mevap,q=cooling_tower_main1(18.989,192.6307,60.6255,172.4631,249.091,121.4750,210,2,28021,43056,3.688,31.8909,256,0.0254,0.0234,4,2,27.75,183,296.15,0.81,100000,311,45200)
# print("mevap:", mevap, "q:", q)


# 基于空冷的干湿联合
def cooling_tower_main2(h4, d4, h7, d7, d0, Lfi, Afrw, Afrd, l, Lte, ntb, Do, Di, nr, nwp, aj, nb, Ta1, RH, pa1, Tin,
                        mw):
    ## tower parameter
    A4 = math.pi * (d4 / 2) ** 2
    d3 = d4
    d6 = 152.03
    h3 = h4 / 2
    h6 = We.Lsp + h4 + Lfi
    A3 = math.pi * (d3 / 2) ** 2
    A6 = math.pi * (d6 / 2) ** 2
    A7 = math.pi * (d7 / 2) ** 2
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
        pvwb1, w1, _ = EN.Environment_calculate(Twb1, Ta1, pa1)
        pvs1, _, _ = EN.Environment_calculate(Ta1, Ta1, pa1)
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
    pa4 = EN.Tan_calculate(Ta1, pa1, h6, w1)
    t1 = 1
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
                HA = HE.HA_calculate(Tin, Twod, mw, cpwdm, Ats, nb, ntb, nwp, Lte, v02, Afrd)
                Ft, delta_t = HE.Ft_calculate(Tin, Ta3, Twod, Ta2)
                Qhd = Ft * HA * delta_t
                delta_en_bad = (Qwd - Qhd) / Qwd
                t3 = t3 + 1


            _, rhoa3 = EN.rhoa_calculate(Ta3, w1, pa3)
            rhoa23 = 2 / (1 / rhoa3 + 1 / rhoa2)
            va3 = ma23 / rhoa3 / Afrd
            Hd = pa2 - pa3
            Kheaj = HE.K_dry(v02, aj, rhoa3, rhoa2)
            Zd = Kheaj * (ma23 / Afrd) ** 2 / (2 * rhoa23) + rhoa3 * va3 ** 2 / 2
            delta_fl_bad = Hd - Zd

        Tinw = Twod
        Twow = Tinw - 2
        Twwm = (Tinw + Twow) / 2
        _, cpwm, _ = EN.cp_calculate(Twwm)
        Ta6 = (Tinw + Twow) / 2
        w3 = w1
        cpa3, cpw3, cpv3 = EN.cp_calculate(Ta3)
        ha3 = cpa3 * (Ta3 - 273.15) + w3 * (EN.ifgwo + cpv3 * (Ta3 - 273.15))
        rhoav3, _ = EN.rhoa_calculate(Ta3, w3, pa4)
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
                    cpa6, cpw6, cpv6 = EN.cp_calculate(Ta6)
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
            nian_a6, nian_v6, nian_av6 = EN.nian_calculate(Ta6, w6)
            Ktsfi, Kctfi, Krzfi, Kfsfi_Kctcfi, Kfi, Kctefi, Kspfi, Kwdfi, Kdefi = We.K_wet(rhoav36, rhoav3, mav3, mav36,
                                                                                           Gav3, Gav6, rhoav6, mav6,
                                                                                           Afrw, d4, h4, Lfi, Gw, Ga,
                                                                                           aden, anian, nian_av3,
                                                                                           nian_av6, aL, av, vw3, Gav36,
                                                                                           vav3)
            K_fi = Kctfi + Krzfi + Kfsfi_Kctcfi + Kfi + Kctefi + Kspfi + Kwdfi + Kdefi
            delta_p456 = pa4 * (1 - (
                        (1 - (0.00975 * (h6 - (h4 + Lfi / 2)) / Ta3)) ** (3.5 * (1 + w3) * (1 - w3 / (w3 + 0.62198)))))
            Hw = pa4 - pa6 - delta_p456
            Zw = K_fi * (mav36 / Afrw) ** 2 / (2 * rhoav36)
            pa6m = pa4 - delta_p456 - Zw
            delta_fl_pa6w = pa6m - pa6

        epsTa6 = CT.epsTan(Ta6, w6, cpw6, cpv6, cpa6, pa6)
        delta_pa7 = 0.1
        pa7 = pa6 - 30
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
        t1 = t1 + 1

    Qaw = (ha6 - ha3) * mav36
    mevap = ma36 * (w6 - w3)
    Qad = ma23 * cpa2 * (Ta3 - Ta2)
    Ta3 = Qwd / (ma23 * cpa2) + Ta2
    evap = mevap / (Qaw + Qad) * 1e6
    Qww = mw * cpwm * (Tinw - Twow)
    Qwd = mw * cpwdm * (Tin - Twod)
    q_tower = Qaw + Qad
    return mevap, q_tower


# 分建式，一个主函数，两个塔分别为子函数
def cooling_tower_main3():
    mevap, q_tower1 = cooling_tower_wet()
    q_tower2 = cooling_tower_dry()
    Q_tot = q_tower1 + q_tower2
    return Q_tot, mevap


def cooling_tower_wet(h3, d3, h9, d9, d0, Lfi, Afrw, Ta1, RH, pa1, Tin, mw):
    A9 = math.pi * (d9 / 2) ** 2
    h5 = h3 + We.Lsp + Lfi
    d5 = 152
    A5 = math.pi * (d5 / 2) ** 2
    # opration
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
    Ta6, pa6 = EN.Tan_calculate(Ta1, pa1, h6, w1)
    cpa6, cpw6, cpv6 = EN.cp_calculate(Ta6)
    w6 = w1
    rhoav6, rhoa6 = EN.rhoa_calculate(Ta6, w6, pa6)
    ha6 = cpa6 * (Ta6 - 273.15) + w6 * (EN.ifgwo + cpv6 * (Ta6 - 273.15))
    w7 = w6
    Ta10, pa10 = EN.Tan_calculate(Ta1, pa1, h9, w1)
    rhoav10, _ = EN.rhoa_calculate(Ta10, w1, pa10)

    return mevap, q_tower


def cooling_tower_dry():
    return q_tower





















