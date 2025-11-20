import pandas as pd
import numpy as np
from scipy.stats import ttest_ind_from_stats
from math import log10
import json
from scipy.stats import shapiro

def BVMT(working_df):
    
    # print("\n - Starting BVMT Norms Analysis -\n")

    # Create a column in the working dataframe for each BVMT Z score
    working_df['BVMT_t1_z'] = None
    working_df['BVMT_t2_z'] = None
    working_df['BVMT_t3_z'] = None
    working_df['BVMT_total_recall_z'] = None
    working_df['BVMT_learning_z'] = None
    working_df['BVMT_delayed_recall_z'] = None
    working_df['BVMT_mean_z'] = None
    working_df['BVMT_stdev_z'] = None

    # Load the BVMT T values
    with open("cogtests/BVMT_t_vals.json") as file:
        
        t_vals = json.load(file)
    
    # Iterate through each participant
    for i in range(len(working_df)):

        # Load the variables for a single participant
        age = working_df.loc[i, 'age']
        t1 = int(working_df.loc[i, 'BVMT_t1'])
        t2 = int(working_df.loc[i, 'BVMT_t2'])
        t3 = int(working_df.loc[i, 'BVMT_t3'])
        total_recall = int(working_df.loc[i, 'BVMT_total_recall'])
        learning = int(working_df.loc[i, 'BVMT_learning'])
        delayed_recall = int(working_df.loc[i, 'BVMT_delayed_recall'])
        
        # Calculate which group from the norms the participant falls into
        age_means = []
       
        for entry in t_vals:
        
            age_means.append(int(entry['age_mean']))

        differences = [abs(x - age) for x in age_means]
        closest_index = differences.index(min(differences))

        # Find the T scores for each test, convert to z-scores, and add to the dataframe
        # Note: BVMT T-scores have a mean of 50 and a standard deviation of 10
        t1_t = (t_vals[closest_index]['trial_1'][t1] - 50) / 10
        t2_t = (t_vals[closest_index]['trial_2'][t2] - 50) / 10
        t3_t = (t_vals[closest_index]['trial_3'][t3] - 50) / 10
        total_recall_t = (t_vals[closest_index]['total_recall'][total_recall] - 50) / 10
        learning_t = (t_vals[closest_index]['learning'][learning] - 50) / 10
        delayed_recall_t = (t_vals[closest_index]['delayed_recall'][delayed_recall] - 50) / 10

        # Add these z-scores to the new dataframe columns
        working_df.loc[i, 'BVMT_t1_z'] = round(t1_t,2)
        working_df.loc[i, 'BVMT_t2_z'] = round(t2_t,2)
        working_df.loc[i, 'BVMT_t3_z'] = round(t3_t,2)
        working_df.loc[i, 'BVMT_total_recall_z'] = round(total_recall_t,2)
        working_df.loc[i, 'BVMT_learning_z'] = round(learning_t,2)
        working_df.loc[i, 'BVMT_delayed_recall_z'] = round(delayed_recall_t,2)
        working_df.loc[i, 'BVMT_mean_z'] = round(np.mean([t1_t, t2_t, t3_t, total_recall_t, learning_t, delayed_recall_t]),2)
        working_df.loc[i, 'BVMT_stdev_z'] = round(np.std([t1_t, t2_t, t3_t, total_recall_t, learning_t, delayed_recall_t]),2)
        
    # Return the working dataframe
    return working_df

def RPM(working_df):

    # Create new RPM_z column
    working_df['RPM_z'] = None

    for i in range(len(working_df)):
        age = working_df.loc[i, 'age']
        rpm_score = working_df.loc[i, 'RPM_score']
        if age >= 18 and age <= 34:
            # Values from https://bpspsychub.onlinelibrary.wiley.com/doi/10.1111/jnp.12308
            rpm_z = (rpm_score - 9.88) / 1.53
        elif age >= 35 and age <= 49:
            rpm_z = (rpm_score - 9.17) / 1.9
        elif age >= 50 and age <= 64:
            rpm_z = (rpm_score - 8.76) / 2.23
        elif age >= 65 and age <= 79:
            rpm_z = (rpm_score - 7.86) / 2.51
        elif age >= 80 and age <= 89:
            rpm_z = (rpm_score - 7.11) / 2.49
        else:
            rpm_z = np.nan

        working_df.loc[i, 'RPM_z'] = round(rpm_z,2)

    return working_df   

