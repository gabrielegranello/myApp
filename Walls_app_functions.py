# import useful libraries
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

#create a function that plots the geometry--------------------------------------------
def plot_geometry(column_values_list,vload_values_list,hd_k_values_list,hd_c_values_list,sc_k_values_list,sc_c_values_list,h_column,d_column,d_beam):
    arrowsize=600; # arrow value for plotting purposes
    L_wall=len(column_values_list)*d_column; # length of the wall

    fig,ax = plt.subplots()
    rect_patches=[]; # define the empty list
    # loop over the values and create the rectangular patches for plot
    for i,value in enumerate(column_values_list):
        if value=="S":
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), d_column, h_column, linewidth=1, edgecolor='k', facecolor='none'))
        elif value=="W":
            rect_patches.append(patches.Rectangle((i*d_column, 0.0), d_column, h_column/2, linewidth=1, edgecolor='k', facecolor='none'))
        elif value=="D":
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
        if F!=0:
            if str(column_values_list[i])=="D" or str(column_values_list[i])=="W":
                ax.arrow(x_arrow,h_column+d_beam,0,-arrowsize,color='r',width=1,head_width=50); # add the arrow
                ax.text(x_arrow-0.33*d_column,h_column+d_beam+150,str(F),color='r',fontsize=8);
            else:
                ax.arrow(x_arrow,h_column+d_beam,0,-arrowsize,color='b',width=1,head_width=50); # add the arrow
                ax.text(x_arrow-0.33*d_column,h_column+d_beam+150,str(F),color='b',fontsize=8);

    # loop over the the hold down forces
    uplift_interface_width=4;
    for i,k_u in enumerate(hd_k_values_list):
        if float(k_u)!=0:
            if str(column_values_list[i])=="D":
                ax.plot([i*d_column,i*d_column+d_column],[0,0],'r',linewidth=uplift_interface_width)
                ax.text(i*d_column,-200,str(k_u),color='r',fontsize='small');
            else:
                ax.plot([i*d_column,i*d_column+d_column],[0,0],'g',linewidth=uplift_interface_width)
                ax.text(i*d_column,-200,str(k_u),color='g',fontsize='small');

    # # loop over the sher stiffness values
    shear_interface_width=4;
    for i,k_s in enumerate(sc_k_values_list):
            if float(k_s)!=0:
                if str(column_values_list[i])=="D" or str(column_values_list[i+1])=="D":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,h_column],'r',linewidth=shear_interface_width)

                elif str(column_values_list[i])=="S" and str(column_values_list[i+1])=="S":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,h_column],'g',linewidth=shear_interface_width)
                    ax.text(i*d_column+d_column+50,0.4*h_column,str(k_s),color='g',fontsize='small',rotation='vertical');
                elif str(column_values_list[i])=="W" or str(column_values_list[i+1])=="W":
                    ax.plot([i*d_column+d_column,i*d_column+d_column],[0,0.5*h_column],'g',linewidth=shear_interface_width)
                    ax.text(i*d_column+d_column+50,0.2*h_column,str(k_s),color='g',fontsize='small',rotation='vertical');

    # lateral force and displacement arrows
    ax.arrow(-arrowsize-50,h_column+0.5*d_beam,arrowsize,0,color='b',width=1,head_width=50); # add the arrow
    ax.text(-2*arrowsize/3,h_column+0.5*d_beam+50,r"$F_h$",color='b',fontsize='medium');

    ax.arrow(L_wall,h_column+0.5*d_beam,arrowsize*0.3,0,color='b',width=1,head_width=50); # add the arrow
    ax.text(L_wall+arrowsize*0.05,h_column+0.5*d_beam+50,r"$d_h$",color='b',fontsize='medium');

    ax.set_xlim(-d_beam*3,len(column_values_list)*d_column+d_column);
    ax.set_ylim(-d_beam,h_column+2*d_beam)
    return fig

