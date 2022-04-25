#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:48:51 2022

@author: dadsensor
"""

# Import libraries
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Walls_app_functions import *

# Intial variables
h_column=2400; # height  of the column
d_column=600; # depth of the column
d_column_corner=318;
d_beam=380; # depth of the top beam
H=h_column+d_beam*0.5; # distance form the horizontal force to the bottom beam



with st.container():
    st.title("Skylark walls - Web app")
    st.header("What is it?")
    st.write("A web based app to calculate the lateral force vs displacement response of Skylark walls.")
    st.write(" The details of the undelining mechanical model can be found here https://doi.org/10.31224/2266.")
    st.write("Choose one of the tested configurations or manually configure the wall.")

with st.container():
    st.header("Manual configuration")
    # with st.expander("Columns geometry:"):
    col_1,col_2,col_3,col_4,col_5,col_6,col_7,col_8=st.columns(8); # divide the space into columns

    col_1_value=col_1.selectbox("C1 type",options=["S","D","W"],index=0,key="col_1_key"); # columns geomtery
    col_2_value=col_2.selectbox("C2 type",options=["S","D","W"],index=0,key="col_2_key"); # columns geomtery
    col_3_value=col_3.selectbox("C3 type",options=["S","D","W"],index=0,key="col_3_key"); # columns geomtery
    col_4_value=col_4.selectbox("C4 type",options=["S","D","W"],index=0,key="col_4_key"); # columns geomtery
    col_5_value=col_5.selectbox("C5 type",options=["S","D","W"],index=0,key="col_5_key"); # columns geomtery
    col_6_value=col_6.selectbox("C6 type",options=["S","D","W"],index=0,key="col_6_key"); # columns geomtery
    col_7_value=col_7.selectbox("C7 type",options=["S","D","W"],index=0,key="col_7_key"); # columns geomtery
    col_8_value=col_8.selectbox("C8 type",options=["S","D","W"],index=0,key="col_8_key"); # columns geomtery
    column_keys_list=["col_1_key","col_2_key","col_3_key","col_4_key","col_5_key","col_6_key","col_7_key","col_8_key"]; # column keys

    # update the column values
    def update_column_values(column_keys_list):
        column_values_list=[];
        for key in column_keys_list:
            column_values_list.append(st.session_state[key]); # append values into a list
        return column_values_list

    column_values_list=update_column_values(column_keys_list);


    if 'vload_expander_state' not in st.session_state:
        st.session_state['vload_expander_state'] = False;
    expander_vertical_load=st.expander("Vertical load:",expanded=st.session_state['vload_expander_state'])
    with expander_vertical_load:

        vl_1,vl_2,vl_3,vl_4=st.columns(4); # divide the space into columns
        vl_5,vl_6,vl_7,vl_8=st.columns(4); # divide the space into columns

        vl_1_value=vl_1.number_input("V1 (kN)",value=1.,key="vl_1_key"); # column's vertical load
        vl_2_value=vl_2.number_input("V2 (kN)",value=1.,key="vl_2_key"); # column's vertical load
        vl_3_value=vl_3.number_input("V3 (kN)",value=1.,key="vl_3_key"); # column's vertical load
        vl_4_value=vl_4.number_input("V4 (kN)",value=1.,key="vl_4_key"); # column's vertical load
        vl_5_value=vl_5.number_input("V5 (kN)",value=1.,key="vl_5_key"); # column's vertical load
        vl_6_value=vl_6.number_input("V6 (kN)",value=1.,key="vl_6_key"); # column's vertical load
        vl_7_value=vl_7.number_input("V7 (kN)",value=1.,key="vl_7_key"); # column's vertical load
        vl_8_value=vl_8.number_input("V8 (kN)",value=1.,key="vl_8_key"); # column's vertical load
        vload_keys_list=["vl_1_key","vl_2_key","vl_3_key","vl_4_key","vl_5_key","vl_6_key","vl_7_key","vl_8_key"]; # append values into a list

        # update the veritcal load values
        def update_vload_values(vload_keys_list):
            vload_values_list=[];
            for key in vload_keys_list:
                vload_values_list.append(st.session_state[key]); # append values into a list
            return vload_values_list

        vload_values_list=update_vload_values(vload_keys_list);

    with st.expander("Hold down connectors:"):
        st.write('Stiffness (kN/m)')
        hd_1k,hd_2k,hd_3k,hd_4k=st.columns(4); # divide the space into columns
        hd_5k,hd_6k,hd_7k,hd_8k=st.columns(4); # divide the space into columns

        st.text('')
        st.text('')

        st.write('Capacity (kN)')
        hd_1c,hd_2c,hd_3c,hd_4c=st.columns(4); # divide the space into columns
        hd_5c,hd_6c,hd_7c,hd_8c=st.columns(4); # divide the space into columns

        hd_1k_value=hd_1k.number_input("k_hd1 (kN/m)",value=1.,key="hd_1k_key"); # column's hold down connector
        hd_2k_value=hd_2k.number_input("k_hd2 (kN/m)",value=1.,key="hd_2k_key"); # column's hold down connector
        hd_3k_value=hd_3k.number_input("k_hd3 (kN/m)",value=1.,key="hd_3k_key"); # column's hold down connector
        hd_4k_value=hd_4k.number_input("k_hd4 (kN/m)",value=1.,key="hd_4k_key"); # column's hold down connector
        hd_5k_value=hd_5k.number_input("k_hd5 (kN/m)",value=1.,key="hd_5k_key"); # column's hold down connector
        hd_6k_value=hd_6k.number_input("k_hd6 (kN/m)",value=1.,key="hd_6k_key"); # column's hold down connector
        hd_7k_value=hd_7k.number_input("k_hd7 (kN/m)",value=1.,key="hd_7k_key"); # column's hold down connector
        hd_8k_value=hd_8k.number_input("k_hd8 (kN/m)",value=1.,key="hd_8k_key"); # column's hold down connector
        hd_k_keys_list=["hd_1k_key","hd_2k_key","hd_3k_key","hd_4k_key","hd_5k_key","hd_6k_key","hd_7k_key","hd_8k_key"]; # append values into a list

        def update_hdk_values(hd_k_keys_list):
            hd_k_values_list=[];
            for key in hd_k_keys_list:
                hd_k_values_list.append(st.session_state[key]); # append values into a list
            return hd_k_values_list

        hd_k_values_list=update_hdk_values(hd_k_keys_list);

        hd_1c_value=hd_1c.number_input("C_hd1 (kN)",value=1.,key="hd_1c_key"); # column's hold down connector
        hd_2c_value=hd_2c.number_input("C_hd2 (kN)",value=1.,key="hd_2c_key"); # column's hold down connector
        hd_3c_value=hd_3c.number_input("C_hd3 (kN)",value=1.,key="hd_3c_key"); # column's hold down connector
        hd_4c_value=hd_4c.number_input("C_hd4 (kN)",value=1.,key="hd_4c_key"); # column's hold down connector
        hd_5c_value=hd_5c.number_input("C_hd5 (kN)",value=1.,key="hd_5c_key"); # column's hold down connector
        hd_6c_value=hd_6c.number_input("C_hd6 (kN)",value=1.,key="hd_6c_key"); # column's hold down connector
        hd_7c_value=hd_7c.number_input("C_hd7 (kN)",value=1.,key="hd_7c_key"); # column's hold down connector
        hd_8c_value=hd_8c.number_input("C_hd8 (kN)",value=1.,key="hd_8c_key"); # column's hold down connector
        hd_c_keys_list=["hd_1c_key","hd_2c_key","hd_3c_key","hd_4c_key","hd_5c_key","hd_6c_key","hd_7c_key","hd_8c_key"]; # append values into a list

        def update_hdc_values(hd_c_keys_list):
            hd_c_values_list=[];
            for key in hd_c_keys_list:
                hd_c_values_list.append(st.session_state[key]); # append values into a list
            return hd_c_values_list

        hd_c_values_list=update_hdc_values(hd_c_keys_list);

    with st.expander("Shear connectors:"):
        st.write('Stiffness (kN/m)')
        sc_12k,sc_23k,sc_34k,sc_45k=st.columns(4); # divide the space into columns
        sc_56k,sc_67k,sc_78k,sc_89k=st.columns(4); # divide the space into columns

        st.text('')
        st.text('')

        st.write('Capacity (kN)')
        sc_12c,sc_23c,sc_34c,sc_45c=st.columns(4); # divide the space into columns
        sc_56c,sc_67c,sc_78c,sc_89=st.columns(4); # divide the space into columns

        sc_12k_value=sc_12k.number_input("k_s12 (kN/m)",value=1.,key="sc_12k_key"); # column's shear connector
        sc_23k_value=sc_23k.number_input("k_s23 (kN/m)",value=1.,key="sc_23k_key"); # column's shear connector
        sc_34k_value=sc_34k.number_input("k_s34 (kN/m)",value=1.,key="sc_34k_key"); # column's shear connector
        sc_45k_value=sc_45k.number_input("k_s45 (kN/m)",value=1.,key="sc_45k_key"); # column's shear connector
        sc_56k_value=sc_56k.number_input("k_s56 (kN/m)",value=1.,key="sc_56k_key"); # column's shear connector
        sc_67k_value=sc_67k.number_input("k_s67 (kN/m)",value=1.,key="sc_67k_key"); # column's shear connector
        sc_78k_value=sc_78k.number_input("k_s78 (kN/m)",value=1.,key="sc_78k_key"); # column's shear connector
        sc_k_keys_list=["sc_12k_key","sc_23k_key","sc_34k_key","sc_45k_key","sc_56k_key","sc_67k_key","sc_78k_key"]; # append values into a list

        def update_sck_values(sc_k_keys_list):
            sc_k_values_list=[];
            for key in sc_k_keys_list:
                sc_k_values_list.append(st.session_state[key]); # append values into a list
            return sc_k_values_list

        sc_k_values_list=update_sck_values(sc_k_keys_list);

        sc_12c_value=sc_12c.number_input("C_s12 (kN)",value=1.,key="sc_12c_key"); # column's shear connector
        sc_23c_value=sc_23c.number_input("C_s23 (kN)",value=1.,key="sc_23c_key"); # column's shear connector
        sc_34c_value=sc_34c.number_input("C_s34 (kN)",value=1.,key="sc_34c_key"); # column's shear connector
        sc_45c_value=sc_45c.number_input("C_s45 (kN)",value=1.,key="sc_45c_key"); # column's shear connector
        sc_56c_value=sc_56c.number_input("C_s56 (kN)",value=1.,key="sc_56c_key"); # column's shear connector
        sc_67c_value=sc_67c.number_input("C_s67 (kN)",value=1.,key="sc_67c_key"); # column's shear connector
        sc_78c_value=sc_78c.number_input("C_s78 (kN)",value=1.,key="sc_78c_key"); # column's shear connector
        sc_c_keys_list=["sc_12c_key","sc_23c_key","sc_34c_key","sc_45c_key","sc_56c_key","sc_67c_key","sc_78c_key"]; # append values into a list

        def update_scc_values(sc_c_keys_list):
            sc_c_values_list=[];
            for key in sc_c_keys_list:
                sc_c_values_list.append(st.session_state[key]); # append values into a list
            return sc_c_values_list

        sc_c_values_list=update_scc_values(sc_c_keys_list);

    with st.container():

        # update all the values
        column_values_list=update_column_values(column_keys_list);
        vload_values_list=update_vload_values(vload_keys_list);
        hd_k_values_list=update_hdk_values(hd_k_keys_list);
        hd_c_values_list=update_hdc_values(hd_c_keys_list);
        sc_k_values_list=update_sck_values(sc_k_keys_list);
        sc_c_values_list=update_scc_values(sc_c_keys_list);

        fig=plot_geometry(column_values_list,vload_values_list,hd_k_values_list,hd_c_values_list,sc_k_values_list,sc_c_values_list,h_column,d_column,d_beam)
        st.pyplot(fig)

        st.subheader("Geometry check")
        # Check for errors in the geomtery before running analysis:
        error=check_geometry(column_values_list,vload_keys_list,hd_k_keys_list,sc_k_keys_list);

with st.container():
    st.header("Tested configurations")
    st.write("Wall configurations tested at BRE. More info at https://doi.org/10.31224/2266")
    column_presets=st.columns(4); # Create the columnspan

    def SW_noLoad_update():
        st.session_state["col_1_key"] = "S";
        st.session_state["col_2_key"] = "S";
        st.session_state["col_3_key"] = "S";
        st.session_state["col_4_key"] = "S";
        st.session_state["col_5_key"] = "S";
        st.session_state["col_6_key"] = "S";
        st.session_state["col_7_key"] = "S";
        st.session_state["col_8_key"] = "S";

        st.session_state["vl_1_key"] = 0.5;
        st.session_state["vl_2_key"] = 0.5;
        st.session_state["vl_3_key"] = 0.5;
        st.session_state["vl_4_key"] = 0.5;
        st.session_state["vl_5_key"] = 0.5;
        st.session_state["vl_6_key"] = 0.5;
        st.session_state["vl_7_key"] = 0.5;
        st.session_state["vl_8_key"] = 0.5;

        st.session_state["hd_1k_key"] = 6.9;
        st.session_state["hd_2k_key"] = 6.9;
        st.session_state["hd_3k_key"] = 6.9;
        st.session_state["hd_4k_key"] = 6.9;
        st.session_state["hd_5k_key"] = 6.9;
        st.session_state["hd_6k_key"] = 6.9;
        st.session_state["hd_7k_key"] = 6.9;
        st.session_state["hd_8k_key"] = 6.9;

        st.session_state["hd_1c_key"] = 14.0;
        st.session_state["hd_2c_key"] = 14.0;
        st.session_state["hd_3c_key"] = 14.0;
        st.session_state["hd_4c_key"] = 14.0;
        st.session_state["hd_5c_key"] = 14.0;
        st.session_state["hd_6c_key"] = 14.0;
        st.session_state["hd_7c_key"] = 14.0;
        st.session_state["hd_8c_key"] = 14.0;

        st.session_state["sc_12k_key"] = 17.7;
        st.session_state["sc_23k_key"] = 17.7;
        st.session_state["sc_34k_key"] = 17.7;
        st.session_state["sc_45k_key"] = 17.7;
        st.session_state["sc_56k_key"] = 17.7;
        st.session_state["sc_67k_key"] = 17.7;
        st.session_state["sc_78k_key"] = 17.7;

        st.session_state["sc_12c_key"] = 39.3;
        st.session_state["sc_23c_key"] = 39.3;
        st.session_state["sc_34c_key"] = 39.3;
        st.session_state["sc_45c_key"] = 39.3;
        st.session_state["sc_56c_key"] = 39.3;
        st.session_state["sc_67c_key"] = 39.3;
        st.session_state["sc_78c_key"] = 39.3;

        st.session_state["cc_1_key"] = 0.4;

        st.session_state["E_w_key"]= 7800.;
        st.session_state["G_w_key"]= 142.;
        st.session_state["I_w_key"]= 7.56945684e+11;
        st.session_state["A_w_key"]= 290736*2/3;
        st.session_state["theta_max_key"]= 0.015;

# create a preset by prefilling some values when the button is hit
    def SW_Load_update():
        st.session_state["col_1_key"] = "S";
        st.session_state["col_2_key"] = "S";
        st.session_state["col_3_key"] = "S";
        st.session_state["col_4_key"] = "S";
        st.session_state["col_5_key"] = "S";
        st.session_state["col_6_key"] = "S";
        st.session_state["col_7_key"] = "S";
        st.session_state["col_8_key"] = "S";

        st.session_state["vl_1_key"] = 6.1;
        st.session_state["vl_2_key"] = 6.1;
        st.session_state["vl_3_key"] = 6.1;
        st.session_state["vl_4_key"] = 6.1;
        st.session_state["vl_5_key"] = 6.1;
        st.session_state["vl_6_key"] = 6.1;
        st.session_state["vl_7_key"] = 6.1;
        st.session_state["vl_8_key"] = 6.1;

        st.session_state["hd_1k_key"] = 6.9;
        st.session_state["hd_2k_key"] = 6.9;
        st.session_state["hd_3k_key"] = 6.9;
        st.session_state["hd_4k_key"] = 6.9;
        st.session_state["hd_5k_key"] = 6.9;
        st.session_state["hd_6k_key"] = 6.9;
        st.session_state["hd_7k_key"] = 6.9;
        st.session_state["hd_8k_key"] = 6.9;

        st.session_state["hd_1c_key"] = 14.0;
        st.session_state["hd_2c_key"] = 14.0;
        st.session_state["hd_3c_key"] = 14.0;
        st.session_state["hd_4c_key"] = 14.0;
        st.session_state["hd_5c_key"] = 14.0;
        st.session_state["hd_6c_key"] = 14.0;
        st.session_state["hd_7c_key"] = 14.0;
        st.session_state["hd_8c_key"] = 14.0;

        st.session_state["sc_12k_key"] = 17.7;
        st.session_state["sc_23k_key"] = 17.7;
        st.session_state["sc_34k_key"] = 17.7;
        st.session_state["sc_45k_key"] = 17.7;
        st.session_state["sc_56k_key"] = 17.7;
        st.session_state["sc_67k_key"] = 17.7;
        st.session_state["sc_78k_key"] = 17.7;

        st.session_state["sc_12c_key"] = 39.3;
        st.session_state["sc_23c_key"] = 39.3;
        st.session_state["sc_34c_key"] = 39.3;
        st.session_state["sc_45c_key"] = 39.3;
        st.session_state["sc_56c_key"] = 39.3;
        st.session_state["sc_67c_key"] = 39.3;
        st.session_state["sc_78c_key"] = 39.3;

        st.session_state["cc_1_key"] = 0.4;

        st.session_state["E_w_key"]= 7800.;
        st.session_state["G_w_key"]= 142.;
        st.session_state["I_w_key"]= 7.56945684e+11;
        st.session_state["A_w_key"]= 290736*2/3;
        st.session_state["theta_max_key"]= 0.015;

# create a preset by prefilling some values when the button is hit
    def WW_noLoad_update():
        st.session_state["col_1_key"] = "S";
        st.session_state["col_2_key"] = "W";
        st.session_state["col_3_key"] = "W";
        st.session_state["col_4_key"] = "S";
        st.session_state["col_5_key"] = "S";
        st.session_state["col_6_key"] = "W";
        st.session_state["col_7_key"] = "W";
        st.session_state["col_8_key"] = "S";

        st.session_state["vl_1_key"] = 0.5;
        st.session_state["vl_2_key"] = 0;
        st.session_state["vl_3_key"] = 0;
        st.session_state["vl_4_key"] = 0.5;
        st.session_state["vl_5_key"] = 0.5;
        st.session_state["vl_6_key"] = 0;
        st.session_state["vl_7_key"] = 0;
        st.session_state["vl_8_key"] = 0.5;

        st.session_state["hd_1k_key"] = 6.9;
        st.session_state["hd_2k_key"] = 6.9;
        st.session_state["hd_3k_key"] = 6.9;
        st.session_state["hd_4k_key"] = 6.9;
        st.session_state["hd_5k_key"] = 6.9;
        st.session_state["hd_6k_key"] = 6.9;
        st.session_state["hd_7k_key"] = 6.9;
        st.session_state["hd_8k_key"] = 6.9;

        st.session_state["hd_1c_key"] = 14.0;
        st.session_state["hd_2c_key"] = 14.0;
        st.session_state["hd_3c_key"] = 14.0;
        st.session_state["hd_4c_key"] = 14.0;
        st.session_state["hd_5c_key"] = 14.0;
        st.session_state["hd_6c_key"] = 14.0;
        st.session_state["hd_7c_key"] = 14.0;
        st.session_state["hd_8c_key"] = 14.0;

        st.session_state["sc_12k_key"] = 5.9;
        st.session_state["sc_23k_key"] = 5.9;
        st.session_state["sc_34k_key"] = 5.9;
        st.session_state["sc_45k_key"] = 17.7;
        st.session_state["sc_56k_key"] = 5.9;
        st.session_state["sc_67k_key"] = 5.9;
        st.session_state["sc_78k_key"] = 5.9;

        st.session_state["sc_12c_key"] = 39.3;
        st.session_state["sc_23c_key"] = 39.3;
        st.session_state["sc_34c_key"] = 39.3;
        st.session_state["sc_45c_key"] = 39.3;
        st.session_state["sc_56c_key"] = 39.3;
        st.session_state["sc_67c_key"] = 39.3;
        st.session_state["sc_78c_key"] = 39.3;

        st.session_state["cc_1_key"] = 0.4;

        st.session_state["E_w_key"]= 7800.;
        st.session_state["G_w_key"]= 142.;
        st.session_state["I_w_key"]= 7.56945684e+11;
        st.session_state["A_w_key"]= 290736*2/3;
        st.session_state["theta_max_key"]= 0.025;

# create a preset by prefilling some values when the button is hit
    def WW_Load_update():
        st.session_state["col_1_key"] = "S";
        st.session_state["col_2_key"] = "W";
        st.session_state["col_3_key"] = "W";
        st.session_state["col_4_key"] = "S";
        st.session_state["col_5_key"] = "S";
        st.session_state["col_6_key"] = "W";
        st.session_state["col_7_key"] = "W";
        st.session_state["col_8_key"] = "S";

        st.session_state["vl_1_key"] = 11.7;
        st.session_state["vl_2_key"] = 0;
        st.session_state["vl_3_key"] = 0;
        st.session_state["vl_4_key"] = 11.7;
        st.session_state["vl_5_key"] = 11.7;
        st.session_state["vl_6_key"] = 0;
        st.session_state["vl_7_key"] = 0;
        st.session_state["vl_8_key"] = 11.7;

        st.session_state["hd_1k_key"] = 6.9;
        st.session_state["hd_2k_key"] = 6.9;
        st.session_state["hd_3k_key"] = 6.9;
        st.session_state["hd_4k_key"] = 6.9;
        st.session_state["hd_5k_key"] = 6.9;
        st.session_state["hd_6k_key"] = 6.9;
        st.session_state["hd_7k_key"] = 6.9;
        st.session_state["hd_8k_key"] = 6.9;

        st.session_state["hd_1c_key"] = 14.0;
        st.session_state["hd_2c_key"] = 14.0;
        st.session_state["hd_3c_key"] = 14.0;
        st.session_state["hd_4c_key"] = 14.0;
        st.session_state["hd_5c_key"] = 14.0;
        st.session_state["hd_6c_key"] = 14.0;
        st.session_state["hd_7c_key"] = 14.0;
        st.session_state["hd_8c_key"] = 14.0;

        st.session_state["sc_12k_key"] = 5.9;
        st.session_state["sc_23k_key"] = 5.9;
        st.session_state["sc_34k_key"] = 5.9;
        st.session_state["sc_45k_key"] = 17.7;
        st.session_state["sc_56k_key"] = 5.9;
        st.session_state["sc_67k_key"] = 5.9;
        st.session_state["sc_78k_key"] = 5.9;

        st.session_state["sc_12c_key"] = 39.3;
        st.session_state["sc_23c_key"] = 39.3;
        st.session_state["sc_34c_key"] = 39.3;
        st.session_state["sc_45c_key"] = 39.3;
        st.session_state["sc_56c_key"] = 39.3;
        st.session_state["sc_67c_key"] = 39.3;
        st.session_state["sc_78c_key"] = 39.3;

        st.session_state["cc_1_key"] = 0.4;

        st.session_state["E_w_key"]= 7800.;
        st.session_state["G_w_key"]= 142.;
        st.session_state["I_w_key"]= 7.56945684e+11;
        st.session_state["A_w_key"]= 290736*2/3;
        st.session_state["theta_max_key"]= 0.025;

    SW_noLoad_button=column_presets[0].button('SW_noLoad',on_click=SW_noLoad_update);
    SW_Load_button=column_presets[1].button('SW_Load',on_click=SW_Load_update);
    WW_noLoad_button=column_presets[2].button('WW_noLoad',on_click=WW_noLoad_update);
    WW_Load_button=column_presets[3].button('WW_Load',on_click=WW_Load_update)


    # add check box for experimental Results
    # import experimental data-
    headers=['SW_noLoad_d1','SW_noLoad_F1','SW_noLoad_d2','SW_noLoad_F2','SW_Load_d','SW_Load_F','WW_noLoad_d','WW_noLoad_F','WW_Load_d','WW_Load_F']
    exp_data=pd.read_excel("Data_resume.xlsx",skiprows=(1),usecols=range(1,11),names=headers,sheet_name='fD');

    headers_2=['SW_noLoad_d','SW_noLoad_dvert','SW_Load_d','SW_Load_dvert','WW_noLoad_d','WW_noLoad_dvert','WW_Load_d','WW_Load_dvert'];
    exp_data_dic=pd.read_excel("Data_resume.xlsx",skiprows=(2),names=headers_2,sheet_name='v_d');

    exp_SW_noLoad,exp_SW_Load,exp_WW_noLoad,exp_WW_Load=st.columns(4); # Create the columnspan
    exp_SW_noLoad.checkbox('Exp data',key='exp_SW_noLoad_key')
    exp_SW_Load.checkbox('Exp data',key='exp_SW_Load_key')
    exp_WW_noLoad.checkbox('Exp data',key='exp_WW_noLoad_key')
    exp_WW_Load.checkbox('Exp data',key='exp_WW_Load_key')

    # generate the keys to pass for plotting
    exp_SW_noLoad_key=st.session_state.exp_SW_noLoad_key;
    exp_SW_Load_key=st.session_state.exp_SW_Load_key;
    exp_WW_noLoad_key=st.session_state.exp_WW_noLoad_key;
    exp_WW_Load_key=st.session_state.exp_WW_Load_key;


with st.container():
    st.header("Analysis")
    st.write("Plywood properties")
    E_w,G_w=st.columns(2)
    E_w_value=E_w.number_input("E (MPa)",value=7800.,key="E_w_key"); # Elastic modulus
    G_w_value=G_w.number_input("G (MPa)",value=142.,key="G_w_key"); # G modulus

    st.write("Wall inertia and shear area")
    I_w,A_w=st.columns(2)
    I_w_value=I_w.number_input("I (mm4)",value=7.56945684e+11,key="I_w_key"); # Second moment of inertia
    A_w_value=A_w.number_input("A (mm2)",value=290736*2/3,key="A_w_key"); # Shear area

    st.write("Other")
    cc_1,theta_max=st.columns(2); # divide the space into columns
    cc_1_value=cc_1.number_input("Stiffness modifier (-)",value=1.,key="cc_1_key"); # calibration coefficient
    theta_max_value=theta_max.number_input("Theta max (rad)",value=0.025,key="theta_max_key"); # calibration coefficient

    st.write(st.session_state.vl_1_key)
    analysis_button = st.button('Run analysis'); # create button analysis


    if analysis_button:
        # update all the values
        st.write(st.session_state.vl_1_key)
        column_values_list=update_column_values(column_keys_list);
        vload_values_list=update_vload_values(vload_keys_list);
        hd_k_values_list=update_hdk_values(hd_k_keys_list);
        hd_c_values_list=update_hdc_values(hd_c_keys_list);
        sc_k_values_list=update_sck_values(sc_k_keys_list);
        sc_c_values_list=update_scc_values(sc_c_keys_list);




        d_h,f_h,L_list,d_v,f_holddown,f_shear,i_fp_min,i_holdown_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_holdowns,i_failure_shear=calculate_pushover_and_failing_indeces(cc_1_value,hd_k_values_list[::-1],sc_k_values_list[::-1],vload_values_list[::-1],d_column,H,E_w_value,G_w_value,A_w_value,I_w_value,theta_max_value,hd_c_values_list[::-1],sc_c_values_list[::-1]);

        # call the function to plot the results
        fig1,fig2,fig3,fig4=results_plot(d_h,f_h,L_list,d_v,f_holddown,f_shear,i_fp_min,i_holdown_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_holdowns,i_failure_shear,exp_SW_noLoad_key,exp_SW_Load_key,exp_WW_noLoad_key,exp_WW_Load_key,exp_data,exp_data_dic);
        st.write("Force displacement response")
        st.pyplot(fig1)

        st.write("")
        st.write("Hold down forces")
        st.pyplot(fig2)

        st.write("")
        st.write("Shear forces")
        st.pyplot(fig3)

        st.write("")
        st.write("Vertical displacements at failure")
        st.pyplot(fig4)

        results_dataframe=pd.DataFrame({"Horizontal displacement (mm)":d_h,"Horizontal Force (kN)":f_h,
        "F holdown 1 (kN)":np.array(f_holddown).T[-1].tolist(), "F holdown 2 (kN)":np.array(f_holddown).T[-2].tolist(),
        "F holdown 3 (kN)":np.array(f_holddown).T[-3].tolist(),"F holdown 4 (kN)":np.array(f_holddown).T[-4].tolist(),
        "F holdown 5  (kN)":np.array(f_holddown).T[-5].tolist(),"F holdown 6 (kN)":np.array(f_holddown).T[-6].tolist(),
        "F holdown 7  (kN)":np.array(f_holddown).T[-7].tolist(),"F holdown 8 (kN)":np.array(f_holddown).T[-8].tolist()})

        download_button = st.download_button(
         label="Download data as CSV",
         data=results_dataframe.to_csv().encode('utf-8'),
         file_name='Skylark_walls.csv',
         mime='text/csv',
         )
