import math
import numpy as np
import pandas as pd
import CoolProp.CoolProp as CP


class Unit:
    def __init__(self):

        self.low_limit = 1
        self.high_limit = 25
        self.design_power = 10000  # kw
        # self.ref2 = 0
        self.design_param = {
            "D0": 0,
            "Ngd": 0,
            "P0d": 0,
            "P1d": 0,
            "P2d": 0,
            "P3d": 0,
            "P4d": 0,
            "P5d": 0,
            "P6d": 0,
            "P7d": 0,
            "PL": 0,
            "Pcnd": 0,
            "pw3b": 0,
            "Pwc": 0,
            "tw1d": 0,
            "tw2d": 0,
            "tw3bd": 0,
            "tw3d": 0,
            "tw4d": 0,
            "tw5d": 0,
            "tw6d": 0,
            "tw7d": 0,
            "twcd": 0,
            "td1d": 0,
            "td2d": 0,
            "td4d": 0,
            "td5d": 0,
            "td6d": 0,
            "td7d": 0,
            "h1_in_P_d": 0,
            "h2_in_P_d": 0,
            "h3_in_P_d": 0,
            "h4_in_P_d": 0,
            "h5_in_P_d": 0,
            "h6_in_P_d": 0,
            "h7_in_P_d": 0,
            "rh1_in_P_d_es_d": 0,
            "rh2_in_P_d_es_d": 0,
            "rh1_in_P_d_ms_d": 0,
            "rh1_out_P_es_d": 0,
            "rh2_out_P_es_d": 0,
            "rh2_in_P_d_ms_d": 0,
            "rh2_out_P_ms_d": 0,
            "lp_in_P_d": 0,
            "h3_out_P_fw_d": 0,
            "sdc1": 0,
            "sdc2": 0,
            "sdc3": 0,
            "sdc4": 0,
            "sdc5": 0,
            "sdc6": 0,
            "sdc7": 0,
            "sdc8": 0,
            "sdc9": 0,
            "xdc1": 0,
            "xdc2": 0,
            "xdc3": 0,
            "xdc4": 0,
            "xdc5": 0,
            "xdc6": 0,
            "xdc7": 0,
            "h1d": 0,
            "h2d": 0,
            "h3d": 0,
            "h4d": 0,
            "h5d": 0,
            "h6d": 0,
            "h7d": 0,
            "hcd": 0,
            "hsg3": 0,
            "t1d": 0,
            "t2d": 0,
            "t3d": 0,
            "t4d": 0,
            "t5d": 0,
            "t6d": 0,
            "t7d": 0,
            "Dsgh": 0,
            "Dsg1": 0,
            "DsgL": 0,
            "Dsg2": 0,
            "Dsg3": 0,
            "Dsg4": 0,
            "Drh2d": 0,
            "Dhd": 0,
            "Dpaid": 0,
            "P0": 0,
            "x0": 0,
            "x1": 0,
            "x2": 0,
            "x3": 0,
            "x5": 0,
            "x6": 0,
            "x7": 0,
            "x8": 0,
            "xc": 0,
        }

        # self.D0 = 0
        # self.Ngd = 1
        # self.P0d = 0
        # self.P1d = 0
        # self.P2d = 0
        # self.P3d = 0
        # self.P4d = 0
        # self.P5d = 0
        # self.P6d = 0
        # self.PL = 0
        # self.P7d = 0
        # self.Pcnd = 0
        # self.pw3b = 0
        #
        # self.tw1d = 0
        # self.tw2d = 0
        # self.tw3bd = 0
        # self.tw3d = 0
        # self.tw4d = 0
        # self.tw5d = 0
        # self.tw6d = 0
        # self.tw7d = 0
        # self.twcd = 0
        #
        # self.td1d = 0
        # self.td2d = 0
        # self.td4d = 0
        # self.td5d = 0
        # self.td6d = 0
        # self.td7d = 0
        #
        # self.h1_in_P_d = 0
        # self.h2_in_P_d = 0
        # self.h3_in_P_d = 0
        # self.h4_in_P_d = 0
        # self.h5_in_P_d = 0
        # self.h6_in_P_d = 0
        # self.h7_in_P_d = 0
        # self.rh1_in_P_d_es_d = 0
        # self.rh2_in_P_d_es_d = 0
        # self.rh1_in_P_d_ms_d = 0
        # self.rh1_out_P_es_d = 0
        # self.rh2_out_P_es_d = 0
        # self.rh2_in_P_d_ms_d = 0
        # self.rh2_out_P_ms_d = 0
        # self.lp_in_P_d = 0
        # self.h3_out_P_fw_d = 0
        #
        # self.sdc1 = 0
        # self.sdc2 = 0
        # self.sdc3 = 0
        # self.sdc4 = 0
        # self.sdc5 = 0
        # self.sdc6 = 0
        # self.sdc7 = 0
        # self.sdc8 = 0
        # self.sdc9 = 0
        # self.xdc1 = 0
        # self.xdc2 = 0
        # self.xdc3 = 0
        # self.xdc4 = 0
        # self.xdc5 = 0
        # self.xdc6 = 0
        # self.xdc7 = 0
        # self.h1d = 0
        # self.h2d = 0
        # self.h3d = 0
        # self.h4d = 0
        # self.h5d = 0
        # self.h6d = 0
        # self.h7d = 0
        # self.hcd = 0
        # self.hsg3 = 0
        #
        # self.t1d = 0
        # self.t2d = 0
        # self.t3d = 0
        # self.t4d = 0
        # self.t5d = 0
        # self.t6d = 0
        # self.t7d = 0
        # self.Dsgh = 0
        # self.Dsg1 = 0
        # self.DsgL = 0
        # self.Dsg2 = 0
        # self.Dsg3 = 0
        # self.Dsg4 = 0
        # self.Drh2d = 0
        # self.Dhd = 0
        # self.Dpaid = 0
        # self.P0 = 0
        # self.x0 = 0
        # self.x1 = 0
        # self.x2 = 0
        # self.x3 = 0
        # self.x5 = 0
        # self.x6 = 0
        # self.x7 = 0
        # self.x8 = 0
        # self.xc = 0

        # self.cqys1 = (self.P1d - self.h1_in_P_d) / self.P1d
        # self.cqys2 = (self.P2d - self.h2_in_P_d) / self.P2d
        # self.cqys3 = (self.P3d - self.h3_in_P_d) / self.P3d
        # self.cqys4 = (self.P4d - self.h4_in_P_d) / self.P4d
        # self.cqys5 = (self.P5d - self.h5_in_P_d) / self.P5d
        # self.cqys6 = (self.P6d - self.h6_in_P_d) / self.P6d
        # self.cqys7 = (self.P7d - self.h7_in_P_d) / self.P7d
        # self.cqys8 = (self.P1d - self.rh1_in_P_d_es_d) / self.P1d
        # self.cqys9 = (self.P0d - self.rh2_in_P_d_es_d) / self.P0d
        # self.cqys10 = (self.P3d - self.rh1_in_P_d_ms_d) / self.P3d
        # self.cqys11 = (self.rh1_in_P_d_es_d - self.rh1_out_P_es_d) / self.rh1_in_P_d_es_d
        # self.cqys12 = (self.rh2_in_P_d_es_d - self.rh2_out_P_es_d) / self.rh2_in_P_d_es_d
        # self.cqys13 = (self.rh1_in_P_d_ms_d - self.rh2_in_P_d_ms_d) / self.rh1_in_P_d_ms_d
        # self.cqys14 = (self.rh2_in_P_d_ms_d - self.rh2_out_P_ms_d) / self.rh2_in_P_d_ms_d
        # self.cqys15 = (self.rh2_out_P_ms_d - self.lp_in_P_d) / self.rh2_out_P_ms_d
        # self.cqys16 = (self.lp_in_P_d - self.h3_out_P_fw_d) / self.lp_in_P_d

    def y01_predict(self, Dh):
        '''Dh: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y01_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     x = Dh / 3.6
        #     y01 = model.predict([[x, x**2]])[0]
        # else:
        y01 = (-0.0000054 * (Dh / 3.6) ** 2 + 0.01721 * (Dh / 3.6) + 69.1874) / 100
        return y01

    def y12_predict(self, Dh):
        '''Dh: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y12_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y12 = model.predict([[Dh]])[0]
        # else:
        y12 = 0.8241
        return y12

    def y23_predict(self, Dh):
        '''Dh: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y23_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y23 = model.predict([[Dh]])[0]
        # else:
        y23 = 0.8592
        return y23

    def y34_predict(self, D34):  # D34修改为h3-h4 / h3，下面同理
        '''D34: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y34_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y34 = model.predict([[D34]])[0]
        # else:
        y34 = 0.01682 * (D34 / (3.6 * 1141.48)) ** 3 - 0.05816 * (D34 / (3.6 * 1141.48)) ** 2 + 0.05839 * (
                D34 / (3.6 * 1141.48)) + 0.91345
        return y34

    def y45_predict(self, D45):
        '''D45: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y45_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y45 = model.predict([[D45]])[0]
        # else:
        y45 = 0.22996 * (D45 / (3.6 * 2691.95)) ** 3 - 0.51404 * (D45 / (3.6 * 2691.95)) ** 2 + 0.31073 * (
                D45 / (3.6 * 2691.95)) + 0.87809
        return y45

    def y56_predict(self, D56):
        '''D56: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y56_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y56 = model.predict([[D56]])[0]
        # else:
        y56 = 0.23511 * (D56 / (3.6 * 2696.425)) ** 3 - 0.52188 * (
                D56 / (3.6 * 2696.425)) ** 2 + 0.31248 * (
                      D56 / (3.6 * 2696.425)) + 0.78785
        return y56

    def y67_predict(self, D67):
        '''D67: 实际运行数据'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y67_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y67 = model.predict([[D67]])[0]
        # else:
        y67 = 0.24659 * (D67 / (3.6 * 2382.375)) ** 3 - 0.54228 * (
                D67 / (3.6 * 2382.375)) ** 2 + 0.32169 * (
                      D67 / (3.6 * 2382.375)) + 0.41018
        return y67

    def y7c_predict(self, Dpai):
        '''Dpai: 模型输出'''
        # new_model_path = glob.glob(os.getcwd() + '/model/y7c_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     y7c = model.predict([[Dpai]])[0]
        # else:
        y7c = -1.49369051e+02 * (Dpai / 3.6) + 2.47633038e-01 * (Dpai / 3.6) ** 2 - 1.82154008e-04 * (
                Dpai / 3.6) ** 3 + 5.01584504e-08 * (Dpai / 3.6) ** 4 + 33731.39809323318
        return y7c

    def b1_predict(self):
        '''汽水分离器效率'''
        # new_model_path = glob.glob(os.getcwd() + '/model/b1_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     b1 = 0.9756
        # else:
        b1 = 0.9756
        return b1

    def b2_predict(self):
        ''''''
        # new_model_path = glob.glob(os.getcwd() + '/model/b2_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     b2 = 0.9756
        # else:
        b2 = 0.9756
        return b2

    def bsep_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/bsep_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     bsep = 0.9662
        # else:
        bsep = 0.9662
        return bsep

    def c1_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/c1_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     c1 = 0.9901
        # else:
        c1 = 0.9901
        return c1

    def c2_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/c2_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     c2 = 0.9885
        # else:
        c2 = 0.9885
        return c2

    def c6_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/c6_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     c6 = 0.9039
        # else:
        c6 = 0.9039
        return c6

    def c7_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/c7_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     c7 = 0.0203
        # else:
        c7 = 0.0203
        return c7

    def cL_predict(self):
        # new_model_path = glob.glob(os.getcwd() + '/model/cL_model_*.pkl')
        # if len(new_model_path) > 0:
        #     with open(new_model_path[-1], 'rb') as f:
        #         model = pickle.load(f)
        #     cL = 0.01655
        # else:
        cL = 0.01655
        return cL

    def real_power_predict(self, Pcn):
        '''
        根据背压计算机组功率
        :param Pcn: 背压，Mpa
        :return: 功率，W
        '''
        W = -0.411 * (Pcn * 1000) ** 6 + 21.1 * (Pcn * 1000) ** 5 - 443.7 * (Pcn * 1000) ** 4 + \
            4861 * (Pcn * 1000) ** 3 + -2.827e+04 * (Pcn * 1000) ** 2 + 6.444e+04 * (
                    Pcn * 1000) - 2.769e+04 + 1263640.056
        return W

    def Tc_calculate(self, tw, qv, Fc):

        # 初始化
        condenser = Condenser()
        water = Water()

        # Tc初始化
        Tc = tw + 15
        # 根据设计参数计算的全局参数
        rhoaw = water.rhoaw_calculate(tw)
        mw = qv * rhoaw  # kg/s
        vw = mw / (rhoaw * condenser.n * np.pi * condenser.dic ** 2 / 4)  # 体积流量
        K0, Fw, Fm = condenser.hc_coef_calculate(vw, tw)
        Kc = 0.001 * K0 * Fw * Fm * Fc

        delta_hc = condenser.delta_hc_predict(Tc)
        Dpai = condenser.Dpai_predict(Tc)
        twater = Dpai * 1000 / 3600 * delta_hc / (water.cpw * mw) + tw
        while Tc < twater:
            Tc = twater + 2.8
            continue
        delta_T = 1
        while abs(delta_T) > 0.000001:
            delta_hc = condenser.delta_hc_predict(Tc)
            Dpai = condenser.Dpai_predict(Tc)
            Q = Dpai * 1000 / 3600 * delta_hc
            twater = Dpai * 1000 / 3600 * delta_hc / (water.cpw * mw) + tw
            Tm = (twater - tw) / np.log(abs((Tc - tw) / (Tc - twater)))
            Qh = Kc * condenser.A * Tm
            delta_T = ((Q - Qh) / Q)
            if delta_T > 0:
                Tc = Tc + 0.5 * abs(delta_T)
            else:
                Tc = Tc - 0.5 * abs(delta_T)

        return Tc, delta_hc, Dpai

    def tin_calculate(self,mw , xpai, Pcn, Qpai):
        # 初始化
        condenser = Condenser()
        water = Water()
        # 初始化tw
        tw = 35 + 273.15
        # 根据设计参数计算的全局参数
        rhoaw = water.rhoaw_calculate(tw)
        vw = mw / (rhoaw * condenser.n * np.pi * condenser.dic ** 2 / 4)  # 体积流量
        Fc = 0.9
        Tc = CP.PropsSI('T', 'P', Pcn * 1e6, 'Q', xpai, 'water')  # 背压kpa，Ts为K
        # 计算tw
        delta_tw = 1
        while abs(delta_tw) > 0.001:
            if delta_tw < 0:
                tw += abs(delta_tw) * 0.5
            else:
                tw -= abs(delta_tw) * 0.5

            K0, Fw, Fm = condenser.hc_coef_calculate(vw, tw)
            Tml = Qpai / (K0 * Fc * Fm * condenser.A * Fw)
            Tw2 = (Tc * (1 - np.exp(Qpai / (water.cpw*1e3 * mw * Tml))) + Qpai / (water.cpw*1e3 * mw)) / (
                    1 - np.exp(Qpai / (water.cpw*1e3 * mw * Tml)))
            tw_c = Tw2 - Qpai / (water.cpw * mw)
            delta_tw = (tw - tw_c)
        tin = Tw2
        return tin,Tc




    def W_calculate(self, Fc, tw, qv):
        '''
        根据凝结水温计算系统功率
        :param Fc:
        :param tw:
        :param qv:
        :return: 系统功率， 单位：W
        '''
        Tc, delta_hc, Dpai = self.Tc_calculate(tw, qv, Fc)  # 凝结水温℃
        Pcn = CP.PropsSI('P', 'T', Tc + 273.15, 'Q', 0, 'water') / 1e6  # 背压Mpa
        W = self.real_power_predict(Pcn)
        return Tc, delta_hc, Dpai, Pcn, W

class GenericPump(Unit):
    def pump_nominal_curve_params(self, serial_number):
        # pumps = []
        pump_df = pd.read_csv(
            r"D:\cooling_system_2024\cooling-system\models\pump_nominal_curve_fit\pump_nominal_curve_fit.csv")
        pump_df = pump_df.loc[pump_df["serial_number"]==serial_number]
        pump = pump_df.iloc[-1].to_dict()
        return pump["pump_a"], pump["pump_b"], pump["pump_c"]

    def head_calculate(self, flow, pump_a, pump_b, pump_c):
        '''
        循环水泵流量-扬程特性曲线： ax2+bx+c
        :param flow: 工况点的流量
        :param pump_a: 曲线参数
        :param pump_b: 曲线参数
        :param pump_c: 曲线参数
        :return: 扬程
        '''
        head = pump_a * flow ** 2 + pump_b * flow + pump_c
        return head

    def pump_efficiency_curve_params(self):
        # pumps = []
        yita_df = pd.read_csv(r"D:\cooling_system_2024\cooling-system\models\pump_efficiency_curve_fit\pump_efficiency_curve_fit.csv")
        yita = yita_df.iloc[-1].to_dict()
        # for sn in pump_df["serial_number"].unique():
        #     tmp = pump_df.loc[pump_df["serial_number"]==sn].iloc[-1].to_dict()
        #     pump = {
        #         "serial_number":sn,
        #         "pump_a":tmp["pump_a"],
        #         "pump_b": tmp["pump_b"],
        #         "pump_c": tmp["pump_c"],
        #     }
        #     pumps.append(pump)
        return yita["x1"], yita["x2"], yita["x3"]

    def yita_calculate(self, qvc, yita_a, yita_b, yita_c):
        '''循环水泵效率曲线'''
        yita = yita_a * qvc ** 3 + yita_b * qvc ** 2 + yita_c * qvc
        return yita

class HighSpeedPump:
    design_flow = 12.3
    design_speed = 290 # rpm
    shaft_power = 2200
    run_flow = 12.3

class LowSpeedPump:
    design_flow = 9.8
    design_speed = 245  # rpm
    shaft_power = 1500
    run_flow = 9.8

class VariableFrequencyPump:
    design_flow = 12
    design_speed = 280
    flow_low_limit = 0.5
    flow_high_limit = 1.2
    design_flow_low_limit = design_flow * flow_low_limit
    design_flow_high_limit = design_flow * flow_high_limit
    shaft_power = 0
    run_flow = 0
    run_speed = 0



class Water:
    def __init__(self):
        self.cpw = 4.1868  # 水的比热容，单位：kJ/kg·°C

    def rhoaw_calculate(self, tw):
        '''
        海水密度计算
        :param tw: 海水温度，单位：℃
        :return: 海水密度 kg/m³
        '''
        rhoaw = (1.49343e-3 - 3.7164e-6 * (tw + 273.15) + 7.09782e-9 * (tw + 273.15) ** 2 -
                 1.90321e-20 * (tw + 273.15) ** 6) ** -1
        return rhoaw

class Condenser:
    # CONDENSER
    def __init__(self):
        self.L1 = 0.5  # 管子厚度
        self.n = 11350 * 4 *2.2/2.4 # 管子根数
        self.dic = 0.024  # 内径
        self.doc = 0.025  # 外径
        self.A = 2.381011747530507e+04 * 4 #换热面积
        self.L = self.A / (math.pi * self.doc * self.n)  # 管长

    def rhoaw_calculate(self, tw):
        rhoaw = (1.49343e-3 - 3.7164e-6 * (tw + 273.15) + 7.09782e-9 * (tw + 273.15) ** 2 - 1.90321e-20 * (
                tw + 273.15) ** 6) ** -1
        return rhoaw

    def hc_coef_calculate(self, vw, tw):
        K0 = 13.4104059308519 * vw ** 3 - 247.967203038242 * vw ** 2 + 1777.52195205562 * vw + 1159.57058483348
        Fw = 1.50389194485069e-05 * (tw - 273.15) ** 3 - 0.00155775284546543 * (tw - 273.15) ** 2 + 0.0569694891299058 * (tw - 273.15)
        Fm = (-0.00220502672681781 * self.L1 ** 3 + 0.0277623084227847 * self.L1 ** 2 - 0.207941532573436 * self.L1 + 1.04968398936745) * 1.7616
        return K0, Fw, Fm

    def delta_hc_predict(self, Tc):
        delta_hc = (2359.65882 - 16.76611 * Tc + 0.47495 * Tc ** 2 - 0.00411 * Tc ** 3)
        return delta_hc

    def Dpai_predict(self, Tc):
        Dpai = (3064.7522 + 5.53756 * Tc ** 1 + 0.00607 * Tc ** 2 + 7.82717E-5 * Tc ** 3)
        return Dpai

    def condensate_side(self, Tc):
        delta_hc = self.delta_hc_predict(Tc)  # train 焓差
        Dpai = self.Dpai_predict(Tc)  # train 排汽流量
        Q = Dpai * 1000 / 3600 * delta_hc  # 排汽热量
        return delta_hc, Dpai, Q

class Tube(Unit):
    # def __init__(self):
    #     self.low_limit = 1
    #     self.high_limit = 25

    def tube_curve_params(self):
        # 读取管路特性曲线参数
        tube_df = pd.read_csv(r"D:\cooling_system_2024\cooling-system\models\tube_curve_fit\tube_curve_fit.csv")
        tube = tube_df.iloc[-1].to_dict()
        return tube["tube_a"], tube["tube_c"]

    def head_calculate(self, flow, tube_a, tube_c):
        '''循环水泵效率曲线'''
        head = tube_a * flow ** 2 + tube_c
        return head

class CoolingTower:
    def __init__(self):
        self.nts = 80  # number of tower supports
        self.Lts = 13.67 * 1.6  # length of tower support, m
        self.dts = 0.5  # diameter of tower support, m
        self.Cdts = 2.0  # drag coeffient of support
        self.ts = 0.8  # thickness of the square-edged (90°) shell at the inlet to the tower, m
        self.ri_d3 = 0.02  # variable ri_d3

    def epsTan(self,Ta5,w5,cpw5,cpv5,cpa5,pa5):
        EN=Environment()
        epsTa5 = -(1 + w5) * EN.g * (1 + 0.42216e-11 * w5 ** 2 * pa5 * math.exp(5406.1915 / Ta5) * (
                EN.ifgwo - (cpw5 - cpv5) * (Ta5 - 273.15)) / ((w5 + 0.622) * EN.T * Ta5)) / (
                         (cpa5 + w5 * cpv5) + 3.6693e-8 * w5 ** 2 * pa5 * math.exp(5406.1915 / Ta5) * (
                         EN.ifgwo - (cpw5 - cpv5) * (Ta5 - 273.15)) / Ta5 ** 2)

        return epsTa5


class HeatExchanger:
    def __init__(self):
        self.d = 0.025  # hydraulic diameter of tube, m
        self.relativeroughness = 5.24 * 10 ** (-4)
        self.Pt = 0.058  # transversal tube pitch, 管间距
        #self.Ats = np.pi * self.Di ** 2 / 4  # inside cross-sectional flow area, m**2
        self.Ati = np.pi * self.d  # inside area of the tube per unit length, m
        self.ratiomf = 0.433  # ratio of minimum to free stream flow area
        self.Kci = 0.05  # inlet contraction loss coefficient

        self.a11 = -0.605
        self.a12 = 4.34
        self.a13 = -9.72
        self.a14 = 7.54
        self.a21 = 0.0231
        self.a22 = 0.0059
        self.a23 = -0.248
        self.a24 = 0.287
        self.a31 = 0.294
        self.a32 = -1.99
        self.a33 = 4.32
        self.a34 = -3
        self.a41 = 0.0198
        self.a42 = -0.305
        self.a43 = 0.897
        self.a44 = -0.731

    def HA_calculate(self, Tin, Two,mw,cpw,Ats,nb,ntb,nwp,Lte,v,Afrd):
        niuwd = 2.414e-5 * 10 ** (247.8 / ((Tin + Two) / 2 - 140))  # 水运动粘度
        Lamdawd = -6.14255e-1 + 6.9963e-3 * ((Tin + Two) / 2) - 1.01075e-5 * (
                (Tin + Two) / 2) ** 2 + 4.74737e-12 * ((Tin + Two) / 2) ** 4  # 水热导率
        Prwd = niuwd * cpw / Lamdawd
        Rhoaw = 1 / (1.49343e-3 - 3.7164e-6 * ((Tin + Two) / 2) + 7.09782e-9 * (
                (Tin + Two) / 2) ** 2 - 1.90321e-20 * ((Tin + Two) / 2) ** 6)
        rhow = (1.49343e-3 - 3.7164e-6 * ((Tin + Two) / 2) + 7.09782e-9 * ((Tin + Two) / 2) ** 2 - 1.90321e-20 * (
                (Tin + Two) / 2) ** 6) ** (-1)
        Uw = mw / rhow / (Ats * nb * 2 * ntb / nwp)
        Rewd = mw * nwp * self.d / Ats / ntb / nb / niuwd
        f = (1.82 * math.log10(Rewd) - 1.64) ** -2  # 水侧Darcy阻力系数
        Nuwd = (f / 8) * (Rewd - 1000) * Prwd * (1 + (self.d / Lte) ** (2 / 3)) / (
                    1 + 12.7 * (f / 8) ** 0.5 * ((Prwd) ** (2 / 3) - 1))  # 水侧换热的Nu数
        hw = Nuwd * Lamdawd / self.d  # 当前水侧雷诺数下的换热系数
        ha = 37.2674 * (v ** 0.327)
        haeAa = ha * Afrd * 71.8
        Aw = self.Ati * Lte * ntb * nb
        HA = 1 / (1 / haeAa + 1 / (hw * Aw))
        return HA

    def Ft_calculate(self,Tind, Ta7, Twod, Ta6):
        delta_t = ((Tind - Ta7) - (Twod - Ta6)) / math.log(
            abs((Tind - Ta7) / (Twod - Ta6)))  # the logarithmic mean temperature difference
        s1 = (Tind - Twod) / (Tind - Ta6)
        s2 = (Ta7 - Ta6) / (Tind - Ta6)
        s12 = s1 / s2
        s3 = abs((s1 - s2) / math.log(abs((1 - s2) / (1 - s1))))
        arctan = math.atan(s12)
        Ft = 1 - self.a11 * (1 - s3) * math.sin(2 * arctan) - self.a12 * (1 - s3) ** 2 * math.sin(
            2 * arctan) - self.a13 * (1 - s3) ** 3 * math.sin(2 * arctan) - \
             self.a14 * (1 - s3) ** 4 * math.sin(2 * arctan) - self.a21 * (1 - s3) * math.sin(4 * arctan) - self.a22 * (
                         1 - s3) ** 2 * math.sin(4 * arctan) - \
             self.a23 * (1 - s3) ** 3 * math.sin(4 * arctan) - self.a24 * (1 - s3) ** 4 * math.sin(
            4 * arctan) - self.a31 * (1 - s3) * math.sin(6 * arctan) - \
             self.a32 * (1 - s3) ** 2 * math.sin(6 * arctan) - self.a33 * (1 - s3) ** 3 * math.sin(
            6 * arctan) - self.a34 * (1 - s3) ** 4 * math.sin(6 * arctan) - \
             self.a41 * (1 - s3) * math.sin(8 * arctan) - self.a42 * (1 - s3) ** 2 * math.sin(8 * arctan) - self.a43 * (
                         1 - s3) ** 3 * math.sin(8 * arctan) - \
             self.a44 * (1 - s3) ** 4 * math.sin(8 * arctan)
        return  Ft,delta_t

    def K_dry(self,v06,aj,rhoa7,rhoa6):
        Khe=51.756 - 32.614 * v06 + 11.682 * v06**2 - 2.0986 * v06**3 + 0.1808 * v06**4 - 0.0059 * v06**5
        ajm=0.0019 * aj**2 + 0.9133 * aj - 3.1558  # mean inlet flow angle
        Kd=math.exp(5.488405 - 0.2131209 * aj + 3.533265e-3 * aj**2 - 0.2901016e-4 * aj**3)  # the downstream loss coefficient
        Kheaj=Khe+ 2 * rhoa7 * (1 / math.sin(ajm / 180 * math.pi) - 1) / (rhoa6 + rhoa7) * (
                (1 / math.sin(ajm / 180 * math.pi) - 1) + 2 * self.Kci**0.5) + 2 * rhoa6 * Kd / (rhoa6 + rhoa7)
        return Kheaj



class Environment:
    def __init__(self):
        self.R = 8.3144598 / 28.966 * 1e3
        self.g = 9.81
        self.Rv = 461.52
        self.T = 273.15
        self.ifgwo = 3.4831814e6 - 5.8627703e3 * self.T + 12.139568 * self.T ** 2 - 1.40290431e-2 * self.T ** 3
        self.Ma = 28.97
        self.Mv = 18.016
        self.Va = 29.9
        self.Vv = 18.8

    def Environment_calculate(self,Twb,Ta,pa):
        z= 10.79586 * (1 - 273.16 / Twb) + 5.02808 * math.log10(273.16 / Twb) + 1.50474e-4 * (1 - 10 ** (-8.29692 * (Twb / 273.16 - 1))) + 4.2873e-4*(10**(4.76955*(1-273.16/Twb))-1)+2.786118312
        pv=10**z
        w=(2501.6-2.3263*(Twb-273.15))/(2501.6+1.8577*(Ta-273.15)-4.184*(Twb-273.15))*(0.62509*pv)/(pa-1.005*pv)-(1.00416*(Ta-Twb))/(2501.6+1.8577*(Ta-273.15)-4.184*(Twb-273.15))
        RH=pa*w/(0.622+w)/pv
        return pv, w, RH

    def rhoa_calculate(self,Ta,w,pa):
        rhoav=(1+w)*(1-w/(w+0.62198))*pa/(self.R*Ta)
        rhoa=pa/(self.R*Ta)
        return rhoav,rhoa

    def cp_calculate(self, Ta):
        cpa = 1.045356e3 - 3.161783e-1 * (Ta + 273.15) / 2 + 7.083814e-4 * ((Ta + 273.15) / 2) ** 2 - 2.705209e-7 * (
                (Ta + 273.15) / 2) ** 3
        cpv = 1.3605e3 + 2.31334 * (Ta + 273.15) / 2 - 2.46784e-10 * ((Ta + 273.15) / 2) ** 5 + 5.91332e-13 * (
                (Ta + 273.15) / 2) ** 6
        cpw = 8.15599e3 - 2.80627e1 * (Ta + 273.15) / 2 + 5.11283e-2 * ((Ta + 273.15) / 2) ** 2 - 2.17582e-13 * (
                (Ta + 273.15) / 2) ** 6
        return cpa,cpw,cpv

    def Tan_calculate(self,Ta,pa1,hn,w):
        Tan=Ta-0.00975*hn
        pan=pa1*(1-(0.00975*hn/Ta))**(3.5*(1+w)*(1-w/(w+0.62198)))

        return Tan,pan

    def nian_calculate(self, Ta, w):
        Xa = 1 / (1 + 1.608 * w)
        Xv = w / (w + 0.622)
        nian_a = 2.287973e-6 + 6.259793e-8 * Ta - 3.131956e-11 * Ta ** 2 + 8.15038e-15 * Ta ** 3
        nian_v = 2.562435e-6 + 1.816683e-8 * Ta + 2.579066e-11 * Ta ** 2 - 1.067299e-14 * Ta ** 3
        nian_av = (Xa * nian_a * self.Ma ** 0.5 + Xv * nian_v * self.Mv ** 0.5) / (
                    Xa * self.Ma ** 0.5 + Xv * self.Mv ** 0.5)
        return nian_a,nian_v,nian_av

class Wet_section:
    def __init__(self):
        self.Lsp = 0.5  # depth of spray zone above fill,m
        self.dd = 0.0035  # mean drop diameter in rain zone,m
        self.Kfs_Kctc = 0.5  # loss coefficient for contraction and fill supports based on Afr
        self.Kwd = 0.5  # loss coefficient for water distribution system
        self.ae6 = 1.01

    def Merkel1(self, pa1, Ta1, Twow,nian_av1,rhoav1,Ga,Gw,vav3,aden,h3,w1,Lfi,anian,rhowo,aL,av):
        EN=Environment()
        D1 = 0.04357 * Ta1 ** 1.5 * (1 / EN.Ma + 1 / EN.Mv) ** 0.5 / pa1 / ((EN.Va ** 0.333 + EN.Vv ** 0.333) ** 2)
        Sc1=nian_av1/(rhoav1*D1)
        zwo = 10.79586 * (1 - 273.16 / Twow) + 5.02808 * math.log10(273.16 / Twow) + 1.50474 * 10 ** (-4) * (1 - 10 ** (-8.29692 * ((Twow / 273.16) - 1))) + 4.2873 * 10 ** (-4) * (10 ** (4.76955 * (1 - 273.16 / Twow)) - 1) + 2.786118312
        pvwo = 10 ** zwo
        ws1 = (2501.6 - 2.3263 * (Twow - 273.15)) / (2501.6 + 1.8577 * (Twow - 273.15) - 4.184 * (Twow - 273.15)) * (0.62509 * pvwo) / (pa1 - 1.005 * pvwo)
        Merz = 12 * (D1 / vav3 / self.dd) * (h3 / self.dd) * (pa1 / EN.Rv / Ta1 / rhowo) * Sc1 ** 0.33 * (
                math.log((ws1 + 0.622) / (w1 + 0.622)) / (ws1 - w1)) * (
                       0.90757 * aden * rhoav1 - 30341.04 * anian * nian_av1 - 0.37564 + 4.04016 *
                       ((0.55 + 41.7215 * (aL * self.dd) ** 0.80043) * (0.713 + 3.741 * (aL * h3) ** (-1.23456)) *
                        (3.11 * math.exp(0.15 * av * vav3) - 3.13) * math.exp((5.3759 * math.exp(-0.2092 * aL * h3)) *
                                                                              math.log(0.3719 * math.exp(0.0019055 * aL * self.dd) + 0.55))))
        Mepfi = 0.25575 * Gw ** (-0.094) * Ga ** 0.6023 * Lfi
        Mesp = 0.2 * self.Lsp * (Ga / Gw) ** 0.5
        Nw = Merz + Mepfi + Mesp
        return Nw

    def Merkel2(self,mww,Twow,Tinw,cpw1,mav15,hai,pa1):
        Tw11 = Twow + 0.1 * (Tinw - Twow)
        Tw12 = Twow + 0.4 * (Tinw - Twow)
        Tw13 = Twow + 0.6 * (Tinw - Twow)
        Tw14 = Twow + 0.9 * (Tinw - Twow)

        hav11 = mww * cpw1 * (Tw11 - Twow) / mav15 + hai
        hav12 = mww * cpw1 * (Tw12 - Twow) / mav15 + hai
        hav13 = mww * cpw1 * (Tw13 - Twow) / mav15 + hai
        hav14 = mww * cpw1 * (Tw14 - Twow) / mav15 + hai

        pvsa11 = 9.8 * 1e3 * 10 ** (
                    1.0141966 - 3.142305 * (1e3 / Tw11 - 1e3 / 373.16) + 8.2 * math.log10(373.16 / Tw11) - 0.0024804 * (
                        373.16 - Tw11))
        hsa11c = (1.005 * (Tw11 - 273.15) + (2500 + 1.842 * (Tw11 - 273.15)) * 0.622 * pvsa11 / (pa1 - pvsa11)) * 1e3

        pvsa12 = 9.8 * 1e3 * 10 ** (
                    1.0141966 - 3.142305 * (1e3 / Tw12 - 1e3 / 373.16) + 8.2 * math.log10(373.16 / Tw12) - 0.0024804 * (
                        373.16 - Tw12))
        hsa12c = (1.005 * (Tw12 - 273.15) + (2500 + 1.842 * (Tw12 - 273.15)) * 0.622 * pvsa12 / (pa1 - pvsa12)) * 1e3

        pvsa13 = 9.8 * 1e3 * 10 ** (
                    1.0141966 - 3.142305 * (1e3 / Tw13 - 1e3 / 373.16) + 8.2 * math.log10(373.16 / Tw13) - 0.0024804 * (
                        373.16 - Tw13))
        hsa13c = (1.005 * (Tw13 - 273.15) + (2500 + 1.842 * (Tw13 - 273.15)) * 0.622 * pvsa13 / (pa1 - pvsa13)) * 1e3

        pvsa14 = 9.8 * 1e3 * 10 ** (
                    1.0141966 - 3.142305 * (1e3 / Tw14 - 1e3 / 373.16) + 8.2 * math.log10(373.16 / Tw14) - 0.0024804 * (
                        373.16 - Tw14))
        hsa14c = (1.005 * (Tw14 - 273.15) + (2500 + 1.842 * (Tw14 - 273.15)) * 0.622 * pvsa14 / (pa1 - pvsa14)) * 1e3

        Ncc = cpw1 * (Tinw - Twow) / 4 * (
                    1 / (hsa11c - hav11) + 1 / (hsa12c - hav12) + 1 / (hsa13c - hav13) + 1 / (hsa14c - hav14))
        return Ncc

    def K_wet(self, rhoav15, rhoav1, mav1, mav15, Gav1, Gav5, rhoav5, mav5, Afrw, d3, h3, Lfi, Gw, Ga, aden, anian, nian_av1, nian_av5, aL, av, vw3,Gav15,vav3):
        CT=CoolingTower()
        Kfs_Kctc = self.Kfs_Kctc  # Use the attribute defined within the class
        Kfsfi_Kctcfi = Kfs_Kctc * rhoav15 / rhoav1 * (mav1 / mav15)**2
        Kfdm = 1.851 * Lfi * Gw**1.2752 * Ga**(-1.0356)
        Kfi = Kfdm + (Gav5**2 / rhoav5 - Gav1**2 / rhoav1) / (Gav15**2 / rhoav15)
        A3 = math.pi * d3**2 / 4
        Kctefi = (1 - Afrw / A3)**2 * (rhoav15 / rhoav5) * (mav5 / mav15)**2
        Kspfi = self.Lsp * (0.4 * (Gw / Ga) + 1) * (rhoav15 / rhoav5) * (mav5 / mav15)**2
        Kwdfi = 0.5 * (rhoav15 / rhoav5) * (mav5 / mav15)**2
        Ry = mav5 / (nian_av5 * Afrw)
        Kdefi = 27.4892 * Ry**(-0.14247) * (rhoav15 / rhoav5) * (mav5 / mav15)**2
        Ktsfi = (CT.Cdts * CT.Lts * CT.dts * CT.nts * Afrw**2 / (math.pi * d3 * h3)**3) * (rhoav15 / rhoav1) * (mav1 / mav15)**2
        Kctfinorz = (0.011266 * math.exp(0.093 * d3 / h3) * 11.07106**2 - 0.3105 * math.exp(0.1085 * d3 / h3) * 11.07106 - 1.7522 + 4.5614 * math.exp(0.131 * d3 / h3) + math.asinh(((10970.2 * math.exp(-0.2442 * 11.07106) + 1391.3) / (d3 / h3 - 15.7258) + 1205.54 * math.exp(-0.23 * 11.07106) + 109.314) * (2 * CT.ri_d3 - 0.01942 / (d3 / h3 - 27.929) - 0.016866))) * (rhoav15 / rhoav1 * (mav1 / mav15)**2 * 4 * Afrw / math.pi / d3**2)**2
        Crz = (0.2394 + 80.1 * (0.0954 / (d3 / h3) + self.dd) * math.exp(0.395 * Gw / Ga) - 0.3195 * (Gw / Ga) - 966 * (self.dd / (d3 / h3)) * math.exp(0.686 * Gw / Ga)) * (1 - 0.06825 * Gw) * 11.07106**0.09667 * math.exp(8.7434 * (1 / d3 - 0.01))
        Kctfi = Crz * Kctfinorz
        Krzfi = 3 * av * vw3 * h3 / self.dd * (0.2246 - 0.31467 * aden * rhoav1 + 5263.04 * anian * nian_av1 + 0.775526 * (1.4824163 * math.exp(71.52 * aL * self.dd) - 0.91) * (0.39364 * math.exp(0.010912 * aL * d3) - 0.17) * (2.0892 * (av * vav3)**(-1.3944) + 0.14) * math.exp((0.8449 * math.log(aL * d3 / 2) - 2.312) * (0.3724 * math.log(av * vav3) + 0.7263) * math.log(206.757 * (aL * h3)**(-2.8344) + 0.43)))*rhoav15/rhoav1*(mav1/mav15)**2*(Afrw/A3)**2
        # K_fi=Ktsfi+Kctfi+Krzfi+Kfsfi_Kctcfi+Kfi+Kctefi+Kspfi+Kwdfi+Kdefi
        return Ktsfi,Kctfi,Krzfi,Kfsfi_Kctcfi,Kfi,Kctefi,Kspfi,Kwdfi,Kdefi

class Machanical_tower:
    def __init__(self):
        self.dd = 4e-3  # rain zone drop diameter
        self.Kctb = 1.5  # bare tube bundle inlet losses
        self.Ktsb = 0.5  # bare tube bundle supports loss coefficient
        self.Kwd = 0.775  # water distribution system 0.5 Kroger 0.775
        self.Krec = -0.3  # plenum recovery
        self.ktf = 17  # tube thermal conductivity W/mK
        self.Ptf = 0.058  # transverse tube pitch
        self.Plf = 0.05022  # lateral tube pitch
        self.dotf = 0.0254  # outer tube diameter
        self.ditf = 0.0216  # inner tube diameter
        self.Rc = 4e-4  # mean thermal contact resistance
        self.df = 0.0572
        self.dr = 0.0276
        self.tft = 0.00025
        self.tf = 0.5e-3  # fin thickness mean
        self.tfr = 0.75e-3  # fin root thickness
        self.Pff = 2.82e-3  # fin pitch
        self.kf = 204  # thermal conductivity of aluminum fin
        self.nrf = 4  # number of tube rows
        self.ntf = 2  # number of tube passes
        self.nbf = 8  # number of heat exchangers
        self.Kna=2.78

    def fin_tube(self,Lt,Hf):
        ntrf = math.ceil(Lt / self.Ptf)
        Afr = self.nbf * Hf * (self.Ptf * (ntrf - 0.5) + self.df)
        Ac = Afr - self.nbf * ntrf * Hf * (
                    self.df * self.tf + (self.Pff - self.tf) * self.dr) / self.Pff  # critical area of airside
        Af = self.nbf * ntrf * self.nrf * Hf / self.Pff * math.pi * (
                    0.5 * (self.df ** 2 - self.dr ** 2) + self.df * self.tft)  # effective airside fin surface
        Aaf = math.pi * (0.5 * (self.df ** 2 - self.dr ** 2) + self.df * self.tft + self.dr * (
                    self.Pff - self.tf)) * self.nbf * ntrf * self.nrf * Hf / self.Pff
        Apf = self.nbf * ntrf * self.nrf * math.pi * Hf * self.ditf  # pipe flow area
        return ntrf,Afr,Ac,Af,Aaf,Apf

    def miua(self,Ta1):
        miua1 = 2.287973 * 10 ** (-6) + 6.259793 * 10 ** (-8) * Ta1 - 3.131956 * 10 ** (-11) * Ta1 ** 2 + 8.15038 * 10 ** (
            -15) * Ta1 ** 3
        return miua1

    def Pravmf(self,w1,miuamf, miuvmf, kamf, kvmf, cpavmf):
        Xa = 1 / (1 + 1.608 * w1)
        Xv = w1 / (w1 + 0.622)
        miuavmf = (Xa * miuamf * Environment.Ma ** 0.5 + Xv * miuvmf * Environment.Mv ** 0.5) / (Xa * Environment.Ma ** 0.5 + Xv * Environment.Mv ** 0.5)
        kavmf = (Xa * kamf * Environment.Ma ** 0.33 + Xv * kvmf * Environment.Mv ** 0.33) / (Xa * Environment.Ma ** 0.33 + Xv * Environment.Mv ** 0.33)
        Pravmf = miuavmf * cpavmf / kavmf
        return Pravmf

    def K_wet(self, rhoav15, rhoavi_hybrid, Afr_fill, Ana, mav1, mavm_b_hybrid, alpha_miu, miuavi, alpha_Rhow, alpha_L,
              Wfi, vav3, Kfs_Kctc, mav5, rhoav5, Gw, Ga, Lfi, Hsp, mavo_b_hybrid, H3, alpha_v,mav15,vav5):
        Knafi = self.Kna * (rhoav15 / rhoavi_hybrid) * (Afr_fill / Ana) ** 2 * (mav1 / mavm_b_hybrid) ** 2

        Krz = 1.5 * alpha_v * vav3 * H3 / self.dd * \
              (0.219164 + 8278.7 * alpha_miu * miuavi - 0.30487 * alpha_Rhow * rhoavi_hybrid + \
               0.954153 * (0.328467 * math.exp(135.7638 * alpha_L * self.dd) + 0.47) * \
               (26.28482 * (alpha_L * H3) ** (-2.95729) + 0.56) * \
               math.exp((math.log(0.204814 * math.exp(0.066518 * alpha_L * Wfi) + 0.21)) * \
                        (3.9186 * math.exp(-0.3 * alpha_L * H3)) * \
                        (0.31095 * math.log(alpha_L * self.dd) + 2.63745)) * \
               (2.177546 * (alpha_v * vav3) ** (-1.46541) + 0.21))
        Krzfi = Krz * (rhoav15 / rhoavi_hybrid) * (mav15 / mavm_b_hybrid) ** 2

        Kfs_Kctcfi = Kfs_Kctc * (rhoav15 / rhoavi_hybrid) * (mav15 / mavm_b_hybrid) ** 2
        Kfdm = 1.851 * Lfi * Gw ** (1.2752) * Ga ** (-1.0356)
        Kfi = Kfdm + (rhoav5 * vav5 ** 2 - rhoavi_hybrid * vav3 ** 2) / (rhoav15 * vav5 ** 2)

        Kspfi = self.Kwd * (rhoav15 / rhoav5) * (mavo_b_hybrid / mavm_b_hybrid) ** 2 + \
                (Hsp * (0.4 * Gw / Ga + 1)) * (rhoav15 / rhoav5) * (mavo_b_hybrid / mavm_b_hybrid) ** 2
        1


        return Knafi,Krzfi,Kfs_Kctcfi,Kfi,Kspfi







































