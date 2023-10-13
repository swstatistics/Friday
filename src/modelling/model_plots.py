import pandas as pd
import numpy as np


import matplotlib.pyplot as plt
import matplotlib
import matplotlib.pylab as pylab


from src.modelling.model_functions import sigmoid, get_plot_data


# colors
exp_green = '#BFCCC3' 
line_orange = '#B59C65'
line_gray = '#666666'
line_blue = '#657AB5'

font = {'family' : 'DejaVu Sans','weight' : 'normal','size' : 10}
params = {'legend.fontsize': 'x-large', 'figure.figsize': (15, 5),'axes.labelsize': 'x-large', 'axes.titlesize':'x-large'}
matplotlib.rc('font', **font)
pylab.rcParams.update(params)


def get_best_limits(a:tuple, b:tuple)-> tuple:
    """
        determines the optimal ylim for the shared yaxis
    """
    if a[0] <= b[0]:
        minimum = a[0]
    else:
        minimum = b[0] 

    if a[1] > b[1]:
        maximum = a[1]
    else:
        maximum = b[1] 

    return (minimum, maximum)
    
def plot_model_field(erg, field_list, on_test_data=False):
    """
        generates a plot for all features in the fieldlist. 
        Depending on the on_test_data, the testdata or the trainingdata will be plotted.
        This could be improved with en ENUM, so the complete Dataset could be plotted as well. 
    """


    number_fields = len(field_list)

    fig, ax = plt.subplots(number_fields, 1, figsize=(25,7*number_fields))

    for i in range(number_fields):

        field_name = field_list[i]

        curr_ax = ax[i]

        
        plot_df_grp = get_plot_data(erg, field_name, on_test_data)
        
    
        twin1 = curr_ax.twinx()
        twin2 = curr_ax.twinx()
        twin3 = curr_ax.twinx()

        twin2.spines.right.set_position(("axes", 1.05))
        twin3.spines.right.set_position(("axes", 1.1))

        # plot Exposure and 
        curr_ax.bar(data = plot_df_grp, x=field_name , height='Exposure' , color=exp_green)
        curr_ax.set_xlabel(field_name)

        # plot observed values
        twin1.plot(plot_df_grp[field_name], plot_df_grp['payment_fault'], color=line_gray, linewidth=2)

        #plot predicted_values
        twin2.plot(plot_df_grp[field_name], plot_df_grp['predicted'], color=line_orange, linewidth=2)

        # plot the factors
        twin3.plot(plot_df_grp[field_name], plot_df_grp['coef'], color=line_blue, linewidth=1.5)




        # Labeling
        matplotlib.rc('font', weight='bold')
        curr_ax.set(ylabel='Exposure')
        curr_ax.yaxis.label.set_color(exp_green)


        # ylimits 
        best_ylim = get_best_limits(twin1.get_ylim(), twin2.get_ylim())

        twin1.set(ylabel='observed', ylim = best_ylim)
        twin1.yaxis.label.set_color(line_gray)

        twin2.set(ylabel='predicted', ylim = best_ylim)
        twin2.yaxis.label.set_color(line_orange)

        twin3.set(ylabel='factors')
        twin3.yaxis.label.set_color(line_blue)

        matplotlib.rc('font', weight='normal')

        #set labels 
        plt.xticks(plot_df_grp[field_name])

    plt.show()





