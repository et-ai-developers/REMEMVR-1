import os
import pandas as pd
import numpy as np
import json
from itertools import combinations

RAVLT_LIST_A = ['Drum', 'Curtain', 'Bell', 'Coffee', 'School', 'Parent', 'Moon', 'Garden', 'Hat', 'Farmer', 'Nose', 'Turkey', 'Color', 'House', 'River']
RAVLT_LIST_B = ['Desk', 'Ranger', 'Bird', 'Shoe', 'Stove', 'Mountain', 'Glasses', 'Towel', 'Cloud', 'Boat', 'Lamb', 'Gun', 'Pencil', 'Church', 'Fish']
    

def ravlt_word_clusters(dfMaster, dfData):

    def get_word_cluster_df(dfMaster):
        # Only keep the rows that have '-COG-X-RAV-' in the name in column 0
        dfRavlt = dfMaster[dfMaster.iloc[:, 0].str.contains('-COG-X-RAV-', na=False)].reset_index(drop=True)

        # Get a list of the remaining variables
        variable_list = dfRavlt.iloc[:, 0].tolist()
        variable_list = [x.split('-')[-1] for x in variable_list]

        # Only keen the columns that contain the data and remove the ones with tags
        dfRavlt = dfRavlt.iloc[:, 1::2].reset_index(drop=True)

        # Remove the -D from the end of the column names
        dfRavlt.columns = dfRavlt.columns.str.replace('-D', '')

        # Transpose the dataframe so that the variables are the columns
        dfRavlt = dfRavlt.T
        dfRavlt.columns = variable_list

        # Turn the index into a column called PXID and insert it as the first column
        dfRavlt.insert(0, 'UID', dfRavlt.index)
        dfRavlt = dfRavlt.reset_index(drop=True)

        order_variables = ['UID']

        for trial in range(1, 9):
            for item in range(15):
                var = f"T{(trial * 100) + item + 1}"
                order_variables.append(var)

        dfRavltWordClusters_wide = dfRavlt[order_variables]

        dfRavltWordClusters = pd.DataFrame(columns=['UID', 'Trial'] + RAVLT_LIST_A)

        for trial in range(1, 9):
            
            df_temp = pd.DataFrame(columns=['UID', 'Trial'])
            df_temp['UID'] = dfRavltWordClusters_wide['UID']
            df_temp['Trial'] = trial

            for word in range(15):
                word_name = RAVLT_LIST_A[word]
                word_var = f"T{(trial * 100) + word + 1}"
                df_temp[word_name] = dfRavltWordClusters_wide[word_var]
            
            dfRavltWordClusters = pd.concat([dfRavltWordClusters, df_temp], ignore_index=True)

        # column_names = ['UID', 'Trial']
        # for i, word in enumerate(RAVLT_LIST_A):
        #     column_names.append(f"{i}_{word}")

        # dfRavltWordClusters.columns = column_names

        return dfRavltWordClusters.copy()

    def convert_words_orders_to_floats(dfRavltWordClusters):

        def normalize_row(row):
            """
            Normalizes the ordinal responses in a single row to a 0-1 scale.
            This version converts responses to numeric to avoid type errors.
            """
            # Determine the columns that contain ordinal responses.
            response_cols = row.index.difference(['UID', 'Trial'])
            
            # Convert responses to numeric (forcing non-numeric values to NaN).
            responses = row[response_cols].apply(lambda x: pd.to_numeric(x, errors='coerce'))
            
            # Filter out missing responses.
            valid_responses = responses.dropna()
            
            if valid_responses.empty:
                return row

            # Calculate the maximum ordinal value.
            max_ordinal = valid_responses.max()

            # Handle single response to avoid division by zero.
            if max_ordinal == 1:
                normalized = valid_responses.copy() * 0
            else:
                # Normalize using: (ordinal - 1) / (max_ordinal - 1)
                normalized = (valid_responses - 1) / (max_ordinal - 1)
            
            # Update row with normalized values.
            row.loc[normalized.index] = normalized
            return row
        
        df_normalized = dfRavltWordClusters.apply(normalize_row, axis=1)

        return df_normalized

    def look_for_patterns(dfRavltWordClusters):

        print(dfRavltWordClusters)

        pass

        # print(dfRavltWordClusters)

        # uid_list = dfRavltWordClusters['UID'].unique()

        # # Calculate the mean of each word for each participant
        # drum = dfRavltWordClusters['Drum'].mean()
        # print(f"Drum: {drum}")
 
    # dfZ = dfData[['UID', 'RAVLT_12345_z', 'RAVLT_dr_z', 'RAVLT_12345irdr_z', 'RAVLT_recpc_z']]

    # Remove duplicate rows
    # dfZ = dfZ.drop_duplicates(subset=['UID'])

    # dfZ.to_clipboard(index=False, header=True)

    dfRavltWordClusters = get_word_cluster_df(dfMaster)

    # dfRavltWordClusters = convert_words_orders_to_floats(dfRavltWordClusters)

    dfRavltWordClusters = look_for_patterns(dfRavltWordClusters)
    
    return dfData

