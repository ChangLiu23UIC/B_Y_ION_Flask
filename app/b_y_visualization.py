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



def read_isotope_csv(filename:str) -> dict:
    """
    This will get a dictionary of abundances and mass for each of the isotope of the
    :param filename: str
    :return: dict
    """
    isotope_dict = {}
    isotopes = pd.read_csv("isotope.csv")
    for index, item in isotopes.iterrows():
        if item["Name"] in isotope_dict:
            isotope_dict[item["Name"]].append((item["Mass"],item["Abundance"]))
        else:
            isotope_dict[item["Name"]] = [(item["Mass"],item["Abundance"])]
    return isotope_dict



# def isotope_weight(peptide:str, isotope_info:dict) -> float:
#     peptide_atom_counts = peptide_composition(peptide)
#     print(peptide_atom_counts)
#     print(isotope_info)
#
#     for atom, count in peptide_atom_counts.items():
#         atom_isotopes = isotope_info[atom]

        # distribution = random.multinomial()



def calculate_isotopic_variants(composition, isotopes,mono_mass, max_changes):
    # Create a list of elements and the number of each in the peptide
    elements = list(itertools.chain.from_iterable([[elem] * count for elem, count in composition.items()]))
    variants = {0: (mono_mass, 1.0)}  # Start with monoisotopic mass

    # Calculate all variants for up to max_changes isotopic substitutions
    for change in range(1, max_changes + 1):
        for subs in itertools.combinations_with_replacement(elements, change):
            mass_diff = sum(isotopes[elem][1][0] - isotopes[elem][0][0] for elem in subs)
            prob = np.prod([isotopes[elem][1][1] / isotopes[elem][0][1] for elem in subs])
            mass = mono_mass + mass_diff
            if change in variants:
                variants[change].append((mass, prob))
            else:
                variants[change] = [(mass, prob)]

    # Sum the probabilities of variants with the same mass
    summed_variants = defaultdict(float)
    for change, var_list in variants.items():
        for mass, prob in var_list:
            summed_variants[mass] += prob

    # Sort variants by mass and convert to list of tuples
    sorted_variants = sorted(summed_variants.items())
    return sorted_variants



def isotope_visualize(b_frag:list, y_frag:list, isotope_dict:dict):
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


if __name__ == '__main__':
    isotopes = pd.read_csv("isotope.csv")
    isotope_dict = read_isotope_csv("isotope.csv")
    # isotope_weight("PEPTIDE", isotope_dict)