def RAVLT(working_df):

    # Create new RAVLT_z columns
    working_df['RAVLT_12345_z'] = None
    working_df['RAVLT_d_z'] = None
    working_df['RAVLT_123456d_z'] = None
    working_df['RAVLT_recpc_z'] = None

    # Sourced from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7895855/

    SS_trial_12345_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 16, 17, 17, 18, 18, 19, 20, 20, 20, 20, 20, 20, 20]

    SS_trial_d_list = [3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 17]

    SS_trial_123456d_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 18, 19, 20, 20, 20, 20, 20, 20, 20, 20]

    SS_trial_recpc_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11, 11, 12, 12, 13, 14, 15]

    for i in range(len(working_df)):

        age = working_df.loc[i, 'age']
        sex = working_df.loc[i, 'sex']
        education = working_df.loc[i, 'education'] + 11

        t1 = working_df.loc[i, 'RAVLT_1']
        t2 = working_df.loc[i, 'RAVLT_2']
        t3 = working_df.loc[i, 'RAVLT_3']
        if t3 == 0:
            t3 = t2
        t4 = working_df.loc[i, 'RAVLT_4']
        if t4 == 0:
            t4 = t3
        t5 = working_df.loc[i, 'RAVLT_5']
        if t5 == 0:
            t5 = t4
        t6 = working_df.loc[i, 'RAVLT_6']
        t7 = working_df.loc[i, 'RAVLT_7']
        t8 = working_df.loc[i, 'RAVLT_8']
        rh = working_df.loc[i, 'RAVLT_recognition_hits']
        rfa = working_df.loc[i, 'RAVLT_recognition_false_alarms']

        trial12345 = int(t1 + t2 + t3 + t4 + t5)
        trial_d = int(t8)
        trial123456d = int(t1 + t2 + t3 + t4 + t5 + t7 + t8)
        recpc = int(round((((rh + (15 - rfa)) / 30) * 100),0))

        # print(f"Trial 12345: {trial12345} | Trial D: {trial_d} | Trial 123456d: {trial123456d} | RecPC: {recpc}")

        AVLTSum5SS = SS_trial_12345_list[trial12345]
        AVDSS = SS_trial_d_list[trial_d]
        AVLTsum5p6DSS = SS_trial_123456d_list[trial123456d]
        AVRecPCSS = SS_trial_recpc_list[recpc]

        t12345_t = round(50 + ((((AVLTSum5SS - (10.2048820335 + (age * 0.0696731708) + (sex * 2.0691847063) + (education * 0.2076286782) + (age ** 2 * -0.0014410120))) / 1) + 0.0000000637336) / 0.23569807), 2)

        t_d_t = round(50 + ((((AVDSS - (12.4118437425 + (age * -0.0016432817) + (sex * 1.8612455591) + (education * 0.1380628944) + (age ** 2 * -0.0007027918))) / 1) + 0.0000001024411) / 0.25299505), 2)

        t123456d_t = round(50 + ((((AVLTsum5p6DSS - (10.8349191766 + (age * 0.0514562686) + (sex * 2.0670904968) + (education * 0.1915793153) + (age ** 2 * -0.0012694294))) / 1) - 0.0000001038205) / 0.23673872), 2)

        recpc_t = round(50 + ((((AVRecPCSS - (10.7915054797 + (age * 0.0163995950) + (sex * -1.8832719513) + (education * 0.1180746912) + (age ** 2 * -0.0005488200))) / 1) + 0.0000001925238) / 0.29155771), 2)

        working_df.loc[i, 'RAVLT_12345_z'] = round((t12345_t - 50) / 10, 2)
        working_df.loc[i, 'RAVLT_d_z'] = round((t_d_t - 50) / 10, 2)
        working_df.loc[i, 'RAVLT_123456d_z'] = round((t123456d_t - 50) / 10, 2)
        working_df.loc[i, 'RAVLT_recpc_z'] = round((recpc_t - 50) / 10, 2)

    return working_df

