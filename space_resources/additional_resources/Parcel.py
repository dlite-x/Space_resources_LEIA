# -*- coding: utf-8 -*-
"""
Description:
    This script defines the ChemicalParcel class where the parcel of regolith
    is processed and passed through the various systems to be produce 
    oxygen. 

@author: Dorian Leger
@date: 22/07/2021
"""


class ChemicalParcel():

    def __init__(self, regolith_mass, ilmenite_concentration,
                 regolith_distance, regolith_depth, Extract_EnerCost_kJ_kg,
                 TransCostkWh_kg_m, Benef_EnerCost_kWh_kg,
                 Carbo_EnerCost_kWh_kg, Sabat_HeatProduced_kWh_per_molCO2,
                 EnergyCost_HeatDissipation,
                 Electro_eff, Liquefy_carnot_eff):

        self.stage = "Pre-extracted"
        self.step = 0
        self.regolith_mass = regolith_mass
        self.ilmenite_concentration = ilmenite_concentration
        self.regolith_distance = regolith_distance
        self.regolith_depth = regolith_depth
        self.ilmenite_mass = self.ilmenite_concentration*(
            self.regolith_mass)
        self.otherminerals_mass = self.regolith_mass-self.ilmenite_mass
        self.energyConsumed = 0
        self.CO2_mols = 0
        self.H2O_mols = 0
        self.O2_mols = 0

        # define process parameters
        self.Extract_EnerCost_kJ_kg = Extract_EnerCost_kJ_kg
        self.TransCostkWh_kg_m = TransCostkWh_kg_m
        self.Benef_EnerCost_kWh_kg = Benef_EnerCost_kWh_kg
        self.Carbo_EnerCost_kWh_kg = Carbo_EnerCost_kWh_kg
        self.Sabat_HeatProduced_kWh_per_molCO2 = (
            Sabat_HeatProduced_kWh_per_molCO2)
        self.EnergyCost_HeatDissipation = EnergyCost_HeatDissipation
        self.Electro_eff = Electro_eff
        self.Liquefy_carnot_eff = Liquefy_carnot_eff

        self.Extract_EnerCost_total = 0
        self.Transport_EnerCost_total = 0
        self.Benef_EnerCost_total = 0
        self.Carbo_EnerCost_total = 0
        self.Sabat_EnerCost_total = 0
        self.Electro_EnerCost_total = 0
        self.Liquefy_EnerCost_total = 0

    def pristine(self):
        self.stage = ("in the ground regolith")
        self.step = 0

    def extraction(self):
        self.stage = "extracted"
        self.step = 1

        # call excavation_model_script to calculate energy cost for RASSOR
        # to excavate regolith at given soil depth
        rassor_energyperkg = excavation_model_script.energy_analysis(
            self.regolith_depth,
            self.Extract_EnerCost_kJ_kg)

        exc_energycost_kJ = rassor_energyperkg*self.regolith_mass
        # convert to kWh
        exc_energycost_kWh = exc_energycost_kJ/3600

        # kWh/kg regolith extracted
        #self.Extract_EnerCost_kWh_kg = 0.0006
        self.Extract_EnerCost_total = exc_energycost_kWh
        self.energyConsumed = self.energyConsumed + (
            self.Extract_EnerCost_total)

    def transportation(self):
        self.stage = "transported to station"
        self.step = 2
        # kWh/kg regolith transported
        Transport_EnerCost_kWh_per_InputRegol_kg = (
            self.regolith_distance * self.TransCostkWh_kg_m)

        self.Transport_EnerCost_total = (
            Transport_EnerCost_kWh_per_InputRegol_kg*self.regolith_mass)

        self.energyConsumed = self.energyConsumed + (
            self.Transport_EnerCost_total)

    def beneficiation(self):

        #self.beneficiation_pass =  self.beneficiation_pass+1
        self.stage = "beneficiation"

        self.step = 3
        # iterate through for amount of beneficiation passes
        # for i in range(self.beneficiation_pass):
        # kWh/kg regolith extracted
        # no energy value added yet for above

        self.Benef_EnerCost_total += self.Benef_EnerCost_kWh_kg*(
            self.regolith_mass)

        # add the same energy cost to energyConsumed for iteration
        self.energyConsumed += self.Benef_EnerCost_kWh_kg*(
            self.regolith_mass)

        # initial masses
        # self.otherminerals_mass= self.regolith_mass*(
        #                        1-self.ilmenite_concentration)

        # self.ilmenite_mass =  self.regolith_mass*(
        #                    self.ilmenite_concentration)

        # self.otherminerals_mass= self.regolith_mass*(
        #                       1-(self.ilmenite_concentration/100))

        # self.ilmenite_mass =  self.regolith_mass*(
        #                    self.ilmenite_concentration/100)

        # after beneficiation pass        +
        ###### New stuff #########
        # give percentage of ilmenite recovered from original ilmenite
        # mass from Quinn et al. (2013)
        # have different values for datasets for Vials A to D
        vialA_ilmenite = 1.6/2
        vialB_ilmenite = 1.4/2
        vialC_ilmenite = 1.6/2
        vialD_ilmenite = 1.7/2

        # For ilmenite recovered percent, taking mean value of all
        # ilmenite recovered fractions
        ilmenite_recovered_percent = (vialA_ilmenite + vialB_ilmenite +
                                      vialC_ilmenite + vialD_ilmenite)/4

        # give percentage of remaining other minerals in regolith
        # from Quinn et al. (2013) Tables 6 to 9 Bin 2 and 3 (Vials A to D)
        vialA_other = 8.3/18
        vialB_other = 8.8/18
        vialC_other = 11.2/18
        vialD_other = 11.7/18

        # For other minerals recovered percent, taking mean value of all
        # other mineral recovered fractions
        other_recovered_percent = (vialA_other + vialB_other + vialC_other +
                                   vialD_other)/4

        # define amount of gangue in target bins
        #self.otherminerals_mass = self.otherminerals_mass * 0.44
        self.otherminerals_mass = self.otherminerals_mass * (
            other_recovered_percent)
        # define mass of ilmenite
        #self.ilmenite_mass = self.ilmenite_mass * 0.75
        self.ilmenite_mass = self.ilmenite_mass * (ilmenite_recovered_percent)

        self.regolith_mass = self.ilmenite_mass+self.otherminerals_mass

        self.ilmenite_concentration = self.ilmenite_mass/(
            self.regolith_mass)

    def carbothermalreactor(self):
        self.stage = "CarboReacted"
        self.step = 4

        self.Carbo_EnerCost_total = (
            self.Carbo_EnerCost_kWh_kg*self.regolith_mass)

        self.energyConsumed = self.energyConsumed + (
            self.Carbo_EnerCost_total)

        # eventually should use this to pull integral value from a file
        start_temp_kelvin = 273.15  # 0 ceclius
        end_temp_kelvin = 1173.15  # 900 ceclius

        self.ilmenite_mass = self.ilmenite_concentration * (
            self.regolith_mass)  # in kg

        self.ilmenite_mols = self.ilmenite_mass / 0.152
        # mols = mass (kg) / mass 0.157 kg /mols

        self.CO2_mols = 0.5*self.ilmenite_mols
        self.ilmenite_mols = 0
        self.regolith_mass = 0
        self.ilmenite_concentration = 0
        self.ilmenite_mass = 0

    def sabatierreactor(self):
        self.stage = "SabatierReacted"
        self.step = 5

        Sabat_Cooling_Cost_per_molCO2 = (
            self.Sabat_HeatProduced_kWh_per_molCO2 * (
                self.EnergyCost_HeatDissipation))

        # pumping coolant cost below based on ISS calculations
        Sabat_EnerCost_kWh_per_InputCO2_mol = (
            Sabat_Cooling_Cost_per_molCO2)

        self.Sabat_EnerCost_total = (
            Sabat_EnerCost_kWh_per_InputCO2_mol*self.CO2_mols)

        self.energyConsumed = self.energyConsumed + (
            self.Sabat_EnerCost_total)

        self.H2O_mols = 2*self.CO2_mols
        self.CO2_mols = 0

    def electrolyzer(self):
        self.stage = "Electrolyzed"
        self.step = 6

        # change efficiency to a decimal value to reflect percentage
        self.Electro_eff = self.Electro_eff/100
        # define combustion energy of one mol of H2 (kJ/mol)
        combust_ener_mol_H2 = 260

        # calculate energy cost per input mol of H2
        Electro_EnerCost_kJ_per_H2_mol = combust_ener_mol_H2/self.Electro_eff

        Electro_EnerCost_kWh_per_InputH2O_mol = (
            Electro_EnerCost_kJ_per_H2_mol/3600)

        self.Electro_EnerCost_total = (
            Electro_EnerCost_kWh_per_InputH2O_mol*self.H2O_mols)

        self.energyConsumed = self.energyConsumed + (
            self.Electro_EnerCost_total)

        self.O2_mols = 0.5*self.H2O_mols
        self.H2O_mols = 0

    def liquefaction(self):
        self.stage = "Liquefied_Oxygen"
        self.step = 7
        # convert liquefy_carnot_eff to a percentage value
        self.Liquefy_carnot_eff = self.Liquefy_carnot_eff/100

        # define parameters that will affect the energy cost
        temp_int = 360  # units: K
        temp_liq = 90  # units: K

        cp_mol = 29  # units: J/mol/K
        O2_molar_mass = 32  # units: g/mol

        heat_of_vap = 6800  # units: J/mol
        delta_t = temp_int - temp_liq

        q_cold = (cp_mol*delta_t)+heat_of_vap  # units: J
        carnot_ideal = delta_t/temp_liq

        carnot_actual = carnot_ideal/self.Liquefy_carnot_eff

        liq_work = carnot_actual*q_cold
        # basis is 1 mol O2
        # calculate work/mol O2
        work_mol_O2 = liq_work/1000  # units: kJ/mol O2
        # convert to kWh for energy cost calculations
        Liquefy_EnerCost_kWh_per_InputO2_mol = work_mol_O2/3600

        self.Liquefy_EnerCost_total = (
            Liquefy_EnerCost_kWh_per_InputO2_mol*self.O2_mols)
        self.energyConsumed = self.energyConsumed + (
            self.Liquefy_EnerCost_total)
