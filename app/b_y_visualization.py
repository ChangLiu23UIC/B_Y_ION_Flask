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


def multinomial_probability(n, outcomes):
    """
    Calculate the multinomial probability.

    :param n: Total number of trials (int)
    :param outcomes: A list of tuples, where each tuple contains the count and probability of each outcome.
    :return: The multinomial probability (float)
    """
    if sum([count for count, _ in outcomes]) != n:
        raise ValueError("The sum of the counts must equal n.")

    # Calculate the factorial of n
    factorial_n = math.factorial(n)

    # Calculate the product of the factorials of the counts and the power of probabilities
    denominator = 1
    probability_product = 1
    for count, probability in outcomes:
        if count < 0 or probability < 0 or probability > 1:
            raise ValueError("Counts and probabilities must be non-negative, and probabilities must not exceed 1.")
        denominator *= math.factorial(count)
        probability_product *= probability ** count

    # Calculate the multinomial probability
    multinomial_prob = factorial_n / denominator * probability_product
    return multinomial_prob


def sum_of_products(list1, list2):
    """
    Calculate the sum of products of corresponding elements from two lists.

    :param list1: First list of numbers
    :param list2: Second list of numbers
    :return: Sum of products of corresponding elements
    """
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length.")

    # Calculate sum of products using a list comprehension and sum function
    result = sum(x * y for x, y in zip(list1, list2))
    return result


def prob_calc(atom, iso_num, total_num, iso_dict):

    prob_list = [mass[1] for mass in iso_dict[atom]]
    mass_list = [mass[0] for mass in iso_dict[atom]]
    diff_num = len(prob_list)-1
    prob_result_list = []
    mass_result_list = []
    for possible_isotopes in get_combinations(diff_num, iso_num):
        atom_distribution = [total_num-iso_num] + [get_combinations(diff_num, len(iso_dict[atom]))]
        probability_result = multinomial_probability(total_num, list(zip(atom_distribution, prob_list)))
        prob_result_list.append(probability_result)

        mass = sum_of_products(atom_distribution, mass_list)
        mass_result_list.append(mass)

    return [prob_result_list, mass_result_list]


def isotope_calculator(peptide:str, iso_dict):
    result = {}
    molecular_dict = peptide_composition(peptide)
    for i in range(5):
        comb_list = get_combinations(len(molecular_dict), i)
        atom_list = [atoms for atoms, count in molecular_dict.items()]
        for combs in comb_list:
            # will show how many of the atoms are there ex: [(4,C),(0,H)]
            features = list(zip(combs, atom_list))
            prob = 1
            for iso_num, atom_name in features:
                prob *= prob_calc(atom_name, iso_num, molecular_dict[atom_name], iso_dict)



if __name__ == '__main__':
    isotope_dict = read_isotope_csv("isotope.csv")
    sample = peptide_composition("PEPTIDEMAMIMIASANAGI")
    # samples = dict_to_formula(sample)
    # dd = isotope_calculator("SAMPLER", isotope_dict)
    # isotope_weight("PEPTIDE", isotope_dict)