def NART(working_df):

    # Create new NART_z column
    working_df['NART_z'] = None

    iq_list = [55.97,57.28,58.58,59.89,61.19,62.5,63.81,65.11,66.42,67.72,69.03,70.34,71.64,72.95,74.25,75.56,76.87,78.17,79.48,80.78,82.09,83.4,84.7,86.01,87.31,88.62,89.93,91.23,92.54,93.84,95.15,96.46,97.76,99.07,100.37,101.68,102.9,104.29,105.6,106.9,108.21,109.52,110.82,112.13,113.43,114.74,116.05,117.35,118.66,119.96,121.27]    
    # Retrieved from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4547520/

    for i in range(len(working_df)):

        nart_score = working_df.loc[i, 'NART_score']
        
        try:
            nart_score = int(nart_score)
            nart_z = round((iq_list[int(nart_score)] - 100) / 15, 2)

        except:
        
            nart_z = np.nan
    
        working_df.loc[i, 'NART_z'] = nart_z

    return working_df

def norms(working_df):

    working_df

    working_df = BVMT(working_df)
    working_df = RPM(working_df)
    working_df = RAVLT(working_df)
    working_df = NART(working_df)
    # # print(working_df[['UID', 'NART_z']])
    # for column in working_df.columns:
    #     if column.endswith('_z'):
    #         data = working_df[column].dropna()
    #         stat, p = shapiro(data)
    #         stat = round(stat, 2)
    #         p = round(p, 4)
    #         print(f"{column} S = {stat} | p = {p}")

    return working_df


# Old stuff below


#     mean_iq = 0
#     count = 0

#     results = []
#     for px in working_df[working_df['test'] == 0].iterrows():
#         try:
#             nart_score = int(px[1]['NART_score'])
#             iq = iq_list[nart_score]
#         except:
#             iq = "ERROR"
        
#         result = {
#             'UID': px[1]['UID'],
#             'AGE': px[1]['age'],
#             'NAR': px[1]['NART_score'],
#             'NIQ': iq,
#             'RPM': px[1]['RPM_score'],
#             'RAV': px[1]['RAVLT_12345678'],
#             'BVM': px[1]['BVMT_total_recall']
#         }
#         results.append(result)

