# =============================================================================
# tools.py - Data Preparation Utilities
# =============================================================================
# This script contains helper functions dedicated to cleaning, filtering, and
# reshaping the raw data into the specific formats required for the analysis.
# Keeping these functions separate makes the main script cleaner and more focused.

import pandas as pd
import numpy as np

def calculateDays(dfData):
    """
    Robustly calculates the number of days from the first session for each participant.

    STATISTICAL NOTE: This converts the test numbers (1, 2, 3, 4) into a
    meaningful continuous variable representing the passage of time. Using the
    actual number of days is more precise than using the ordinal test number.
    It uses groupby() to operate on each participant independently, which is
    robust to missing data or incorrect sorting.
    """
    # Ensure the date column is in a datetime format pandas can understand
    dfData['Time_Date'] = pd.to_datetime(dfData['Time_Date'], errors='coerce')
    all_days = []
    
    for uid, group in dfData.groupby('UID'):
        # Find the date of the very first test session for this participant
        first_test = group[group['test'] == 1].dropna(subset=['Time_Date'])
        if not first_test.empty:
            first_date = first_test['Time_Date'].iloc[0]
            # Make an explicit copy to avoid SettingWithCopyWarning
            group_copy = group.copy()
            # Calculate the difference in days from that first session
            group_copy['time_day'] = (group_copy['Time_Date'] - first_date).dt.days
            all_days.append(group_copy)
            
    return pd.concat(all_days).sort_index() if all_days else pd.DataFrame()

def select_px(df, exclude_uids=[], age_range=[0, 100]):
    """
    Filters the main DataFrame by participant UID and age range based on parameters
    defined in the main script.
    """
    if 'UID' not in df.columns or 'age' not in df.columns:
        raise ValueError("DataFrame must contain 'UID' and 'age' columns.")

    filtered_df = df[~df['UID'].isin(exclude_uids)]
    filtered_df = filtered_df[(filtered_df['age'] >= age_range[0]) & (filtered_df['age'] <= age_range[1])]

    if filtered_df.empty:
        raise ValueError(f"No participants found in the age range {age_range[0]}-{age_range[1]} after exclusions.")
    
    # Return an explicit copy to prevent pandas' SettingWithCopyWarning in downstream steps.
    return filtered_df.copy()

def select_data(df, tests=[1, 2, 3, 4], all_tags=[], groups={}, categories={}, specify_room=False):
    """
    Selects the relevant item columns and reshapes the data from a wide format
    (one row per test) into the "long" format (one row per item response)
    required for the analysis.
    """

    # ============================ CORRECTED RESCORING LOGIC ===========================
    # Find all columns that represent the items to be rescored.
    # These are columns whose names contain both 'TQ_' and '-N-'.
    rescore_cols = [col for col in df.columns if 'TQ_' in col and '-N-' in col]
    # Loop through each of these columns and apply the rescoring logic.
    for col in rescore_cols:
        # For the current column, find all rows where the value is 0.5 and set them to 0.
        df.loc[df[col] == 0.5, col] = 0
    
    if len(categories) == 3:
        rescore_cols = [col for col in df.columns if 'TQ_' in col and '-L-' in col]
        # Loop through each of these columns and apply the rescoring logic.
        for col in rescore_cols:
            # For the current column, find all rows where the value is 0.5 and set them to 0.
            df.loc[df[col] == 0.5, col] = 0
        rescore_cols = [col for col in df.columns if 'TQ_' in col and '-U-' in col]
        # Loop through each of these columns and apply the rescoring logic.
        for col in rescore_cols:
            # For the current column, find all rows where the value is 0.5 and set them to 0.
            df.loc[df[col] == 0.5, col] = 0
        rescore_cols = [col for col in df.columns if 'TQ_' in col and '-D-' in col]
        # Loop through each of these columns and apply the rescoring logic.
        for col in rescore_cols:
            # For the current column, find all rows where the value is 0.5 and set them to 0.
            df.loc[df[col] == 0.5, col] = 0

    
    # ==================================================================================

    # Create an explicit copy after filtering to avoid the warning
    df_filtered = df[df['test'].isin(tests)].copy()
    
    items_summary = {}

    # Use a set for efficiency to find the unique item tags to include
    tags_to_include = set()
    for group_name, regex_list in groups.items():
        items_summary[group_name] = {
            'initial': 0,
        }
        for regex in regex_list:
            for tag in all_tags:
                if regex in tag:
                    tags_to_include.add(tag)
                    if specify_room:
                        items_summary[group_name]['initial'] += 4 # Assuming each tag has 4 items
                    else:
                        items_summary[group_name]['initial'] += 1
    
    required_cols = ['UID', 'test', 'VR_room'] + list(tags_to_include)
    existing_cols = [col for col in required_cols if col in df_filtered.columns]
    df_filtered = df_filtered[existing_cols]
    
    if 'UID' not in df_filtered.columns or 'test' not in df_filtered.columns:
        raise ValueError("Essential columns 'UID' or 'test' are missing after filtering.")
    
    # The 'melt' function is the key operation that transforms the data from wide to long format.
    df_long = df_filtered.melt(
        id_vars=['UID', 'test', 'VR_room'], 
        var_name='item_name', 
        value_name='score'
    )
    
    # Create a globally unique ID for each item.
    if specify_room:
        df_long['item_name'] = df_long['VR_room'] + '_' + df_long['item_name']
    
    df_long.drop(columns=['VR_room'], inplace=True)
    
    if not categories:
        print("No categories specified, using default binary scoring.")
        df_long['score'] = df_long['score'].apply(lambda x: 1 if x >= 1 else 0)
    else:
        print(f"Applying polytomous scoring with {len(categories)} categories.")
        
        # Create a list of conditions and a corresponding list of choices
        conditions = [
            (df_long['score'] >= range_min) & (df_long['score'] <= range_max)
            for new_score, [range_min, range_max] in categories.items()
        ]
        choices = [int(new_score) for new_score in categories.keys()]
        
        # Apply all conditions at once. The `default` value is used if no condition is met.
        df_long['score'] = np.select(conditions, choices, default=np.nan)

    return df_long, items_summary

def remove_invariant_items(df_irt, min_prop=0.05):
    """
    Removes items that have essentially no variance—that is, where one
    response category accounts for >= (1 - min_prop) of all responses.

    Parameters
    ----------
    df_irt : pd.DataFrame
        A long-form table with columns ['item_name', 'score', ...].
    min_prop : float, optional
        The minimum proportion of responses that must fall outside the
        largest category for an item to be retained.  Defaults to 0.05
        (i.e. we remove items with ≥95% in one category).

    Returns
    -------
    pd.DataFrame
        A filtered version of `df_irt` with those uninformative items removed.
    """
    if 'item_name' not in df_irt.columns or 'score' not in df_irt.columns:
        return df_irt

    print(f"Checking for uninformative items in {len(df_irt)} responses (min_prop={min_prop})...")

    to_drop = []
    # for each item, look at the distribution of scores
    for item, grp in df_irt.groupby('item_name'):
        props = grp['score'].value_counts(normalize=True)
        if props.max() >= 1.0 - min_prop:
            to_drop.append(item)

    if to_drop:
        pct = (1.0 - min_prop) * 100
        print(
            f"Removing {len(to_drop)} items with ≥{pct:.0f}% of responses in one category:\n"
            f"{to_drop}"
        )
        return df_irt[~df_irt['item_name'].isin(to_drop)]
    else:
        print("No uninformative items found.")
        return df_irt
