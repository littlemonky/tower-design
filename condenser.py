from asset_config import Unit

unit = Unit()

def condenser_main(Fc, tw, qv):
    #TODO
    Tc, delta_hc, Dpai, Pcn, W = unit.W_calculate(Fc, tw, qv)

    return Tc, delta_hc, Dpai, Pcn, W