#     output_df = pd.DataFrame(results)
#     output_df.to_excel("output.xlsx", index=False)



    # ravlt_df = pd.read_excel("cogtests/RAVLT_norms.xlsx", sheet_name="analysis")

    # group_list = ["30-39","40-49","50-59","60-69"]
    # age_low_list = [30,40,50,60]
    # age_high_list = [39,49,59,70]

    # for i in range(len(group_list)):
    #     n = 0
    #     age_list = []
    #     gender_list = []
    #     education_list = []
    #     t12345_list = []
    #     t8_list = []
    #     t1234578_list = []
    #     percent_recog_list = []
    #     t1_list = []
    #     t2_list = []
    #     t3_list = []
    #     t4_list = []
    #     t5_list = []
    #     t123_list = []
    #     t6_list = []
    #     t7_list = []
    #     short_term_retention_percentage_list = []
    #     long_term_retention_percentage_list = []
    #     memory_efficiency_score_list = []
    #     for px in working_df[working_df['test'] == 0].iterrows():
    #         if px[1]['age'] >= age_low_list[i] and px[1]['age'] <= age_high_list[i]:

    #             t1 = px[1]['RAVLT_1']
    #             t2 = px[1]['RAVLT_2']
    #             t3 = px[1]['RAVLT_3']
    #             if t3 == 0:
    #                 t3 = t2
    #             t4 = px[1]['RAVLT_4']
    #             if t4 == 0:
    #                 t4 = t3
    #             t5 = px[1]['RAVLT_5']
    #             if t5 == 0:
    #                 t5 = t4

    #             t6 = px[1]['RAVLT_6']
    #             t7 = px[1]['RAVLT_7']
    #             t8 = px[1]['RAVLT_8']
    #             rh = px[1]['RAVLT_recognition_hits']
    #             rfa = px[1]['RAVLT_recognition_false_alarms']

    #             n += 1
    #             age_list.append(px[1]['age'])
    #             gender_list.append(px[1]['sex'])
    #             education_list.append(px[1]['education'])

    #             t12345_list.append(t1 + t2 + t3 + t4 + t5)
    #             t8_list.append(t8)
    #             t1234578_list.append(t1 + t2 + t3 + t4 + t5 + t7 + t8)

    #             percent_recog_list.append(
    #                 (((rh + (15 - rfa)) / 30) * 100)
    #             )
                
    #             t1_list.append(t1)
    #             t2_list.append(t2)
    #             t3_list.append(t3)
    #             t4_list.append(t4)
    #             t5_list.append(t5)
    #             t123_list.append(t1 + t2 + t3)
    #             t6_list.append(t6)
    #             t7_list.append(t7)

    #             short_term_retention_percentage_list.append(
    #                 100 * (t7 / t5)
    #             )
                
    #             long_term_retention_percentage_list.append(
    #                 100 * (t8 / t5)
    #             )
                
    #             memory_efficiency_score_list.append(
    #                 (((t8 / 15) / ((t1 + t2 + t3 + t4 + t5) / 75)) + ((rh / 15) - (rfa / 15)))
    #             )

    #     age_m = round(np.mean(age_list),2)
    #     age_sd = round(np.std(age_list),2)
    #     percent_male = round(np.mean(gender_list),2) * 100
    #     education_m = round(np.mean(education_list),2)
    #     education_sd = round(np.std(education_list),2)
    #     t12345_m = round(np.mean(t12345_list),2)
    #     t12345_sd = round(np.std(t12345_list),2)
    #     t8_m = round(np.mean(t8_list),2)
    #     t8_sd = round(np.std(t8_list),2)
    #     t1234578_m = round(np.mean(t1234578_list),2)
    #     t1234578_sd = round(np.std(t1234578_list),2)
    #     percent_recog_m = round(np.mean(percent_recog_list),2)
    #     percent_recog_sd = round(np.std(percent_recog_list),2)
    #     t1_m = round(np.mean(t1_list),2)
    #     t1_sd = round(np.std(t1_list),2)
    #     t2_m = round(np.mean(t2_list),2)
    #     t2_sd = round(np.std(t2_list),2)
    #     t3_m = round(np.mean(t3_list),2)
    #     t3_sd = round(np.std(t3_list),2)
    #     t4_m = round(np.mean(t4_list),2)
    #     t4_sd = round(np.std(t4_list),2)
    #     t5_m = round(np.mean(t5_list),2)
    #     t5_sd = round(np.std(t5_list),2)
    #     t123_m = round(np.mean(t123_list),2)
    #     t123_sd = round(np.std(t123_list),2)
    #     t6_m = round(np.mean(t6_list),2)
    #     t6_sd = round(np.std(t6_list),2)
    #     t7_m = round(np.mean(t7_list),2)
    #     t7_sd = round(np.std(t7_list),2)
    #     short_term_retention_percentage_m = round(np.mean(short_term_retention_percentage_list),2)
    #     short_term_retention_percentage_sd = round(np.std(short_term_retention_percentage_list),2)
    #     long_term_retention_percentage_m = round(np.mean(long_term_retention_percentage_list),2)
    #     long_term_retention_percentage_sd = round(np.std(long_term_retention_percentage_list),2)
    #     memory_efficiency_score_m = round(np.mean(memory_efficiency_score_list),2)
    #     memory_efficiency_score_sd = round(np.std(memory_efficiency_score_list),2)

    #     ravlt_df.iloc[(i * 8) + 3, 2] = n
    #     ravlt_df.iloc[(i * 8) + 3, 3] = n
    #     ravlt_df.iloc[(i * 8) + 3, 4] = n
    #     ravlt_df.iloc[(i * 8) + 3, 5] = n
    #     ravlt_df.iloc[(i * 8) + 3, 6] = n
    #     ravlt_df.iloc[(i * 8) + 3, 7] = n
    #     ravlt_df.iloc[(i * 8) + 3, 8] = n
    #     ravlt_df.iloc[(i * 8) + 3, 9] = n
    #     ravlt_df.iloc[(i * 8) + 3, 10] = n
    #     ravlt_df.iloc[(i * 8) + 3, 11] = n
    #     ravlt_df.iloc[(i * 8) + 3, 12] = n
    #     ravlt_df.iloc[(i * 8) + 3, 13] = n
    #     ravlt_df.iloc[(i * 8) + 3, 14] = n
    #     ravlt_df.iloc[(i * 8) + 3, 15] = n
    #     ravlt_df.iloc[(i * 8) + 3, 16] = n
    #     ravlt_df.iloc[(i * 8) + 3, 17] = n
    #     ravlt_df.iloc[(i * 8) + 3, 18] = n

    #     ravlt_df.iloc[(i * 8) + 4, 2] = age_m
    #     ravlt_df.iloc[(i * 8) + 4, 3] = education_m
    #     ravlt_df.iloc[(i * 8) + 4, 4] = t12345_m
    #     ravlt_df.iloc[(i * 8) + 4, 5] = t8_m
    #     ravlt_df.iloc[(i * 8) + 4, 6] = t1234578_m
    #     ravlt_df.iloc[(i * 8) + 4, 7] = percent_recog_m
    #     ravlt_df.iloc[(i * 8) + 4, 8] = t1_m
    #     ravlt_df.iloc[(i * 8) + 4, 9] = t2_m
    #     ravlt_df.iloc[(i * 8) + 4, 10] = t3_m
    #     ravlt_df.iloc[(i * 8) + 4, 11] = t4_m
    #     ravlt_df.iloc[(i * 8) + 4, 12] = t5_m
    #     ravlt_df.iloc[(i * 8) + 4, 13] = t123_m
    #     ravlt_df.iloc[(i * 8) + 4, 14] = t6_m
    #     ravlt_df.iloc[(i * 8) + 4, 15] = t7_m
    #     ravlt_df.iloc[(i * 8) + 4, 16] = short_term_retention_percentage_m
    #     ravlt_df.iloc[(i * 8) + 4, 17] = long_term_retention_percentage_m
    #     ravlt_df.iloc[(i * 8) + 4, 18] = memory_efficiency_score_m

    #     ravlt_df.iloc[(i * 8) + 5, 2] = age_sd
    #     ravlt_df.iloc[(i * 8) + 5, 3] = education_sd
    #     ravlt_df.iloc[(i * 8) + 5, 4] = t12345_sd
    #     ravlt_df.iloc[(i * 8) + 5, 5] = t8_sd
    #     ravlt_df.iloc[(i * 8) + 5, 6] = t1234578_sd
    #     ravlt_df.iloc[(i * 8) + 5, 7] = percent_recog_sd
    #     ravlt_df.iloc[(i * 8) + 5, 8] = t1_sd
    #     ravlt_df.iloc[(i * 8) + 5, 9] = t2_sd
    #     ravlt_df.iloc[(i * 8) + 5, 10] = t3_sd
    #     ravlt_df.iloc[(i * 8) + 5, 11] = t4_sd
    #     ravlt_df.iloc[(i * 8) + 5, 12] = t5_sd
    #     ravlt_df.iloc[(i * 8) + 5, 13] = t123_sd
    #     ravlt_df.iloc[(i * 8) + 5, 14] = t6_sd
    #     ravlt_df.iloc[(i * 8) + 5, 15] = t7_sd
    #     ravlt_df.iloc[(i * 8) + 5, 16] = short_term_retention_percentage_sd
    #     ravlt_df.iloc[(i * 8) + 5, 17] = long_term_retention_percentage_sd
    #     ravlt_df.iloc[(i * 8) + 5, 18] = memory_efficiency_score_sd

    # print(ravlt_df)

    # for i in range(len(group_list)):
    #     for j in range(17):
    #         norm_n = ravlt_df.iloc[(i * 8) + 0, j + 2]
    #         norm_m = ravlt_df.iloc[(i * 8) + 1, j + 2]
    #         norm_sd = ravlt_df.iloc[(i * 8) + 2, j + 2]

    #         data_n = ravlt_df.iloc[(i * 8) + 3, j + 2]
    #         data_m = ravlt_df.iloc[(i * 8) + 4, j + 2]
    #         data_sd = ravlt_df.iloc[(i * 8) + 5, j + 2]

            
    #         try:
    #             t, p = ttest_ind_from_stats(mean1=data_m, std1=data_sd, nobs1=data_n, mean2=norm_m, std2=norm_sd, nobs2=norm_n, equal_var=False)
    #         except:
    #             print("ERROR")
    #             print(f"Age: {group_list[i]} | Variable: {ravlt_df.columns[j + 1]} | Norm N: {norm_n} | Norm M: {norm_m} | Norm SD: {norm_sd} | Data N: {data_n} | Data M: {data_m} | Data SD: {data_sd}")
    #         t = round(t, 2)
    #         p = round(p, 4)
    #         ravlt_df.iloc[(i * 8) + 6, j + 2] = t
    #         ravlt_df.iloc[(i * 8) + 7, j + 2] = p

    # print(ravlt_df)
    # ravlt_df.to_excel("output.xlsx", index=False)


    # rpm_norms = pd.read_excel("cogtests/RPM_norms.xlsx", sheet_name="norms")
    # rpm_data = pd.read_excel("cogtests/RPM_norms.xlsx", sheet_name="data")

    # for i in range(len(rpm_norms)):
    #     age_t, age_p = ttest_ind_from_stats(mean1=rpm_data.loc[i, 'age_m'], std1=rpm_data.loc[i, 'age_sd'], nobs1=rpm_data.loc[i, 'n'], mean2=rpm_norms.loc[i, 'age_m'], std2=rpm_norms.loc[i, 'age_sd'], nobs2=rpm_norms.loc[i, 'n'], equal_var=False)
    #     rpm_t, rpm_p = ttest_ind_from_stats(mean1=rpm_data.loc[i, 'rpm_m'], std1=rpm_data.loc[i, 'rpm_sd'], nobs1=rpm_data.loc[i, 'n'], mean2=rpm_norms.loc[i, 'rpm_m'], std2=rpm_norms.loc[i, 'rpm_sd'], nobs2=rpm_norms.loc[i, 'n'], equal_var=False)
    #     age_t = round(age_t, 2)
    #     age_p = round(age_p, 4)
    #     rpm_t = round(rpm_t, 2)
    #     rpm_p = round(rpm_p, 4)
    #     print(f"Age: {rpm_norms.loc[i, 'age_group']} | Age t: {age_t} | Age p: {age_p} | RPM t: {rpm_t} | RPM p: {rpm_p}")

    # for row in rpm_norms.iterrows():
    #     print(row[1]['age_group'])
    #     ages = [] 
    #     rpm_scores = []
        
    #     for px in working_df[working_df['test'] == 0].iterrows():
        
    #         if px[1]['age'] >= row[1]['age_low'] and px[1]['age'] <= row[1]['age_high']:
        
    #             age_temp = px[1]['age']
    #             ages.append(age_temp)

    #             rpm_key = [8,4,5,1,2,5,6,3,7,8,7,6]
    #             rpm_responses = [int(px[1]['RPM_1']),int(px[1]['RPM_2']),int(px[1]['RPM_3']),int(px[1]['RPM_4']),int(px[1]['RPM_5']),int(px[1]['RPM_6']),int(px[1]['RPM_7']),int(px[1]['RPM_8']),int(px[1]['RPM_9']),int(px[1]['RPM_10']),int(px[1]['RPM_11']),int(px[1]['RPM_12'])]
    #             rpm_score = 0

    #             for i in range(12):
    #                 if rpm_responses[i] == rpm_key[i]:
    #                     rpm_score += 1

    #             rpm_scores.append(rpm_score)

    #     num = len(ages)

    #     ages_mean = round(np.mean(ages),2)
    #     ages_sd = round(np.std(ages),2)

    #     rpm_scores_mean = round(np.mean(rpm_scores),2)
    #     rpm_scores_sd = round(np.std(rpm_scores),2)

    #     print(f"N = {num}, Mean Age: {ages_mean} | SD Age: {ages_sd} | Mean RPM: {rpm_scores_mean} | SD RPM: {rpm_scores_sd}")


