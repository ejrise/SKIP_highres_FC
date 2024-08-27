
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 17:54:38 2024

@author: elizabethrizor
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import zscore
import pingouin as pg
import seaborn as sns
from statannot import add_stat_annotation
from scipy.stats import skewtest 
import statannot
import numpy as np

# Read the CSV file into a DataFrame
df = pd.read_csv("mean_connectivity_values_lefthem.csv")
df['Map-Mask'] = df['Connectivity_Map'] + '-' + df['Mask']

#AIM 1: SUBCORTICAL FC 
# Define the factors for BLA and Thal
factor1_levels = ['left_AMY_BL_Complex-bin_left_ventral_putamen', 'left_AMY_BL_Complex-bin_left_dorsal_putamen']
factor2_levels = ['left_Thal_VL_AAL3-bin_left_ventral_putamen', 'left_Thal_VL_AAL3-bin_left_dorsal_putamen']

relevant_conditions = factor1_levels + factor2_levels
filtered_df = df[df['Map-Mask'].isin(relevant_conditions)]
filtered_df = filtered_df.rename(columns={'Connectivity_Map': 'subcortnode'})
filtered_df = filtered_df.rename(columns={'Mask': 'putamen'})
    
# Perform the 2x2 ANOVA
aov = pg.rm_anova(dv='Mean_Connectivity_Value', within=['subcortnode', 'putamen'], subject='Subject_ID', correction='auto', detailed=True, effsize='ng2', data=filtered_df)
pair = pg.pairwise_tests(dv='Mean_Connectivity_Value',  within=['subcortnode', 'putamen'], subject='Subject_ID', correction='auto', effsize='cohen', padjust='bonf', return_desc='True', data=filtered_df)

# Define the factors for BLA and Thal
factor1_levels = ['left_BF_ch4-bin_left_ventral_putamen', 'left_Thal_VL_AAL3-bin_left_ventral_putamen']
factor2_levels = ['left_BF_ch4-bin_left_dorsal_putamen', 'left_Thal_VL_AAL3-bin_left_dorsal_putamen']

relevant_conditions = factor1_levels + factor2_levels
filtered_df2 = df[df['Map-Mask'].isin(relevant_conditions)]
filtered_df2 = filtered_df2.rename(columns={'Connectivity_Map': 'subcortnode'})
filtered_df2 = filtered_df2.rename(columns={'Mask': 'putamen'})
    
# Perform the 2x2 ANOVA
aov2 = pg.rm_anova(dv='Mean_Connectivity_Value', within=['subcortnode', 'putamen'], subject='Subject_ID', correction='auto', detailed=True, effsize='ng2', data=filtered_df2)
pair2 = pg.pairwise_tests(dv='Mean_Connectivity_Value',  within=['subcortnode', 'putamen'], subject='Subject_ID', correction='auto', effsize='cohen', padjust='bonf', return_desc='True', data=filtered_df2)

#plot subcortical FC
#Define the regions to plot
regions = ['left_AMY_BL_Complex-bin_left_ventral_putamen', 'left_AMY_BL_Complex-bin_left_dorsal_putamen', 'left_AMY_BL_Complex-bin_left_accumbens_thr50', 
           'left_BF_ch4-bin_left_ventral_putamen', 'left_BF_ch4-bin_left_dorsal_putamen', 'left_BF_ch4-bin_left_accumbens_thr50', 
           'left_Thal_VL_AAL3-bin_left_ventral_putamen', 'left_Thal_VL_AAL3-bin_left_dorsal_putamen', 'left_Thal_VL_AAL3-bin_left_accumbens_thr50',
           'left_GPi_pauli-bin_left_dorsal_putamen', 'left_GPi_pauli-bin_left_ventral_putamen', 'left_GPi_pauli-bin_left_accumbens_thr50']

filtered_df3 = df[df['Map-Mask'].isin(regions)]
filtered_df3 = filtered_df3.rename(columns={'Connectivity_Map': 'subcortnode'})
filtered_df3 = filtered_df3.rename(columns={'Mask': 'putamen'})

# Initialize the plot
plt.figure(figsize=(20, 10))

# Create the bar plot with error bars
bar = sns.barplot(data=filtered_df3, x='subcortnode', y='Mean_Connectivity_Value', hue='putamen', errorbar='se', palette=['gold', '#89CFF0', '#FF6F61'], capsize=.05, 
                  order=['left_AMY_BL_Complex', 'left_BF_ch4', 'left_GPi_pauli', 'left_Thal_VL_AAL3'])