#%% Check the geomtery -------------------------------------------------------------------------------------------------------------------------
def check_geometry(column_values_list,vload_keys_list,hd_k_keys_list,sc_k_keys_list):

    # Check if there is a vertical load on top of door or window
    id_error=0;
    for i,(c_type,F_v) in enumerate(zip(column_values_list,vload_keys_list)):
        if c_type=="D" or c_type=="W":
            if st.session_state[F_v]!=0:
                id_error+=1
                error_text_vl='<p style="color:Red;">Warning '+ str(id_error)+': Attention! Check vertical load!</p>'
                st.markdown(error_text_vl,unsafe_allow_html=True)

    # Check if there is a hold down connector under a door
    for i,(c_type,k_hd) in enumerate(zip(column_values_list,hd_k_keys_list)):
        if c_type=="D":
            if st.session_state[k_hd]!=0:
                id_error+=1
                error_text_hd='<p style="color:Red;">Warning '+ str(id_error)+': Attention! Check hold down connectors!</p>'
                st.markdown(error_text_hd,unsafe_allow_html=True)


    # Check if there is a shear connector on the side of a door
    for i,k_s in enumerate(sc_k_keys_list):
        if column_values_list[i]=="D" or column_values_list[i+1]=="D":
            if st.session_state[k_s]!=0:
                id_error+=1
                error_text_sc='<p style="color:Red;">Warning '+ str(id_error)+': Attention! Check shear connectors!</p>'
                st.markdown(error_text_sc,unsafe_allow_html=True)

    if id_error==0:
        no_error_text='<p style="color:Green;">Geometry of the wall OK!</p>'
        st.markdown(no_error_text,unsafe_allow_html=True)

    return id_error

#%% fuction to plot the results-----------------------------------------------------------------------------------
def results_plot(d_h,f_h,L_list,d_v,f_holddown,f_shear,i_fp_min,i_holdown_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_holdowns,i_failure_shear,exp_SW_noLoad_key,exp_SW_Load_key,exp_WW_noLoad_key,exp_WW_Load_key,exp_data,exp_data_dic):

    # plot the pushover
    fig1,ax1=plt.subplots()

    # plot experimental results
    if exp_SW_noLoad_key:
        ax1.plot(exp_data["SW_noLoad_d1"],exp_data["SW_noLoad_F1"],'tab:blue',label="SW_noLoad exp")
        ax1.plot(exp_data["SW_noLoad_d2"],exp_data["SW_noLoad_F2"],'tab:blue')

    if exp_SW_Load_key:
        ax1.plot(exp_data["SW_Load_d"],exp_data["SW_Load_F"],'tab:pink',label="SW_Load exp")

    if exp_WW_noLoad_key:
        ax1.plot(exp_data["WW_noLoad_d"],exp_data["WW_noLoad_F"],'tab:cyan',label="WW_noLoad exp")

    if exp_WW_Load_key:
        ax1.plot(exp_data["WW_Load_d"],exp_data["WW_Load_F"],'tab:red',label="WW_Load exp")


    ax1.plot(d_h,f_h,'k--',label='model calibrated')
    ax1.plot(d_h[i_fp_min],f_h[i_fp_min],'rx',label='holdown '+i_holdown_failing_swap)
    ax1.plot(d_h[i_fshear_min],f_h[i_fshear_min],'ro',label='shear conn '+ i_shear_failing_swap)
    ax1.set_xlabel(r'$d_h$ (mm)')
    ax1.set_ylabel('$F_h$ (kN)')
    ax1.legend(loc='best')
    ax1.grid()


    # plot the holddown forces
    fig2,ax2=plt.subplots()
    f_holddownTra=np.array(f_holddown).transpose(); # tranpose the matrix
    colors=['tab:blue','tab:orange','tab:pink','tab:brown','tab:cyan','tab:olive','tab:purple','tab:red'];
    for i,(f_p,c,i_fp) in enumerate(zip(f_holddownTra,colors,i_failure_holdowns)):
        ax2.plot(d_h[0:i_fp],f_p[0:i_fp],label="holdown "+holdown_swapping(i),color=c)
        if i_fp < len(d_h)-1:
            ax2.plot(d_h[i_fp],f_p[i_fp],'x',color=c); # plot the failure with x

    ax2.set_xlabel(r'$d_h$ (mm)')
    ax2.set_ylabel(r'$F_{holdown}$ (kN)')
    ax2.legend(loc='best')
    ax2.grid()

    # plot the shear forces
    fig3,ax3=plt.subplots()
    f_shearTra=np.array(f_shear).transpose(); # transpose the matrix
    for i,(f_s,c,i_fs) in enumerate(zip(f_shearTra,colors,i_failure_shear)):
        ax3.plot(d_h[0:i_fs],f_p[0:i_fs],label="shear conn "+shearconnector_swapping(i),color=c)
        if i_fs < len(d_h)-1:
            ax3.plot(d_h[i_fs],f_p[i_fs],'o',color=c); # plot the failure with x

    ax3.set_xlabel(r'$d_h$ (mm)')
    ax3.set_ylabel(r'$F_{shear}$ (kN)')
    ax3.legend(loc='best')
    ax3.grid()

    # plot the vertical displacements at i_failure_pegs
    fig4,ax4=plt.subplots()
    d_v_holdown=d_v[i_fp_min]; # vertical displacement where the holdown fails
    d_v_shear=d_v[i_fshear_min]; # vertical displacement where the shear connector fails
    ax4.plot(L_list[::-1],d_v_holdown,'kx--',markeredgecolor='r',label='holdown failure')
    ax4.plot(L_list[::-1],d_v_shear,'ko--',markeredgecolor='r',label='holdown failure')

    if exp_SW_noLoad_key:
        ax4.plot(exp_data_dic["SW_noLoad_d"],exp_data_dic["SW_noLoad_dvert"],'tab:blue',label="SW_noLoad exp")

    if exp_SW_Load_key:
        ax4.plot(exp_data_dic["SW_Load_d"],exp_data_dic["SW_Load_dvert"],'tab:pink',label="SW_Load exp")

    if exp_WW_noLoad_key:
        ax4.plot(exp_data_dic["WW_noLoad_d"],exp_data_dic["WW_noLoad_dvert"],'tab:cyan',label="WW_noLoad exp")

    if exp_WW_Load_key:
        ax4.plot(exp_data_dic["WW_Load_d"],exp_data_dic["WW_Load_dvert"],'tab:red',label="WW_Load exp")

    ax4.set_ylabel(r'$d_v$ (mm)')
    ax4.set_xlabel(r'$L_{wall}$ (mm)')
    ax4.legend(loc='best')
    ax4.grid()

    return fig1,fig2,fig3,fig4


