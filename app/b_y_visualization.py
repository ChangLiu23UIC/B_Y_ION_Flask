from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Label
import pandas as pd
from numpy import random
from protein_calculate import *
from scipy.stats import multinomial
from itertools import combinations_with_replacement, product
from collections import Counter
import numpy as np
import itertools
import math
import itertools
from collections import defaultdict

def read_isotope_csv(filename: str) -> dict:
    """
    This will get a dictionary of abundances and mass for each of the isotope of the
    :param filename: str
    :return: dict
    """
    isotope_dict = {}
    isotopes = pd.read_csv("isotope.csv")
    for index, item in isotopes.iterrows():
        if item["Name"] in isotope_dict:
            isotope_dict[item["Name"]].append((item["Mass"], item["Abundances"]))
        else:
            isotope_dict[item["Name"]] = [(item["Mass"], item["Abundances"])]
    return isotope_dict


# def isotope_weight(peptide:str, isotope_info:dict) -> float:
#     peptide_atom_counts = peptide_composition(peptide)
#     print(peptide_atom_counts)
#     print(isotope_info)
#
#     for atom, count in peptide_atom_counts.items():
#         atom_isotopes = isotope_info[atom]

# distribution = random.multinomial()


def isotope_visualize(b_frag: list, y_frag: list, isotope_dict: dict):
    """

    :param b_frag:
    :param y_frag:
    :param isotope_dict:
    :return:
    """
    b_frag = []


def spectrum_visualization(b_y_dataframe: pd.DataFrame):
    """
    This will take the b_y_fragment dataframe with the isotopic mass dictionary to calculate the peaks of different mass
    and then use bokeh to visualize it.

    :param b_y_dataframe:
    :return:
    """
    mainTitle = 'Isotope Fragmentation Mass Spectrum'


def get_combinations(isotope_num, atom_num):
    """
    Generate all combinations of isotopes that sum up to a certain atom number.

    Parameters:
    isotope_num (int): Number of isotopes/buckets to distribute atoms into.
    atom_num (int): Total number of atoms to distribute.

    Returns:
    list: List of all possible combinations of isotopes.
    """
    def generate_combinations(remaining_atoms, remaining_isotopes, current_combination):
        if remaining_isotopes == 0:
            if remaining_atoms == 0:
                return [current_combination]
            else:
                return []

        combinations = []
        for atoms in range(remaining_atoms + 1):
            combinations.extend(
                generate_combinations(
                    remaining_atoms - atoms,
                    remaining_isotopes - 1,
                    current_combination + [atoms]
                )
            )
        return combinations

    return generate_combinations(atom_num, isotope_num, [])


def isotope_calculator(peptide:str, iso_dict):
    molecular_dict = peptide_composition(peptide)
    for i in range(5):
        comb_list = get_combinations(len(molecular_dict), i)
        atom_list = [atoms for atoms, count in molecular_dict.items()]
        for combs in comb_list:
            # will show how many of the atoms are there ex: [(4,C),(0,H)]
            features = list(zip(combs, atom_list))
            C_prob = (math.comb(molecular_dict[features[0][1]], features[0][0])
                      * pow(iso_dict[features[0][1]][1][1],features[0][0])
                      * pow(iso_dict[features[0][1]][0][1],i - features[0][0]))
            print("FEAUTURE is : ")
            print(features)
            print("Isotope dict is :")
            print(iso_dict)
            print("molecular formula is :")
            print(molecular_dict)
            print("All the possibile combination is:")
            print(comb_list)

            # print(C_prob)

if __name__ == '__main__':
    isotope_dict = read_isotope_csv("isotope.csv")
    sample = peptide_composition("SAMPLER")
    # samples = dict_to_formula(sample)
    dd = isotope_calculator("SAMPLER", isotope_dict)
    # isotope_weight("PEPTIDE", isotope_dict)