bar.set_title('Subcortical Node-Putamen FC', fontsize=36)
bar.set_xlabel('Seed Region', fontsize=30)
bar.set_ylabel("Mean FC (Fisher's Z)", fontsize=30)
bar.set_xticklabels(["BLA", "NBM", "GPi", "ThalVL"])
bar.tick_params(axis='both', which='major', labelsize=26)

handles, labels = plt.gca().get_legend_handles_labels()
bar.legend(handles=handles, labels=['NAc','PUTd','PUTv'],loc='upper left', fontsize=26)

sns.despine()

# Add the post-hoc test annotation
statannot.add_stat_annotation(plt.gca(),
                              data=filtered_df3, 
                              x='subcortnode', 
                              y='Mean_Connectivity_Value', 
                              order=['left_AMY_BL_Complex', 'left_BF_ch4', 'left_GPi_pauli', 'left_Thal_VL_AAL3'],
                              hue='putamen',
                              box_pairs=[(('left_AMY_BL_Complex', 'bin_left_accumbens_thr50'), ('left_AMY_BL_Complex', 'bin_left_ventral_putamen')),
                                         (('left_AMY_BL_Complex', 'bin_left_dorsal_putamen'), ('left_AMY_BL_Complex', 'bin_left_ventral_putamen')),
                                         (('left_BF_ch4', 'bin_left_accumbens_thr50'), ('left_BF_ch4', 'bin_left_ventral_putamen')),
                                         (('left_BF_ch4', 'bin_left_dorsal_putamen'), ('left_BF_ch4', 'bin_left_ventral_putamen')), 
                                         (('left_GPi_pauli', 'bin_left_accumbens_thr50'), ('left_GPi_pauli', 'bin_left_ventral_putamen')),
                                         (('left_GPi_pauli', 'bin_left_dorsal_putamen'), ('left_GPi_pauli', 'bin_left_ventral_putamen')),
                                         (('left_Thal_VL_AAL3', 'bin_left_accumbens_thr50'), ('left_Thal_VL_AAL3', 'bin_left_ventral_putamen')),
                                         (('left_Thal_VL_AAL3', 'bin_left_dorsal_putamen'), ('left_Thal_VL_AAL3', 'bin_left_ventral_putamen'))],
                              test='t-test_paired', 
                              text_format='star',
                              loc='inside', 
                              fontsize='26',
                              verbose=2)

bar.figure.savefig("/path/to/folder/put_fc_fig2.png", bbox_inches="tight",dpi=300)

#AIM 2: MOTOR CORTICAL FC
# Define the factors and the dependent variable
regions1 = ['left_SMA-bin_left_ventral_putamen', 'left_SMA-bin_left_dorsal_putamen', 
            'left_CMA-bin_left_ventral_putamen', 'left_CMA-bin_left_dorsal_putamen', 
           'left_precentral_gyrus_A4ul_thr25-bin_left_ventral_putamen', 'left_precentral_gyrus_A4ul_thr25-bin_left_dorsal_putamen']

regions2 = ['left_SMA-bin_left_ventral_putamen', 'left_SMA-bin_left_accumbens_thr50', 
            'left_CMA-bin_left_ventral_putamen', 'left_CMA-bin_left_accumbens_thr50', 
           'left_precentral_gyrus_A4ul_thr25-bin_left_ventral_putamen', 'left_precentral_gyrus_A4ul_thr25-bin_left_accumbens_thr50']

regions3 = ['frontmed_cortex-bin_left_ventral_putamen', 'frontmed_cortex-bin_left_dorsal_putamen', 'frontmed_cortex-bin_left_accumbens_thr50']

filtered_df5 = df[df['Map-Mask'].isin(regions1)]
filtered_df5 = filtered_df5.rename(columns={'Connectivity_Map': 'motorarea'})
filtered_df5 = filtered_df5.rename(columns={'Mask': 'putamen'})
    
# Perform the 2x3 ANOVA for PUTv vs PUTd
aov3 = pg.rm_anova(dv='Mean_Connectivity_Value', within=['motorarea','putamen'], subject='Subject_ID', correction='auto', detailed=True, effsize='ng2', data=filtered_df5)
pair3 = pg.pairwise_tests(dv='Mean_Connectivity_Value',  within=['motorarea','putamen'], subject='Subject_ID', correction='auto', effsize='cohen', padjust='bonf', return_desc='True', data=filtered_df5)

filtered_df6 = df[df['Map-Mask'].isin(regions2)]
filtered_df6 = filtered_df6.rename(columns={'Connectivity_Map': 'motorarea'})
filtered_df6 = filtered_df6.rename(columns={'Mask': 'putamen'})
    
