import numpy as np
import os


def tac_column(Problem):
    """
    # ### >> Total Annual Cost << Conventional Distillation Column ########
    #     - Investment costs:
    #           * Tower
    #           * Trays
    #           * Reboiler
    #           * Condenser
    #     - Operating Costs
    #           * Heating Steam
    #           * Cooling Water 
    #----------------------------------------------------------------------
    """

    # 01 # Recover Hysys Objects from structure Problem
    HyObject = Problem.HyObject  # Main Aspen Hysys Objects
    MaterialStream = HyObject.MaterialStream  # Column material streams
    EnergyStream = HyObject.EnergyStream  # Column energy streams

    # 02 # Import Data from Aspen Hysys Model
    NT = HyObject.DistColumn.Main_TS.NumberOfTrays  # Column Active  Trays
    NT = np.ceil(NT / 0.7)  # Trays efficiency correction

    TD = MaterialStream.Distillate.Temperature.GetValue('C')  # Distillate Temperature
    TB = MaterialStream.Bottoms.Temperature.GetValue('C')  # Residue Temperature
    TF = HyObject.DistColumn.FeedMainTS.Temperature.GetValue('C')  # Feed Temperature
    VF = MaterialStream.Vapor.Temperature.GetValue('C') # Kettle Reboiler Temperature

    Qcond = EnergyStream.Qcond.HeatFlow.GetValue('kW')  # Condenser duty
    Qreb = EnergyStream.Qreb.HeatFlow.GetValue('kW')  # Reboiler Duty
    Qpreheat = EnergyStream.Qpreheat.HeatFlow.GetValue('kW')  # Preheating Duty
    Qflash = EnergyStream.Qflash.HeatFlow.GetValue('kW') # Flashing duty

    # 03 # Run Aspen Hysys Script "Col_diam_V8.SCP" to update column diameter
    # Problem.HyObject.HyCase.Application.PlayScript(os.path.abspath('Column_Diameter.SCP'))

    column_diameter = HyObject.DistColumn.Main_TS.ColumnDiameterValue  # [m]

    # # Equipment and Utility Parameter Cost ##################################

    # * CEPIC
    CEPIC_Actual = 567.5  # Annual Index 2017
    CEPIC_2001 = 397  # Base Annual Index
    UpdateFactor = CEPIC_Actual / CEPIC_2001

    # * Annualization Factor parameters ***************************************
    i = 0.1  # interest_rate
    n = 8  # equipment life time yrs

    # * Utility Costs *********************************************************
    WATER = 0.354 * (1 / 1e9) * 3600 * 1e3  # $/GJ [30 ºC to 40-45 ºC] (R.Turton 4º Ed. Table 8.3) ==> [$ /kW·h]
    STEAM = 14.04 * (1 / 1e9) * 3600 * 1e3  # $/GJ Low Pressure Steam [5barg, 160ºC] (R.Turton 4º Ed. Table 8.3) ==> [$ /kW·h]
    STEAM_HP = 17.70 * (1 / 1e9) * 3600 * 1e3 # $/GJ High Pressure Steam
    YEAR = 8000  # Operating hours per year

    # * Equip Cost Constants (K). See Appendix A - R .Turton ******************
    Ktray = np.array([2.9949, 0.4465, 0.3961])  # Trays (sieves)               Area    m2
    Ktower = np.array([3.4974, 0.4485, 0.1074])  # Towers (tray)                Volume  m3
    Khx = np.array([4.3247, -0.3030, 0.1634])  # Heat Exchanger (fixed tube)  Area    m2
    Kettle = np.array([4.4646, -0.5277, 0.3955])  # Kettle Reboiler


    # * Bare module Cost Factor: direct and indirect costs for each unit ******
    FBMtray = 1  # Table A.6 & Figure A.9 (Trays - sieve trays)
    FBMtower = (2.25 + 1.82 * 1.0)  # Table A.4 & Figure A.8 (Process vessels - vertical (including towers)) 
    FBMhx = (1.63 + 1.66 * 1.3)  # Table A.4 & Figure A.8 (fixed tube sheet)
    FBMKettle = (1.63 + 1.66 * 1.7) # Table A.4 & Figure A.8 (fixed tube sheet)

    # * Cooler ****************************************************************
    Ucooler = 800  # [W/(m2 K)] 
    Twin = 30  # Cooling water inlet  [ºC]
    Twout = 40  # Cooling water outlet  Condenser [ºC]

    # * Heater ****************************************************************
    Uheater = 820  # [W/(m2 K)]
    Tstm = 160  # Low Pressure Steam Temperature (R.Turton 4º Ed. Table 8.3)
    Tstm_high = 254  # High Pressure Steam Temperature

    # Tower Column
    tray_Spacing = 0.6096  # [m]    

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> # END Equipment and Utility Parameter Cost

    # 04 # Operating Cost ########################################################

    # * Cooling Water Cost [$/yr] *********************************************
    coolingWater_Cost = Qcond * WATER * YEAR

    # * Steam Cost [$/yr] *****************************************************
    Steam_Cost = Qreb * STEAM_HP * YEAR
    Preheating_Cost = Qpreheat * STEAM * YEAR
    Flashing_Cost = Qflash * STEAM * YEAR

    # 05 # Capital Cost ##########################################################

    # * Column dimensions
    column_area = np.pi * np.square(column_diameter) / 4  # Sieve area [m2]
    column_height = (3 + NT) * tray_Spacing  # Tower Height [m] (0.7 to account for tray efficiency)
    column_volume = column_area * column_height  # Volume Tower [m3]

    # * Column Shell **********************************************************
    # Purchase cost  for base conditions
    column_Cp0 = 10 ** (Ktower[0] + Ktower[1] * np.log10(column_volume) +
                        Ktower[2] * (np.log10(column_volume) ** 2))

    # Bare Module cost
    column_CBM_old = column_Cp0 * FBMtower
    column_CBM = column_CBM_old * UpdateFactor  # [$] ======================

    # * Column trays **********************************************************
    # Purchase cost  for base conditions
    tray_Cp0 = 10 ** (Ktray[0] + Ktray[1] * np.log10(column_area) +
                      Ktray[2] * (np.log10(column_area) ** 2))
    # Tray factor
    if NT < 20:
        Fq = 10 ** (0.4771 + 0.0816 * np.log10(NT) - 0.3473 * (np.log10(NT)) ** 2)
    else:
        Fq = 1

    # Bare Module cost
    tray_CBM_old = tray_Cp0 * FBMtray * Fq
    tray_CBM = tray_CBM_old * NT * UpdateFactor  # [$] ================

    # * Column Condenser ******************************************************
    inc_T_cond = ((TD - Twout) - (TD - Twin)) / np.log((TD - Twout) / (TD - Twin))
    condenser_area = Qcond / (Ucooler * inc_T_cond) * 1e3  # *1e3 porque U esta en W.

    # Purchase cost  for base conditions
    condenser_Cp0 = 10 ** (Khx[0] + Khx[1] * np.log10(condenser_area) +
                           Khx[2] * (np.log10(condenser_area) ** 2))

    # Condenser Bare Module cost
    condenser_CBM_old = condenser_Cp0 * FBMhx
    condenser_CBM = condenser_CBM_old * UpdateFactor  # [$] ================

    # * Column Reboiler *****************************************************************************************************
    inc_T_reb = Tstm_high - TB
    reboiler_area = Qreb / (Uheater * inc_T_reb) * 1e3  # *1e3 porque U esta en W.

    # Purchase cost  for base conditions
    reboiler_Cp0 = 10 ** (Khx[0] + Khx[1] * np.log10(reboiler_area) + Khx[2] * (np.log10(reboiler_area) ** 2))

    # Reboiler Bare Module cost
    reboiler_CBM_old = reboiler_Cp0 * FBMhx
    reboiler_CBM = reboiler_CBM_old * UpdateFactor  # [$] ==================

    # * Preheater  ***********************************************************************************************************
    delta_in = 160 - 111.2
    delta_out = 159 - TF
    LMTD = (delta_in - delta_out) / (np.log(delta_in) - np.log(delta_out))
    # LMTD = 160 - TF
    preheat_area = Qpreheat / (Uheater * LMTD) * 1e3  # 1e3 to change kW to W

    # Purchase cost  for base conditions
    preheater_Cp0 = 10 ** (Khx[0] + Khx[1] * np.log10(preheat_area) + Khx[2] * (np.log10(preheat_area) ** 2))

    # Preheater Bare Module cost
    preheater_CBM_old = preheater_Cp0 * FBMhx
    preheater_CBM = preheater_CBM_old * UpdateFactor  # [$] ==================

    # * Kettle Reboiler *****************************************************************************************************
    delta_T = Tstm - VF
    kettle_area = Qflash / (Uheater * delta_T) * 1e3  # *1e3 convert kW to W

    if (kettle_area < 100):
        # Purchase cost  for base conditions
        kettle_Cp0 = 10 ** (Kettle[0] + Kettle[1] * np.log10(kettle_area) + Kettle[2] * (np.log10(kettle_area) ** 2))

        # Reboiler Bare Module cost
        kettle_CBM_old = kettle_Cp0 * FBMKettle
        kettle_CBM = kettle_CBM_old * UpdateFactor  # [$] ==================
    else:
        kettle_area = kettle_area/2
        # Purchase cost  for base conditions
        kettle_Cp0 = 10 ** (Kettle[0] + Kettle[1] * np.log10(kettle_area) + Kettle[2] * (np.log10(kettle_area) ** 2))

        # Reboiler Bare Module cost
        kettle_CBM_old = kettle_Cp0 * FBMKettle
        kettle_CBM = kettle_CBM_old * UpdateFactor  # [$] ==================
        kettle_CBM = kettle_CBM * 2


    # 06 # Total Annual Cost #####################################################

    # * Total Operating Cost
    Cop = coolingWater_Cost + Steam_Cost + Preheating_Cost + Flashing_Cost

    # * Total Capital Cost
    Ccap = column_CBM + tray_CBM + condenser_CBM + reboiler_CBM + preheater_CBM + kettle_CBM

    # * Discounted annualisation factor based on interest rate and num of years
    # F = i * (1 + i) ** n / ((1 + i) ** n - 1)

    # * Payback period for 3 years
    F = 1/3

    # * TAC ===================================================================
    TAC = (Cop + Ccap * F) * 1e-6  # [MM $/yr]

    # ============================================== END TAC calculations #####

    # *Revenue from selling product PG
    Product_MassFlow = HyObject.MaterialStream.Bottoms.MassFlow.GetValue('kg/h')
    PG_price = 2645 / 1e3  # $2,645/tonne PG
    PG_sale = Product_MassFlow * PG_price * YEAR * 1e-6

    class ColumnCost:
        pass

    ColumnCost.CoolingWater = coolingWater_Cost
    ColumnCost.Stea = Steam_Cost
    ColumnCost.Shell = column_CBM
    ColumnCost.Trays = tray_CBM
    ColumnCost.condenser = condenser_CBM
    ColumnCost.reboiler = reboiler_CBM
    ColumnCost.TAC = TAC - PG_sale

    return (ColumnCost)