# def BVMT2(working_df):
#     print("\n - Starting BVMT Norms Analysis -\n")
#     # Load the norms
#     norms_m = pd.read_excel("cogtests/BVMT_norms.xlsx", sheet_name="norms_m")
#     norms_sd = pd.read_excel("cogtests/BVMT_norms.xlsx", sheet_name="norms_sd")
#     data_m = pd.read_excel("cogtests/BVMT_norms.xlsx", sheet_name="data_m")
#     data_sd = pd.read_excel("cogtests/BVMT_norms.xlsx", sheet_name="data_sd")

#     for i in range(len(norms_m)):

#         age_low = norms_m.loc[i, "age_low"]
#         age_high = norms_m.loc[i, "age_high"]
#         temp_df = pd.DataFrame(columns=['age','n','BVMT_t1','BVMT_t2','BVMT_t3','BVMT_total_recall','BVMT_learning','BVMT_delayed_recall','BVMT_percent_retained','BVMT_hits','BVMT_false_alarms','BVMT_discrimination_index','BVMT_response_bias'])
#         variables = temp_df.columns
#         count = 0
#         for px in working_df[working_df['test'] == 0].iterrows(): 
#             if px[1]['age'] >= age_low and px[1]['age'] <= age_high:
#                 count += 1
#                 for var in variables:
#                     if var == 'n':
#                         pass
#                     else:
#                         temp_df.loc[count, var] = px[1][var]
#                     # temp_df.loc[count, var] = px[1][var]
#         mean_values = temp_df.mean()
#         stdev_values = temp_df.std()
#         mean_df = mean_values.to_frame().transpose()
#         stdev_df = stdev_values.to_frame().transpose()
#         for var in variables:
#             if var == 'n':
#                 data_m.loc[i, var] = count
#                 data_sd.loc[i, var] = count
#             else:
#                 data_m.loc[i, var] = mean_df[var][0]
#                 data_sd.loc[i, var] = stdev_df[var][0]
                
