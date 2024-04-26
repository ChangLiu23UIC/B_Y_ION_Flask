from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter, Label
import pandas as pd
from protein_calculate import *
from scipy.stats import multinomial


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


def isotope_weight(peptide:str) -> float:
    atom_counts = sum(protein_index(peptide).values())


def isotope_visualize(b_frag:list, y_frag:list, isotope_dict:dict):
    """

    :param b_frag:
    :param y_frag:
    :param isotope_dict:
    :return:
    """
    b_frag =



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