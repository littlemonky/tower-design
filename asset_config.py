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
        self.n = 11350 * 4  # 管子根数
        self.dic = 0.024  # 内径
        self.doc = 0.025  # 外径
        self.A = 2.381011747530507e+04 * 4 #换热面积
        self.L = self.A / (math.pi * self.doc * self.n)  # 管长

    def rhoaw_calculate(self, tw):
        rhoaw = (1.49343e-3 - 3.7164e-6 * (tw + 273.15) + 7.09782e-9 * (tw + 273.15) ** 2 - 1.90321e-20 * (
                tw + 273.15) ** 6) ** -1
        return rhoaw

    def hc_coef_calculate(self, vw, tw):
        K0 = 12.87 * vw ** 5 - 145.1 * vw ** 4 + 638.4 * vw ** 3 - 1525 * vw ** 2 + 3007 * vw + 714.7
        Fw = 1.151 * math.exp(-((tw - 55.95) / 75.15) ** 2) + 0.07026 * math.exp(-((tw - 20.01) / 14.15) ** 2)
        Fm = (0.002362 * self.L1 ** 2 - 0.2093 * self.L1 + 4.056) / (self.L1 + 3.863)
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