#     variables = norms_m.columns
#     results_df = pd.DataFrame(columns=['age_low','age_high','variable','norm_m','norm_sd','norm_n','data_m','data_sd','data_n','t','p','x'])
#     for i in range(len(norms_m)):     
#         for var in variables:
#             if var == 'age_low' or var == 'age_high' or var == 'n':
#                 pass
#             else:
#                 t, p = ttest_ind_from_stats(mean1=data_m.loc[i, var], std1=data_sd.loc[i, var], nobs1=data_m.loc[i, 'n'], mean2=norms_m.loc[i, var], std2=norms_sd.loc[i, var], nobs2=norms_m.loc[i, 'n'], equal_var=False)
#                 # t = round(t, 2)
#                 # p = round(p, 4)

#                 new_row = {'age_low': norms_m.loc[i,'age_low'], 'age_high': norms_m.loc[i,'age_high'], 'variable': var, 'norm_m': norms_m.loc[i, var], 'norm_sd': norms_sd.loc[i, var], 'norm_n': norms_m.loc[i, 'n'], 'data_m': data_m.loc[i, var], 'data_sd': data_sd.loc[i, var], 'data_n': data_m.loc[i, 'n'], 't': t, 'p': p}
#                 results_df = pd.concat([results_df, pd.DataFrame(new_row, index=[0])], ignore_index=True)

