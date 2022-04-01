#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 09:52:30 2022

@author: dadsensor
"""
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

from Mechanical_model_function import *

# define standard geometry values
h_column=2400; # height  of the column
d_column=600; # depth of the column
d_beam=380; # depth of the top beam
H=h_column+d_beam*0.5; # distance form the horizontal force to the bottom beam
E_w=7800; # Elastic modulus in MPa
G_w=142; # shear modulus
A_w=290736*2/3; # Shear area
I_w=7.56945684e+11;
d_gap=0; # gap opening

# import experimental data-
headers=['SW_noLoad_d1','SW_noLoad_F1','SW_noLoad_d2','SW_noLoad_F2','SW_Load_d','SW_Load_F','WW_noLoad_d','WW_noLoad_F','WW_Load_d','WW_Load_F']
exp_data=pd.read_excel("Data_resume.xlsx",skiprows=(1),usecols=range(1,11),names=headers,sheet_name='fD');

headers_2=['SW_noLoad_d','SW_noLoad_dvert','SW_Load_d','SW_Load_dvert','WW_noLoad_d','WW_noLoad_dvert','WW_Load_d','WW_Load_dvert'];
exp_data_dic=pd.read_excel("Data_resume.xlsx",skiprows=(2),names=headers_2,sheet_name='v_d');

# Start the GUI

root = Tk();
root.title("WikiHouse walls")
root.geometry("900x400")

column_labels_list=[]; # list with all the labels name
column_values_list=[]; # list with all the values name
vload_values_list=[]; # list with the vertical load by column
peg_values_list=[]; # list with all the values name
peg_failure_list=[]; # list with all the values name

# -------------------------COLUMNS------------------------------
# create the labels and entries for the columns
for i in range(8):
    column_labels_list.append(Label(root,text="column "+str(i+1), padx=25)); # column label
    column_values_list.append(Entry(root,width=5)); # column value
    vload_values_list.append(Entry(root,width=5)); # value of vertical load by column
    peg_values_list.append(Entry(root,width=5)); # value fo the pegs stiffness
    peg_failure_list.append(Entry(root,width=5)); # value fo the pegs stiffness

# place the  column labels in the window
for i,(label,value,vload,pegK,pegF) in enumerate(zip(column_labels_list,column_values_list,vload_values_list,peg_values_list,peg_failure_list)):
    label.grid(row=i+1,column=0); # place the label of the column
    value.grid(row=i+1,column=1); # place the entry for the column
    value.insert(0,"S"); # pre-insert a vaue for the column
    vload.grid(row=i+1,column=2); # place the entry for the vertical Load
    vload.insert(0,0); # pre-insert a value for the vertical load
    pegK.grid(row=i+1,column=3); # place the entry for the peg stiffness
    pegK.insert(0,6.9); # place the peg stiffness
    pegF.grid(row=i+1,column=4); # place the entry for the peg stiffness
    pegF.insert(0,14); # place the peg failure load


# create the vertical load label and entry
label_padx=10;
column_type_label=Label(root,text="S,W,D",padx=label_padx)
v_load_label=Label(root,text="Load (kN)",padx=label_padx)
peg_label=Label(root,text="k_u (kN/mm)",padx=label_padx)
pegF_label=Label(root,text="F_u_max (kN)",padx=label_padx)
shearkey_label=Label(root,text="k_s (kN/mm)",padx=label_padx)
shearkeyF_label=Label(root,text="F_s_max (kN)",padx=label_padx)
column_type_label.grid(row=0,column=1)
v_load_label.grid(row=0,column=2);
peg_label.grid(row=0,column=3);
pegF_label.grid(row=0,column=4);
shearkey_label.grid(row=0,column=6);
shearkeyF_label.grid(row=0,column=7);

#--------------------------SHEAR keys-----------------------------------
shear_labels_list=[]; # list with the shear stiffness labels
shear_values_list=[]; # list with the shear stiffness values
shear_failure_list=[]; # list with the shear failure values
for i in range(7):
    shear_labels_list.append(Label(root,text="interface "+str(i+1)+"-"+str(i+2), padx=25)); # shear label
    shear_values_list.append(Entry(root,width=5)); # column value
    shear_failure_list.append(Entry(root,width=5)); # column value
for i,(label,value,failure) in enumerate(zip(shear_labels_list,shear_values_list,shear_failure_list)):
    label.grid(row=i+1,column=5); # place the label of the shear connection
    value.grid(row=i+1,column=6); # place the entry for the shear connection
    value.insert(0,17.7); # pre-insert a vaue for the shear connection
    failure.grid(row=i+1,column=7); # place the entry for the shear connection
    failure.insert(0,39); # pre-insert a vaue for the shear connection

#-------------------------CALIBRATION coefficients--------------------------------------------
calibration_label=Label(root,text="calibration coeff",padx=25); # calibration label
calibration_value=Entry(root,width=5); # calibration value
calibration_label.grid(row=8,column=5); # place the label
calibration_value.grid(row=8,column=6); # Place the entry
calibration_value.insert(0,1); # place a number different from 0

#----------------------EXPERIMENTAL Results---------------------------------------------


#create a function that updates the geomtery
def main_geometry(column_values_list,vload_values_list,shear_values_list,peg_values_list,h_column,d_column,d_beam):
    L_wall=len(column_values_list)*d_column; # length of the wall
    plt.close('all')

    fig,ax = plt.subplots(figsize=(10, 7.5))
    rect_patches=[]; # define the empty list
    # loop over the values and create the rectangular patches for plot
    for i,value in enumerate(column_values_list):
        if str(value.get())=="S":
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), d_column, h_column, linewidth=1, edgecolor='k', facecolor='none'))
        elif str(value.get())=="W":
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), d_column, h_column/2, linewidth=1, edgecolor='k', facecolor='none'))
        elif str(value.get())=="D":
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), 0, 0, linewidth=1, edgecolor='k', facecolor='none'))
        else:
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), d_column, h_column, linewidth=1, edgecolor='k', facecolor='none'))
            display("choose S, W or W")
        if i==len(column_values_list)-1:
            rect_patches.append(patches.Rectangle((0, h_column), (i+1)*d_column, d_beam, linewidth=1, edgecolor='k', facecolor='none'))

    for patch in rect_patches:
        ax.add_patch(patch); # add the column patches ot the image.

    # loop over the vertical load values
    for i,F in enumerate(vload_values_list):
        arrowsize=600; # arrow value
        x_arrow=(i+1)*d_column-0.5*d_column; # x coordinate of the arrow size
        if float(F.get())!=0:
            if str(column_values_list[i].get())=="D" or str(column_values_list[i].get())=="W":
                ax.arrow(x_arrow,h_column+d_beam,0,-arrowsize,color='r',width=1,head_width=50); # add the arrow
                ax.text(x_arrow,h_column+d_beam+150,str(F.get())+" kN",color='r');
            else:
                ax.arrow(x_arrow,h_column+d_beam,0,-arrowsize,color='b',width=1,head_width=50); # add the arrow
                ax.text(x_arrow,h_column+d_beam+150,str(F.get())+" kN",color='b');

    # loop over the sher stiffness values
    shear_interface_width=4;
    for i,k_s in enumerate(shear_values_list):
            if float(k_s.get())!=0:
                if str(column_values_list[i].get())=="D" or str(column_values_list[i+1].get())=="D":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,h_column],'r',linewidth=shear_interface_width)

                elif str(column_values_list[i].get())=="S" and str(column_values_list[i+1].get())=="S":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,h_column],'g',linewidth=shear_interface_width)
                    ax.text(i*d_column+d_column+50,0.4*h_column,str(k_s.get())+" kN/mm",color='g',fontsize='small',rotation='vertical');
                elif str(column_values_list[i].get())=="W" or str(column_values_list[i+1].get())=="W":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,0.5*h_column],'g',linewidth=shear_interface_width)
                    ax.text(i*d_column+d_column+50,0.2*h_column,str(k_s.get())+" kN/mm",color='g',fontsize='small',rotation='vertical');
                else :
                    display("Error")
    uplift_interface_width=4;
    for i,k_u in enumerate(peg_values_list):
        if float(k_u.get())!=0:
            if str(column_values_list[i].get())=="D":
                ax.plot([i*d_column,i*d_column+d_column],[0,0],'r',linewidth=uplift_interface_width)
                ax.text(i*d_column,-200,str(k_u.get())+" kN/mm",color='r',fontsize='small');
            else:
                ax.plot([i*d_column,i*d_column+d_column],[0,0],'g',linewidth=uplift_interface_width)
                ax.text(i*d_column,-200,str(k_u.get())+" kN/mm",color='g',fontsize='small');


    # lateral force and displacement
    ax.arrow(-arrowsize-50,h_column+0.5*d_beam,arrowsize,0,color='b',width=1,head_width=50); # add the arrow
    ax.text(-2*arrowsize/3,h_column+0.5*d_beam+50,r"$F_h$",color='b',fontsize='medium');

    ax.arrow(L_wall,h_column+0.5*d_beam,arrowsize*0.3,0,color='b',width=1,head_width=50); # add the arrow
    ax.text(L_wall+arrowsize*0.05,h_column+0.5*d_beam+50,r"$d_h$",color='b',fontsize='medium');

    ax.set_xlim(-d_beam*3,len(column_values_list)*d_column+d_column);
    ax.set_ylim(-d_beam,h_column+2*d_beam)
    #ax.arrow(0,)
    fig.show()

def get_values_calculate_plot(d_column,H,E_w,G_w,A_w,I_w,d_gap):
    k_u_list=[]; # list of uplifing forces
    k_s_list=[]; # shear stiffness of the connectors
    F_v_list=[]; # vertical load list
    f_fail_list=[]; # failing load of the pegs
    f_failshear_list=[]; # failing load of the shear connectors
    calibration_factors=[]; # calibration factors
    calibration_factors.append(float(calibration_value.get()));
    calibration_factors.append(float(calibration_value.get()));

    for k_u,F_v,f_fail in zip(peg_values_list,vload_values_list,peg_failure_list):
        k_u_list.append(float(k_u.get())); # get and append the values
        F_v_list.append(float(F_v.get())); # get and append the values
        f_fail_list.append(float(f_fail.get())); # get and append the values

    for k_s,f_shear in zip(shear_values_list,shear_failure_list):
        k_s_list.append(float(k_s.get())); # get and append the values
        f_failshear_list.append(float(f_shear.get())); # get and append the values

    d_h,f_h,L_list,d_v,f_peg,f_shear,i_fp_min,i_peg_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_pegs,i_failure_shear=calculate_and_plot_walls(calibration_factors,k_u_list[::-1],k_s_list[::-1],F_v_list[::-1],d_column,H,E_w,G_w,A_w,I_w,d_gap,f_fail_list[::-1],f_failshear_list[::-1]);

    plt.close('all')
    fig,ax=plt.subplots(2,2,figsize=(10, 7.5))
    if SW_noLoad_var.get()==1:
        ax[0,0].plot(exp_data["SW_noLoad_d1"],exp_data["SW_noLoad_F1"],'tab:blue',label="SW_noLoad exp")
        ax[0,0].plot(exp_data["SW_noLoad_d2"],exp_data["SW_noLoad_F2"],'tab:blue')

    if SW_Load_var.get()==1:
        ax[0,0].plot(exp_data["SW_Load_d"],exp_data["SW_Load_F"],'tab:pink',label="SW_Load exp")

    if WW_noLoad_var.get()==1:
            ax[0,0].plot(exp_data["WW_noLoad_d"],exp_data["WW_noLoad_F"],'tab:cyan',label="WW_noLoad exp")

    if WW_Load_var.get()==1:
        ax[0,0].plot(exp_data["WW_Load_d"],exp_data["WW_Load_F"],'tab:red',label="WW_Load exp")


    ax[0,0].plot(d_h,f_h,'k--',label='model calibrated')
    ax[0,0].plot(d_h[i_fp_min],f_h[i_fp_min],'rx',label='peg '+i_peg_failing_swap)
    ax[0,0].plot(d_h[i_fshear_min],f_h[i_fshear_min],'ro',label='shear conn '+ i_shear_failing_swap)
    ax[0,0].set_xlabel(r'$d_h$ (mm)')
    ax[0,0].set_ylabel('$F_h$ (kN)')
    ax[0,0].legend(loc='lower right')
    # ax.set_xlim([0,90])
    # ax.set_ylim([0,90])
    ax[0,0].grid()
    # fig.show()

    f_pegTra=np.array(f_peg).transpose(); # tranpose the matrix
    # fig,axes=plt.subplots(2,4,figsize=(10, 6))
    colors=['tab:blue','tab:orange','tab:pink','tab:brown','tab:cyan','tab:olive','tab:purple','tab:red'];
    for i,(f_p,c,i_fp) in enumerate(zip(f_pegTra,colors,i_failure_pegs)):
        ax[0,1].plot(d_h[0:i_fp],f_p[0:i_fp],label="peg "+peg_swapping(i),color=c)
        if i_fp < len(d_h)-1:
            ax[0,1].plot(d_h[i_fp],f_p[i_fp],'x',color=c); # plot the failure with x

    ax[0,1].set_xlabel(r'$d_h$ (mm)')
    ax[0,1].set_ylabel(r'$F_{peg}$ (kN)')
    ax[0,1].legend(loc='upper left')
    ax[0,1].grid()

    f_shearTra=np.array(f_shear).transpose(); # transpose the matrix
    for i,(f_s,c,i_fs) in enumerate(zip(f_shearTra,colors,i_failure_shear)):
        ax[1,0].plot(d_h[0:i_fs],f_p[0:i_fs],label="shear conn "+shearconnector_swapping(i),color=c)
        if i_fs < len(d_h)-1:
            ax[1,0].plot(d_h[i_fs],f_p[i_fs],'o',color=c); # plot the failure with x

    ax[1,0].set_xlabel(r'$d_h$ (mm)')
    ax[1,0].set_ylabel(r'$F_{shear}$ (kN)')
    ax[1,0].legend(loc='upper left')
    ax[1,0].grid()

    d_v_peg=d_v[i_fp_min]; # vertical displacement where the peg fails
    d_v_shear=d_v[i_fshear_min]; # vertical displacement where the shear connector fails
    ax[1,1].plot(L_list[::-1],d_v_peg,'kx--',markeredgecolor='r',label='peg failure')
    ax[1,1].plot(L_list[::-1],d_v_shear,'ko--',markeredgecolor='r',label='peg failure')
    ax[1,1].set_ylabel(r'$d_v$ (mm)')
    ax[1,1].set_xlabel(r'$L_{wall}$ (mm)')
    ax[1,1].legend(loc='upper left')
    ax[1,1].grid()

    # ax.set_ylim([0,90])
    fig.tight_layout()
    fig.show()

# create function to plot the experimental results
def SW_noLoad_experimental():
    for col,F_v,k_u,peg_F in zip(column_values_list,vload_values_list,peg_values_list,peg_failure_list):
        col.delete(0,END);
        F_v.delete(0,END);
        k_u.delete(0,END);
        peg_F.delete(0,END);

        col.insert(0,"S"); # insert experimental values
        F_v.insert(0,0.5); # insert experimental values
        k_u.insert(0,6.9); # insert experimental values
        peg_F.insert(0,14); # insert experimental values
    for k_s,f_shear in zip(shear_values_list,shear_failure_list):
        k_s.delete(0,END);
        f_shear.delete(0,END);
        k_s.insert(0,17.7); # insert he experimental values
        f_shear.insert(0,39); # insert the experimental values
    calibration_value.delete(0,END); # insert the experimental values
    calibration_value.insert(0,0.3); # insert the experimental values
    return

def SW_Load_experimental():
    for col,F_v,k_u,peg_F in zip(column_values_list,vload_values_list,peg_values_list,peg_failure_list):
        col.delete(0,END);
        F_v.delete(0,END);
        k_u.delete(0,END);
        peg_F.delete(0,END);

        col.insert(0,"S"); # insert experimental values
        F_v.insert(0,6.1); # insert experimental values
        k_u.insert(0,6.9); # insert experimental values
        peg_F.insert(0,14); # insert experimental values
    for k_s,f_shear in zip(shear_values_list,shear_failure_list):
        k_s.delete(0,END);
        f_shear.delete(0,END);
        k_s.insert(0,17.7); # insert he experimental values
        f_shear.insert(0,39.3); # insert the experimental values
    calibration_value.delete(0,END); # insert the experimental values
    calibration_value.insert(0,0.45); # insert the experimental values
    return

def WW_noLoad_experimental():
    for col,F_v,k_u,peg_F in zip(column_values_list,vload_values_list,peg_values_list,peg_failure_list):
        col.delete(0,END);
        F_v.delete(0,END);
        k_u.delete(0,END);
        peg_F.delete(0,END);
        k_u.insert(0,6.9); # insert experimental values
        peg_F.insert(0,14); # insert experimental values


    column_values_list[0].insert(0,"S"); # insert experimental values
    column_values_list[1].insert(0,"W"); # insert experimental values
    column_values_list[2].insert(0,"W"); # insert experimental values
    column_values_list[3].insert(0,"S"); # insert experimental values
    column_values_list[4].insert(0,"S"); # insert experimental values
    column_values_list[5].insert(0,"W"); # insert experimental values
    column_values_list[6].insert(0,"W"); # insert experimental values
    column_values_list[7].insert(0,"S"); # insert experimental values

    vload_values_list[0].insert(0,0.5); # insert experimental values
    vload_values_list[1].insert(0,0.25); # insert experimental values
    vload_values_list[2].insert(0,0.25); # insert experimental values
    vload_values_list[3].insert(0,0.5); # insert experimental values
    vload_values_list[4].insert(0,0.5); # insert experimental values
    vload_values_list[5].insert(0,0.25); # insert experimental values
    vload_values_list[6].insert(0,0.25); # insert experimental values
    vload_values_list[7].insert(0,0.5); # insert experimental values

    for k_s,f_shear in zip(shear_values_list,shear_failure_list):
        k_s.delete(0,END);
        f_shear.delete(0,END);

    shear_values_list[0].insert(0,5.9); # insert he experimental values
    shear_values_list[1].insert(0,5.9); # insert he experimental values
    shear_values_list[2].insert(0,5.9); # insert he experimental values
    shear_values_list[3].insert(0,17.7); # insert he experimental values
    shear_values_list[4].insert(0,5.9); # insert he experimental values
    shear_values_list[5].insert(0,5.9); # insert he experimental values
    shear_values_list[6].insert(0,5.9); # insert he experimental values


    shear_failure_list[0].insert(0,13.1); # insert the experimental values
    shear_failure_list[1].insert(0,13.1); # insert the experimental values
    shear_failure_list[2].insert(0,13.1); # insert the experimental values
    shear_failure_list[3].insert(0,39.3); # insert the experimental values
    shear_failure_list[4].insert(0,13.1); # insert the experimental values
    shear_failure_list[5].insert(0,13.1); # insert the experimental values
    shear_failure_list[6].insert(0,13.1); # insert the experimental values


    calibration_value.delete(0,END); # insert the experimental values
    calibration_value.insert(0,0.25); # insert the experimental values
    return

def WW_Load_experimental():
    for col,F_v,k_u,peg_F in zip(column_values_list,vload_values_list,peg_values_list,peg_failure_list):
        col.delete(0,END);
        F_v.delete(0,END);
        k_u.delete(0,END);
        peg_F.delete(0,END);
        k_u.insert(0,6.9); # insert experimental values
        peg_F.insert(0,14); # insert experimental values


    column_values_list[0].insert(0,"S"); # insert experimental values
    column_values_list[1].insert(0,"W"); # insert experimental values
    column_values_list[2].insert(0,"W"); # insert experimental values
    column_values_list[3].insert(0,"S"); # insert experimental values
    column_values_list[4].insert(0,"S"); # insert experimental values
    column_values_list[5].insert(0,"W"); # insert experimental values
    column_values_list[6].insert(0,"W"); # insert experimental values
    column_values_list[7].insert(0,"S"); # insert experimental values

    vload_values_list[0].insert(0,11.7); # insert experimental values
    vload_values_list[1].insert(0,0.25); # insert experimental values
    vload_values_list[2].insert(0,0.25); # insert experimental values
    vload_values_list[3].insert(0,11.7); # insert experimental values
    vload_values_list[4].insert(0,11.7); # insert experimental values
    vload_values_list[5].insert(0,0.25); # insert experimental values
    vload_values_list[6].insert(0,0.25); # insert experimental values
    vload_values_list[7].insert(0,11.7); # insert experimental values

    for k_s,f_shear in zip(shear_values_list,shear_failure_list):
        k_s.delete(0,END);
        f_shear.delete(0,END);

    shear_values_list[0].insert(0,5.9); # insert he experimental values
    shear_values_list[1].insert(0,5.9); # insert he experimental values
    shear_values_list[2].insert(0,5.9); # insert he experimental values
    shear_values_list[3].insert(0,17.7); # insert he experimental values
    shear_values_list[4].insert(0,5.9); # insert he experimental values
    shear_values_list[5].insert(0,5.9); # insert he experimental values
    shear_values_list[6].insert(0,5.9); # insert he experimental values


    shear_failure_list[0].insert(0,13.1); # insert the experimental values
    shear_failure_list[1].insert(0,13.1); # insert the experimental values
    shear_failure_list[2].insert(0,13.1); # insert the experimental values
    shear_failure_list[3].insert(0,39.3); # insert the experimental values
    shear_failure_list[4].insert(0,13.1); # insert the experimental values
    shear_failure_list[5].insert(0,13.1); # insert the experimental values
    shear_failure_list[6].insert(0,13.1); # insert the experimental values


    calibration_value.delete(0,END); # insert the experimental values
    calibration_value.insert(0,0.5); # insert the experimental values
    return
# -------------------------------------create the BUTTONS for the presets-------------------------------
SW_noLoad_button=Button(root,text="SW_noLoad",command=SW_noLoad_experimental);
SW_noLoad_var=IntVar();
SW_noLoad_check=Checkbutton(root, text = "Plot exp data",variable=SW_noLoad_var);
SW_noLoad_button.grid(row=20,column=0,columnspan=2)
SW_noLoad_check.grid(row=20,column=2)

SW_Load_button=Button(root,text="SW_Load",command=SW_Load_experimental);
SW_Load_var=IntVar();
SW_Load_check=Checkbutton(root, text = "Plot exp data",variable=SW_Load_var);
SW_Load_button.grid(row=21,column=0,columnspan=2)
SW_Load_check.grid(row=21,column=2)

WW_noLoad_button=Button(root,text="WW_noLoad",command=WW_noLoad_experimental)
WW_noLoad_var=IntVar();
WW_noLoad_check=Checkbutton(root, text = "Plot exp data",variable=WW_noLoad_var);
WW_noLoad_button.grid(row=22,column=0,columnspan=2)
WW_noLoad_check.grid(row=22,column=2)

WW_Load_button=Button(root,text="WW_Load",command=WW_Load_experimental)
WW_Load_var=IntVar();
WW_Load_check=Checkbutton(root, text = "Plot exp data",variable=WW_Load_var);
WW_Load_button.grid(row=23,column=0,columnspan=2)
WW_Load_check.grid(row=23,column=2)


#-----------------------------------------Calculation and visualization buttons----------------------------
button_view_geometry=Button(root,text="View geometry",command=lambda: main_geometry(column_values_list,vload_values_list,shear_values_list,peg_values_list,h_column,d_column,d_beam))
button_view_geometry.grid(row=20,column=6,columnspan=2,rowspan=2)

button_calculation=Button(root,text="Calculate",command=lambda: get_values_calculate_plot(d_column,H,E_w,G_w,A_w,I_w,d_gap))
button_calculation.grid(row=22,column=6,columnspan=2,rowspan=2)
root.mainloop()
