from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Label
import pandas as pd
from numpy import random
from protein_calculate import *
from scipy.stats import multinomial
from itertools import combinations_with_replacement, product
from collections import Counter
import numpy as np
from math import comb



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



def calculate_isotopic_variants(molecular_formula, isotopes, max_changes=10):
    # Calculate base mass using the most abundant isotope
    base_mass = sum(isotopes[element][0][0] * count for element, count in molecular_formula.items())

    # Generate all possible isotope substitutions for each element
    isotope_combinations = {element: list(combinations_with_replacement(isotopes[element], count))
                            for element, count in molecular_formula.items()}

    # Calculate the mass and abundance of each combination
    results = {}
    for num_changes in range(1, max_changes + 1):
        for selected_elements in combinations_with_replacement(molecular_formula.keys(), num_changes):
            for product_combination in product(*(isotope_combinations[element] for element in selected_elements)):
                # Flatten the list of tuples and count the isotopes
                isotopes_flat = [(element, iso) for element in selected_elements
                                 for iso in product_combination[selected_elements.index(element)]]
                isotope_counts = Counter(isotopes_flat)

                # Calculate mass and abundance for the current combination
                mass = base_mass + sum((iso_mass - isotopes[element][0][0]) * isotope_counts[(element, (iso_mass, iso_abundance))]
                                       for element, (iso_mass, iso_abundance) in isotopes_flat)

                abundance = np.prod([iso_abundance ** isotope_counts[(element, (iso_mass, iso_abundance))]
                                     for element, (iso_mass, iso_abundance) in isotopes_flat])

                # Adjust for the number of identical isotopes in the combination
                for (element, (iso_mass, _)), count in isotope_counts.items():
                    if count > 1:
                        abundance *= comb(molecular_formula[element], count)

                # If this mass has already been calculated, add the abundances
                if mass in results:
                    results[mass] += abundance
                else:
                    results[mass] = abundance

    # Normalize the abundances to sum to 1 (or 100%)
    total_abundance = sum(results.values())
    normalized_results = {mass: abundance / total_abundance for mass, abundance in results.items()}

    return normalized_results



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