#     for i in range(len(results_df)):

#         s_pooled = np.sqrt(((results_df.loc[i, 'norm_n'] - 1) * results_df.loc[i, 'norm_sd'] ** 2 + (results_df.loc[i, 'data_n'] - 1) * results_df.loc[i, 'data_sd'] ** 2) / (results_df.loc[i, 'norm_n'] + results_df.loc[i, 'data_n'] - 2))
#         cohens_d = (results_df.loc[i, 'norm_m'] - results_df.loc[i, 'data_m']) / s_pooled       
#         metric_x = cohens_d * (-log10(results_df.loc[i, 'p'])) * -1

#         results_df.loc[i, 'x'] = metric_x

#     results_df.to_excel("cogtests/BVMT_metric_x.xlsx", sheet_name='output', index=False) 


# def BVMT_create_t_values_json():
    
#     age_groups = ["18-22","20-24","22-26","24-28","26-30","28-32","30-34","32-36","34-38","36-40","38-42","40-44","42-46","44-48","46-50","48-52","50-54","52-56","54-58","56-60","58-62","60-64","62-66","64-68","66-70","68-72","70-74","72-79"]
#     variable_names = ["trial_1", "trial_2",	"trial_3", "total_recall", "learning","delayed_recall"]
    
#     t_vals_json = []