# Perform the 2x3 ANOVA for PUTv vs NAc
aov4 = pg.rm_anova(dv='Mean_Connectivity_Value', within=['motorarea', 'putamen'], subject='Subject_ID', correction='auto', detailed=True, effsize='ng2', data=filtered_df6)
pair4 = pg.pairwise_tests(dv='Mean_Connectivity_Value',  within=['motorarea', 'putamen'], subject='Subject_ID', correction='auto', effsize='cohen', padjust='bonf', return_desc='True', data=filtered_df6)

#NAc mPFC analysis
filtered_df7 = df[df['Map-Mask'].isin(regions3)]
filtered_df7 = filtered_df7.rename(columns={'Connectivity_Map': 'frontmed'})
filtered_df7 = filtered_df7.rename(columns={'Mask': 'putamen'})
aov5 = pg.rm_anova(dv='Mean_Connectivity_Value', within=['putamen'], subject='Subject_ID', correction='auto', detailed=True, effsize='ng2', data=filtered_df7)
pair5 = pg.pairwise_tests(dv='Mean_Connectivity_Value',  within=['putamen'], subject='Subject_ID', correction='auto', effsize='cohen', padjust='bonf', return_desc='True', data=filtered_df7)

#Motor cortical area plot  
regions = ['left_SMA-bin_left_ventral_putamen', 'left_SMA-bin_left_dorsal_putamen', 'left_SMA-bin_left_accumbens_thr50', 
           'left_CMA-bin_left_ventral_putamen', 'left_CMA-bin_left_dorsal_putamen', 'left_CMA-bin_left_accumbens_thr50', 
           'left_precentral_gyrus_A4ul_thr25-bin_left_ventral_putamen', 'left_precentral_gyrus_A4ul_thr25-bin_left_dorsal_putamen', 'left_precentral_gyrus_A4ul_thr25-bin_left_accumbens_thr50']

filtered_df4 = df[df['Map-Mask'].isin(regions)]
filtered_df4 = filtered_df4.rename(columns={'Connectivity_Map': 'motorarea'})
filtered_df4 = filtered_df4.rename(columns={'Mask': 'putamen'})

# Initialize the plot
plt.figure(figsize=(25, 15))

# Create the bar plot with error bars
bar = sns.barplot(data=filtered_df4, x='motorarea', y='Mean_Connectivity_Value', hue='putamen', errorbar='se', palette=['gold', '#89CFF0', '#FF6F61'], capsize=.05, 
                  order=['left_CMA', 'left_SMA', 'left_precentral_gyrus_A4ul_thr25'])

bar.set_title('Cortical Motor Area-Striatum FC', fontsize=36)
bar.set_xlabel('Seed Region', fontsize=30)
bar.set_ylabel("Mean FC (Fisher's Z)", fontsize=30)
bar.set_ylim(0, 0.25)
bar.set_xticklabels(["CMA", "SMA", "M1$_{ul}$"])
bar.tick_params(axis='both', which='major', labelsize=26)

handles, labels = plt.gca().get_legend_handles_labels()
bar.legend(handles=handles, labels=['NAc','PUTd','PUTv'], loc='upper right', fontsize=22)

# Remove top and right spines
sns.despine()

# Add the posthoc test annotation
statannot.add_stat_annotation(plt.gca(),
                              data=filtered_df4, 
                              x='motorarea', 
                              y='Mean_Connectivity_Value', 
                              order=['left_CMA', 'left_SMA', 'left_precentral_gyrus_A4ul_thr25'],
                              hue='putamen',
                              box_pairs=[(('left_CMA', 'bin_left_accumbens_thr50'), ('left_CMA', 'bin_left_ventral_putamen')),
                                         (('left_CMA', 'bin_left_dorsal_putamen'), ('left_CMA', 'bin_left_ventral_putamen')),
                                         (('left_SMA', 'bin_left_accumbens_thr50'), ('left_SMA', 'bin_left_ventral_putamen')),
                                         (('left_SMA', 'bin_left_dorsal_putamen'), ('left_SMA', 'bin_left_ventral_putamen')),
                                         (('left_precentral_gyrus_A4ul_thr25', 'bin_left_accumbens_thr50'), ('left_precentral_gyrus_A4ul_thr25', 'bin_left_ventral_putamen')),
                                         (('left_precentral_gyrus_A4ul_thr25', 'bin_left_dorsal_putamen'), ('left_precentral_gyrus_A4ul_thr25', 'bin_left_ventral_putamen'))],
                              test='t-test_paired', 
                              text_format='star',
                              loc='inside', 
                              fontsize='26',
                              verbose=2)

bar.figure.savefig("/path/to/folder/put_fc_fig4.png", bbox_inches="tight",dpi=300)


