from asset_config import Unit

unit = Unit()

def condenser_main(qv, xpai, Pcn, Qpai):
    #TODO
    #Tc, delta_hc, Dpai, Pcn, W = unit.W_calculate(Fc, tw, qv)
    tin,Tc=unit.tin_calculate(qv,xpai,Pcn,Qpai)
    return tin,Tc

    #return Tc, delta_hc, Dpai, Pcn, W