def calculate_norms(dfData, recompute=True):

    def BVMT(dfData):
        
            # Create a column in the working dataframe for each BVMT Z score
        
        new_variable_list = ['BVMT_t1_z', 'BVMT_t2_z', 'BVMT_t3_z', 'BVMT_total_recall_z', 'BVMT_learning_z', 'BVMT_delayed_recall_z']

        for variable in new_variable_list:

                column_id = dfData.columns.get_loc(variable.replace("_z", "")) + 1
                dfData.insert(column_id, variable, None)
        
        # Load the BVMT T values
        with open("./cog/BVMT/BVMT_t_vals.json") as file:
            
            t_vals = json.load(file)
        
        # Iterate through each participant
        for i in range(len(dfData)):

            if dfData.loc[i, 'test'] == 1:
                
                # Load the variables for a single participant
                age = dfData.loc[i, 'age']
                t1 = int(dfData.loc[i, 'BVMT_t1'])
                t2 = int(dfData.loc[i, 'BVMT_t2'])
                t3 = int(dfData.loc[i, 'BVMT_t3'])
                total_recall = int(dfData.loc[i, 'BVMT_total_recall'])
                learning = int(dfData.loc[i, 'BVMT_learning'])
                delayed_recall = int(dfData.loc[i, 'BVMT_delayed_recall'])
                
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
                dfData.loc[i, 'BVMT_t1_z'] = round(t1_t,2)
                dfData.loc[i, 'BVMT_t2_z'] = round(t2_t,2)
                dfData.loc[i, 'BVMT_t3_z'] = round(t3_t,2)
                dfData.loc[i, 'BVMT_total_recall_z'] = round(total_recall_t,2)
                dfData.loc[i, 'BVMT_learning_z'] = round(learning_t,2)
                dfData.loc[i, 'BVMT_delayed_recall_z'] = round(delayed_recall_t,2)
                
            else:

                for variable in new_variable_list:
                    
                    dfData.loc[i, variable] = dfData.loc[i - 1, variable]
                
        return dfData

    def RPM(dfData):

        # Create new RPM_z column

        new_variable_list = ['RPM_score_z']

        for variable in new_variable_list:

            column_id = dfData.columns.get_loc(variable.replace("_z", "")) + 1
            dfData.insert(column_id, variable, None)

        for i in range(len(dfData)):

            if dfData.loc[i, 'test'] == 1:

                age = dfData.loc[i, 'age']
                rpm_score = dfData.loc[i, 'RPM_score']
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

                dfData.loc[i, 'RPM_score_z'] = round(rpm_z,2)

            else:
                    
                dfData.loc[i, 'RPM_score_z'] = dfData.loc[i - 1, 'RPM_score_z']

        return dfData   

    def RAVLT(dfData):

        # Create new RAVLT_z columns

        new_variable_list = ['RAVLT_12345_z', 'RAVLT_dr_z', 'RAVLT_12345irdr_z', 'RAVLT_recpc_z']
        column_id = dfData.columns.get_loc('RAVLT_miss') + 1

        for variable in new_variable_list:

            dfData.insert(column_id, variable, None)
            column_id += 1

        # Sourced from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7895855/

        SS_trial_12345_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 15, 15, 15, 15, 16, 16, 17, 17, 18, 18, 19, 20, 20, 20, 20, 20, 20, 20]

        SS_trial_d_list = [3, 4, 5, 6, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 15, 17]

        SS_trial_123456d_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 15, 15, 15, 15, 15, 16, 16, 16, 16, 17, 17, 17, 18, 19, 20, 20, 20, 20, 20, 20, 20, 20]

        SS_trial_recpc_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11, 11, 12, 12, 13, 14, 15]

        for i in range(len(dfData)):

            if dfData.loc[i, 'test'] == 1:

                age = dfData.loc[i, 'age']
                sex = dfData.loc[i, 'sex']
                education = dfData.loc[i, 'education'] + 11

                t1 = dfData.loc[i, 'RAVLT_t1']
                t2 = dfData.loc[i, 'RAVLT_t2']
                t3 = dfData.loc[i, 'RAVLT_t3']
                if t3 == 0:
                    t3 = t2
                t4 = dfData.loc[i, 'RAVLT_t4']
                if t4 == 0:
                    t4 = t3
                t5 = dfData.loc[i, 'RAVLT_t5']
                if t5 == 0:
                    t5 = t4
                t6 = dfData.loc[i, 'RAVLT_lb']
                t7 = dfData.loc[i, 'RAVLT_ir']
                t8 = dfData.loc[i, 'RAVLT_dr']
                rh = dfData.loc[i, 'RAVLT_hit']
                rfa = dfData.loc[i, 'RAVLT_miss']

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

                dfData.loc[i, 'RAVLT_12345_z'] = round((t12345_t - 50) / 10, 2)
                dfData.loc[i, 'RAVLT_dr_z'] = round((t_d_t - 50) / 10, 2)
                dfData.loc[i, 'RAVLT_12345irdr_z'] = round((t123456d_t - 50) / 10, 2)
                dfData.loc[i, 'RAVLT_recpc_z'] = round((recpc_t - 50) / 10, 2)

            else:
                
                for variable in new_variable_list:
                    
                    dfData.loc[i, variable] = dfData.loc[i - 1, variable]

        return dfData

    def NART(dfData):

        # Create new NART_z column
        column_id = dfData.columns.get_loc('NART_score') + 1
        dfData.insert(column_id, 'NART_score_z', None)

        iq_list = [55.97,57.28,58.58,59.89,61.19,62.5,63.81,65.11,66.42,67.72,69.03,70.34,71.64,72.95,74.25,75.56,76.87,78.17,79.48,80.78,82.09,83.4,84.7,86.01,87.31,88.62,89.93,91.23,92.54,93.84,95.15,96.46,97.76,99.07,100.37,101.68,102.9,104.29,105.6,106.9,108.21,109.52,110.82,112.13,113.43,114.74,116.05,117.35,118.66,119.96,121.27]    
        # Retrieved from https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4547520/

        for i in range(len(dfData)):

            if dfData.loc[i, 'test'] == 1:

                nart_score = dfData.loc[i, 'NART_score']
                
                try:
                    nart_score = int(nart_score)
                    nart_z = round((iq_list[int(nart_score)] - 100) / 15, 2)

                except:
                
                    nart_z = np.nan
            
                dfData.loc[i, 'NART_score_z'] = nart_z

            else:

                dfData.loc[i, 'NART_score_z'] = dfData.loc[i - 1, 'NART_score_z']

        return dfData

    print("\n-- Cognitive Test Norms --\n")

    if os.path.exists('./data/cache/norms.db') and recompute == False:

        print("Cached Version Found")

        dfData = pd.read_pickle('./data/cache/norms.db')

        print("Norms Loaded")

    else:

        print("Cached Version Not Found\nRecaclulating Norms")

        dfData = BVMT(dfData)
        dfData = RPM(dfData)
        dfData = RAVLT(dfData)
        dfData = NART(dfData)
        
        print("Creating New Cache")

        pd.to_pickle(dfData, "./data/cache/norms.db")
        
        print("Norms Loaded")

    return dfData