# Hold down elastic constitutive law: retuns the force in the hold down connectors-------------------------------------------------------------------------
def hold_down_constitutive_law(d_array,k_hd):
    F_list=[];
    for d,k in zip(d_array,k_hd):
        F=k*d; # calculate the force as displacement* stiffness
        F_list.append(F)
    return np.array(F_list)

#%% the function solves the equilibrium equations + consitutive laws to find the displacements and forces--------------------------------------------------
def calculate_pushover(calibration_factor,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,theta_max_value): #height of the wall; # depth fot th column); # number of columns):
    n_columns=len(k_u_list); # number of columns

    k_u1=k_u_list[0]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u2=k_u_list[1]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u3=k_u_list[2]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u4=k_u_list[3]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u5=k_u_list[4]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u6=k_u_list[5]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u7=k_u_list[6]*calibration_factor; # kN/mm uplifiting stiffness of the joint
    k_u8=k_u_list[7]*calibration_factor; # kN/mm uplifiting stiffness of the joint

    k_s1=k_s_list[0]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s2=k_s_list[1]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s3=k_s_list[2]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s4=k_s_list[3]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s5=k_s_list[4]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s6=k_s_list[5]*calibration_factor; # kN/mm shear slip modulus of the bow tie
    k_s7=k_s_list[6]*calibration_factor; # kN/mm shear slip modulus of the bow tie

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
    f_holddown=[]; # force on the holdowns
    f_shear=[]; # shear forces

    theta=np.arange(0.00, theta_max_value,0.00025)
    for t in theta:
        d_combined=[]; # displacement vector
        for L in L_list:
            d=L*t; # calculate the vertical displacement and substract the slip
            d_combined.append(max(0,d)); # append the value if positive

        #B[n_columns+1:]=np.array(d_combined) *np.array([k_u1,k_u2,k_u3,k_u4,k_u5,k_u6,k_u7,k_u8]); # multiply for the stiiffness to get the forces
        B[n_columns+1:]=hold_down_constitutive_law(d_combined,[k_u1,k_u2,k_u3,k_u4,k_u5,k_u6,k_u7,k_u8])
        X=np.linalg.solve(A_final,B); # solve the linear system
        f_h.append(X[15]); # horizontal force
        d_v_i=np.array([X[0]/k_u1,X[2]/k_u2,X[4]/k_u3,X[6]/k_u4,X[8]/k_u5,X[10]/k_u6,X[12]/k_u7,X[14]/k_u7]) # vertical displacement vector
        d_v.append(np.array(d_v_i)); # append the correct values
        f_holddown.append(np.array([X[0],X[2],X[4],X[6],X[8],X[10],X[12],X[14]])); # store the force in the holdowns
        f_shear.append(np.array([X[1],X[3],X[5],X[7],X[9],X[11],X[13]])); # store the force in the shear connectors
        shear_deformation=X[15]*1000*H/(G_w*A_w);
        bending_deformation=X[15]*1000*H/(2*E_w*I_w)
        d_h.append(t*H+shear_deformation+bending_deformation); # calculate the horizontal displacement
    return d_h,f_h,L_list,d_v,f_holddown,f_shear;

