#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 12:53:30 2022
Mechanical model to describe the walls behavio
@author: dadsensor
"""
# import useful libraries


#%% import experiemntal data

#%% define constants
# CORR_1=0.2;
# CORR_2=0.2;
import numpy as np
import matplotlib.pyplot as plt



# define functions
def pegs_consitutiv_law(d_array,d_gap,k_peg):
    F_list=[];
    for d,k in zip(d_array,k_peg):
        if d<=d_gap:
            F=0;
        else:
            F=k*(d-d_gap);
        F_list.append(F)
    return np.array(F_list)


def wall_calculation(calibration_factors,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,d_gap): #height of the wall; # depth fot th column); # number of columns):
    n_columns=len(k_u_list); # number of columns

    corr_1=calibration_factors[0]; # assign the calibration factors
    corr_2=calibration_factors[1]; # assign_the calibration calibration_factors

    k_u1=k_u_list[0]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u2=k_u_list[1]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u3=k_u_list[2]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u4=k_u_list[3]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u5=k_u_list[4]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u6=k_u_list[5]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u7=k_u_list[6]*corr_1; # kN/mm uplifiting stiffness of the joint
    k_u8=k_u_list[7]*corr_1; # kN/mm uplifiting stiffness of the joint

    k_s1=k_s_list[0]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s2=k_s_list[1]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s3=k_s_list[2]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s4=k_s_list[3]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s5=k_s_list[4]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s6=k_s_list[5]*corr_2; # kN/mm shear slip modulus of the bow tie
    k_s7=k_s_list[6]*corr_2; # kN/mm shear slip modulus of the bow tie

    r_k1=k_u1/k_s1; # ratio of the stiffness
    r_k2=k_u2/k_s2; # ratio of the stiffness
    r_k3=k_u3/k_s3; # ratio of the stiffness
    r_k4=k_u4/k_s4; # ratio of the stiffness
    r_k5=k_u5/k_s5; # ratio of the stiffness
    r_k6=k_u6/k_s6; # ratio of the stiffness
    r_k7=k_u7/k_s7; # ratio of the stiffness

    F_v_g=np.array(F_v_list); # #vertical load vector
    L_list=np.arange(d_column*0.5,d_column*(n_columns),d_column); # list of lever arms
    n_unknowns=2*n_columns+1; # define the number of unknowns

    #%% build the first 2 lines of the matrix
    line_1=np.zeros(n_unknowns); #first line of the matrix
    for n,ele in enumerate(line_1):
        if n%2==0 and n<=2*len(L_list)-1:
            line_1[n]=L_list[int((n)/2)];
    line_1[n_columns*2-1]=-H;


    #%% local equilibrium on each column
    A=np.array([[-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
               [0,1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,1,-1,-1,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,1,-1,-1,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,1,-1,-1,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,1,-1,-1,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,1,-1,-1,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0]])

    #%% build the congruence equations evector
    C=np.array([[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,r_k1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,r_k1,0,r_k2,1,0,0,0,0,0,0,0,0,0,0,0,0],
                 [0,r_k1,0,r_k2,0,r_k3,1,0,0,0,0,0,0,0,0,0,0],
                 [0,r_k1,0,r_k2,0,r_k3,0,r_k4,1,0,0,0,0,0,0,0,0],
                 [0,r_k1,0,r_k2,0,r_k3,0,r_k4,0,r_k5,1,0,0,0,0,0,0],
                 [0,r_k1,0,r_k2,0,r_k3,0,r_k4,0,r_k5,0,r_k6,1,0,0,0,0],
                 [0,r_k1,0,r_k2,0,r_k3,0,r_k4,0,r_k5,0,r_k6,0,r_k7,1,0,0]]);

    #%% Assemble the matrix
    A_final=np.concatenate(([line_1],A,C),axis=0)

    #%% Assemble the B vector
    B=np.zeros(n_unknowns);
    B[0]=-F_v_g.dot(L_list); # contribution of the vertical loads
    B[1]=F_v_g[0];# contribution of the vertical loads
    B[2]=F_v_g[1];# contribution of the vertical loads
    B[3]=F_v_g[2];# contribution of the vertical loads
    B[4]=F_v_g[3];# contribution of the vertical loads
    B[5]=F_v_g[4];# contribution of the vertical loads
    B[6]=F_v_g[5];# contribution of the vertical loads
    B[7]=F_v_g[6];# contribution of the vertical loads
    B[8]=F_v_g[7];# contribution of the vertical loads

    #%% create the epty lists to be filled
    d_h=[]; # horizontal displacement list
    f_h=[]; # horizontal force list
    d_v=[]; # vertical displacement list
    f_peg=[]; # force on the pegs
    f_shear=[]; # shear forces

    theta=np.arange(0.00, 0.04,0.00025)
    for t in theta:
        d_combined=[]; # displacement vector
        for L in L_list:
            d=L*t; # calculate the vertical displacement and substract the slip
            d_combined.append(max(0,d)); # append the value if positive

        #B[n_columns+1:]=np.array(d_combined) *np.array([k_u1,k_u2,k_u3,k_u4,k_u5,k_u6,k_u7,k_u8]); # multiply for the stiiffness to get the forces
        B[n_columns+1:]=pegs_consitutiv_law(d_combined,d_gap,[k_u1,k_u2,k_u3,k_u4,k_u5,k_u6,k_u7,k_u8])
        X=np.linalg.solve(A_final,B); # solve the linear system
        f_h.append(X[15]); # horizontal force
        d_v_i=np.array([X[0]/k_u1,X[2]/k_u2,X[4]/k_u3,X[6]/k_u4,X[8]/k_u5,X[10]/k_u6,X[12]/k_u7,X[14]/k_u7]) # vertical displacement vector
        d_v.append(np.array(d_v_i)); # append the correct values
        f_peg.append(np.array([X[0],X[2],X[4],X[6],X[8],X[10],X[12],X[14]])); # store the force in the pegs
        f_shear.append(np.array([X[1],X[3],X[5],X[7],X[9],X[11],X[13]])); # store the force in the shear connectors
        shear_deformation=X[15]*1000*H/(G_w*A_w);
        bending_deformation=X[15]*1000*H/(2*E_w*I_w)
        d_h.append(t*H+shear_deformation+bending_deformation); # calculate the horizontal displacement
    return d_h,f_h,L_list,d_v,f_peg,f_shear;

def check_peg_failures(f_peg_list,f_fail_list):
    i_failure_indeces=[]; # failure indices
    for f_peg,f_fail in zip(f_peg_list,f_fail_list):
        i_fail_vector=np.argwhere(np.array(f_peg)>f_fail); # find the potioning index where the failure load is met
        if i_fail_vector.size==0:
            i_fail_index=len(f_peg)-1; # if failure does not occure, set the last possible index
        else:
            i_fail_index=int(i_fail_vector[0]); # take the smallest index
        i_failure_indeces.append(i_fail_index); # vector containing the failure indices for each peg
    return i_failure_indeces

def check_shear_failures(f_shear_list,f_failshear_list):
    i_failure_indeces=[]; # failure indices
    for f_peg,f_fail in zip(f_shear_list,f_failshear_list):
        i_fail_vector=np.argwhere(np.array(f_peg)>f_fail); # find the potioning index where the failure load is met
        if i_fail_vector.size==0:
            i_fail_index=len(f_peg)-1; # if failure does not occure, set the last possible index
        else:
            i_fail_index=int(i_fail_vector[0]); # take the smallest index
        i_failure_indeces.append(i_fail_index); # vector containing the failure indices for each peg
    return i_failure_indeces

# def plot_fh_vs_dh(d_h,f_h,i_fp_min,i_peg_failing_swap,i_fshear_min,i_shear_failing_swap):
#
#     return

def peg_swapping(k):
    N=['8','7','6','5','4','3','2','1']; # reverse pegs list
    return N[k]

def shearconnector_swapping(k):
    N=['7-8','6-7','5-6','4-5','3-4','2-3','1-2']; # reverse shear connector list
    return N[k]

def calculate_and_plot_walls(calibration_factors,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,d_gap,f_fail_list,f_failshear_list):
    # calling the wall_calculation_function where d_h horizontal displacement, f_h horizontal force, L_list lever arm distances for the pegs,d_v vertical displacements, f_peg force in the pegs,f_shear force in the shear connectors
    d_h,f_h,L_list,d_v,f_peg,f_shear=wall_calculation(calibration_factors,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,d_gap);
    i_failure_pegs=check_peg_failures(np.array(f_peg).transpose(),f_fail_list); # checkes whether a peg failed
    i_fp_min=min(i_failure_pegs); # check smallest value of peg failing
    i_peg_failing=np.argmin(i_failure_pegs); # check what is the peg failing: add one beacuse counting starts from zero
    i_peg_failing_swap=peg_swapping(i_peg_failing);

    i_failure_shear=check_shear_failures(np.array(f_shear).transpose(),f_failshear_list); # check wheter a shear connection failed
    i_fshear_min=min(i_failure_shear); # check smallest value of shear connector failing
    i_shear_failing=np.argmin(i_failure_shear); # check what is the shear connector failing: add one beacuse counting starts from zero
    i_shear_failing_swap=shearconnector_swapping(i_shear_failing);

    return d_h,f_h,L_list,d_v,f_peg,f_shear,i_fp_min,i_peg_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_pegs,i_failure_shear;
