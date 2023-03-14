"""
This module provides tools for cleaning datas and calibration process of the sensor
"""


from typing import Type


def clean_none(var, var_with_none):
    """
    When you have var_with_none : list with None data and var : list full and the two lists have the same size, you can "clean" None with this function
    """
    if not (isinstance(var, list) or isinstance(var_with_none, list)):
        raise TypeError("var or var_with_none is not a list")
    if len(var) != len(var_with_none):
        raise IndexError("var and var_with_none does not have the same length")

    var_cleaned = [i for i,j in zip(var, var_with_none) if j is not None]
    var_with_none_cleaned = [j for j in var_with_none if j is not None ]
    
    return (var_cleaned,var_with_none_cleaned) 


import plotly.graph_objects as px
from plotly.subplots import make_subplots

import plotly.express as pxp
import numpy as np



def make_calibration_plot(input_var, output_var_calib, output_var_true, error):
    """
    This function compute a graph with :
    - input_var in absciss (Ex : mesurande)
    - output_var_calib: output expermental value of complete sensor (after cpu)
    - output_var_true: "true value" of input
    - error: error between true and experimental output value

    Output : fig. It means you have to do f = make_calibration_plot(error) then f.show()
    """
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        px.Scatter(x = input_var, y= output_var_calib, mode='markers', name = 'measure'), 
        secondary_y=False
        )
    fig1.add_trace(
        
        px.Scatter(x = input_var, y = output_var_true, mode='markers', name = 'true'),
        secondary_y=False,
        )

    fig1.add_trace(
        px.Scatter(x = input_var, y = error, mode='markers', name = 'error'),
        secondary_y=True
        )

    fig1.update_yaxes(title_text="Sortie", secondary_y=False)
    fig1.update_yaxes(title_text="Erreur", secondary_y=True)
    fig1.update_xaxes(title_text="Entrée")
    
    return fig1


def make_histogram(error):
    """
    Plot an histogram of errors. 
    Input : Error has to be a list of errors.
    Output : fig. It means you have to do f = make_histogram(error) then f.show()
    """
    # Compute frequency and bins
    error_for_histo = []
    for e in error:
        if e is not None:
            error_for_histo.append(e)
        

    frequency, bins = np.histogram(error_for_histo, bins=20, range=[-100, 100])



    fig = pxp.histogram( x=error_for_histo,
                    marginal="box" # or violin, rug
                    )

    return fig

def compute_error(experimental, true_value):
    error = [x-y for x,y in zip(experimental, true_value)]
    return error