#% The function checks wether a failure is occurred in the hold down connectors by comparing with the maximum allowable force--------------------------------------------
def check_holdown_failures(f_holddown_list,f_failholdown_list):
    i_failure_indeces=[]; # failure indices
    for f_holddown,f_fail in zip(f_holddown_list,f_failholdown_list):
        i_fail_vector=np.argwhere(np.array(f_holddown)>f_fail); # find the postion  index where the failure load is met
        if i_fail_vector.size==0:
            i_fail_index=len(f_holddown)-1; # if failure does not occurr, set the last possible index
        else:
            i_fail_index=int(i_fail_vector[0]); # take the smallest index
        i_failure_indeces.append(i_fail_index); # vector containing the failure indices for each holdown
    return i_failure_indeces

#% The function checks wether a failure is occurred in the shear connectors by comparing with the maximum allowable force--------------------------------------------
def check_shear_failures(f_shear_list,f_failshear_list):
    i_failure_indeces=[]; # failure indices
    for f_holddown,f_fail in zip(f_shear_list,f_failshear_list):
        i_fail_vector=np.argwhere(np.array(f_holddown)>f_fail); # find the potioning index where the failure load is met
        if i_fail_vector.size==0:
            i_fail_index=len(f_holddown)-1; # if failure does not occure, set the last possible index
        else:
            i_fail_index=int(i_fail_vector[0]); # take the smallest index
        i_failure_indeces.append(i_fail_index); # vector containing the failure indices for each holdown
    return i_failure_indeces

#% The function swap the indeces for plotting purposes--------------------------------
def holdown_swapping(k):
    N=['8','7','6','5','4','3','2','1']; # reverse holdowns list
    return N[k]

#% The function swap the indeces for plotting purposes--------------------------------
def shearconnector_swapping(k):
    N=['7-8','6-7','5-6','4-5','3-4','2-3','1-2']; # reverse shear connector list
    return N[k]

# the function returns the pushover with also the fialing indeces fo each peg
def calculate_pushover_and_failing_indeces(calibration_factors,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,theta_max_value,f_failholdown_list,f_failshear_list):

    # calling the calculate_pushover_function where d_h horizontal displacement, f_h horizontal force, L_list lever arm distances for the holdowns,d_v vertical displacements, f_holddown force in the holdowns,f_shear force in the shear connectors
    d_h,f_h,L_list,d_v,f_holddown,f_shear=calculate_pushover(calibration_factors,k_u_list,k_s_list,F_v_list,d_column,H,E_w,G_w,A_w,I_w,theta_max_value);
    i_failure_holdowns=check_holdown_failures(np.array(f_holddown).transpose(),f_failholdown_list); # checkes whether a holdown failed
    i_fp_min=min(i_failure_holdowns); # check smallest value of holdown failing
    i_holdown_failing=np.argmin(i_failure_holdowns); # check what is the holdown failing: add one beacuse counting starts from zero
    i_holdown_failing_swap=holdown_swapping(i_holdown_failing); # swap for plotting purposes

    i_failure_shear=check_shear_failures(np.array(f_shear).transpose(),f_failshear_list); # check wheter a shear connection failed
    i_fshear_min=min(i_failure_shear); # check smallest value of shear connector failing
    i_shear_failing=np.argmin(i_failure_shear); # check what is the shear connector failing: add one beacuse counting starts from zero
    i_shear_failing_swap=shearconnector_swapping(i_shear_failing); # swap for plotting purposes

    return d_h,f_h,L_list,d_v,f_holddown,f_shear,i_fp_min,i_holdown_failing_swap,i_fshear_min,i_shear_failing_swap,i_failure_holdowns,i_failure_shear;
