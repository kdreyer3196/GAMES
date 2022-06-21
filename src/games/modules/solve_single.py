#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 15:25:47 2022

@author: kate
"""
import os
from typing import Tuple
import numpy as np
from games.models.set_model import model
from games.utilities.saving import create_folder
from games.utilities.metrics import calc_chi_sq, calc_r_sq
from games.plots.plots_training_data import plot_training_data
from games.plots.plots_timecourses import plot_timecourses
from games.config.settings import settings, folder_path
from games.config.experimental_data import ExperimentalData


def solve_single_parameter_set() -> Tuple[list, float, float]:
    """
    Solves model for a single parameter set

    Parameters
    ----------
    None

    Returns
    -------
    solutions_norm
        a list of floats containing the normalized simulation values corresponding to the dataID defined in Settings

    chi_sq
        a float defining the value of the cost function

    r_sq
        a float defining the value of the correlation coefficient (r_sq)
    """

    if settings["modelID"] == "synTF_chem":
        if settings["dataID"] == "ligand dose response":
            solutions = model.solve_ligand_sweep(ExperimentalData.x)

    elif settings["modelID"] == "synTF":
        if settings["dataID"] == "synTF dose response":
            solutions = model.solve_synTF_sweep(ExperimentalData.x)

    solutions_norm = [i / max(solutions) for i in solutions]
    chi_sq = calc_chi_sq(ExperimentalData.exp_data, solutions_norm, ExperimentalData.exp_error)
    r_sq = calc_r_sq(ExperimentalData.exp_data, solutions_norm)

    return solutions_norm, chi_sq, r_sq


def run_single_parameter_set() -> Tuple[list, float, float]:
    """Solves model for a single parameter set using dataID defined in settings["

    Parameters
    ----------
    None

    Returns
    -------
    solutions_norm
        a list of floats containing the normalized simulation values corresponding to the dataID defined in Settings

    chi_sq
        a float defining the value of the cost function

    r_sq
        a float defining the value of the correlation coefficient (r_sq)

    """
    sub_folder_name = "TEST SINGLE PARAMETER SET"
    path = create_folder(folder_path, sub_folder_name)
    os.chdir(path)
    model.parameters = settings["parameters"]
    solutions_norm, chi_sq, r_sq = solve_single_parameter_set()
    filename = "FIT TO TRAINING DATA"
    plot_timecourses()
    plot_training_data(
        ExperimentalData.x,
        solutions_norm,
        ExperimentalData.exp_data,
        ExperimentalData.exp_error,
        filename,
    )

    print("")
    print("*************************")
    print("Parameters")
    for i, label in enumerate(settings["parameter_labels"]):
        print(label + " = " + str(model.parameters[i]))
    print("")
    print("Metrics")
    print("R_sq = " + str(np.round(r_sq, 4)))
    print("chi_sq = " + str(np.round(chi_sq, 4)))
    print("*************************")
    print("")

    return solutions_norm, chi_sq, r_sq