#     for group in age_groups:

#         group_df = pd.read_excel("cogtests/BVMT_t_norms.xlsx", sheet_name=group)

#         trial_1_t = [0,1,2,3,4,5,6,7,8,9,10,11,12]
#         trial_2_t = [0,1,2,3,4,5,6,7,8,9,10,11,12]
#         trial_3_t = [0,1,2,3,4,5,6,7,8,9,10,11,12]
#         total_recall_t = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]
#         learning_t = [0,1,2,3,4,5,6,7,8,9,10,11,12]
#         delayed_recall_t = [0,1,2,3,4,5,6,7,8,9,10,11,12]

#         for row in group_df.iterrows():

#             t_score = row[1]['t_score']

#             for var in variable_names:
#                 value = row[1][var]
#                 values = []
#                 try:
#                     values.append(int(value))
#                 except:
#                     try:
#                         value_range = value.split("-")
#                         for i in range(int(value_range[0]), int(value_range[1])+1):
#                             values.append(i)
#                     except:
#                         pass

#                 if len(values) > 0:
#                     for val in values:
#                         if var == "trial_1":
#                             trial_1_t[val] = t_score
#                         if var == "trial_2":
#                             trial_2_t[val] = t_score
#                         if var == "trial_3":
#                             trial_3_t[val] = t_score
#                         if var == "total_recall":
#                             total_recall_t[val] = t_score
#                         if var == "learning":
#                             learning_t[val] = t_score
#                         if var == "delayed_recall":
#                             delayed_recall_t[val] = t_score

#         json_entry = {
#             "group": group,
#             "trial_1": trial_1_t,
#             "trial_2": trial_2_t,
#             "trial_3": trial_3_t,
#             "total_recall": total_recall_t,
#             "learning": learning_t,
#             "delayed_recall": delayed_recall_t
#         }

#         t_vals_json.append(json_entry)
        
#     with open("cogtests/BVMT_t_vals.json", "w") as file:
#         json.dump(t_vals_json, file, indent=4)