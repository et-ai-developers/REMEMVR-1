"""
REMEMVR Data Extraction Module

This module provides functions for extracting data from master.xlsx using a
tag-based system. It replaces the legacy variables.xlsx regex approach.

Key Features:
- Direct tag extraction from master.xlsx
- Validation with expected dimensions
- Missing data handling per column
- Support for multiple data sources (master.xlsx + previous RQ outputs)

Author: REMEMVR Project
Created: 2025-01-05 (TDD Rewrite)
"""

import pandas as pd
import numpy as np
import os
from typing import Union, List, Dict, Optional


# ==============================================================================
# EXCEPTIONS
# ==============================================================================

class ValidationError(Exception):
    """Raised when data validation fails"""
    pass


# ==============================================================================
# CORE FUNCTIONS
# ==============================================================================

def load_master(use_cache: bool = True) -> pd.DataFrame:
    """
    Load master.xlsx data with optional caching.

    This function is kept from the legacy system as it works correctly.
    It loads the master Excel file and caches it as CSV for faster subsequent loads.

    Parameters:
    -----------
    use_cache : bool, default=True
        If True, use cached CSV version if available.
        If False, force reload from Excel.

    Returns:
    --------
    pd.DataFrame
        Master dataframe with columns in pairs: (UID, UID-D)
        Example columns: A010, A010-D, A011, A011-D, ...

    Notes:
    ------
    - First column in each pair contains tags (e.g., "A010-COG-X-RPM-Scor")
    - Second column contains data values (e.g., "8")
    - "x" values in data columns represent missing data (converted to NaN)

    Example:
    --------
    >>> df_master = load_master()
    >>> print(df_master.shape)
    (1854, 200)  # 1854 tags × 100 participants × 2 columns per participant
    """
    print("\n--- Master Data ---\n")

    cache_path = './data/cache/dfMaster.csv'

    if use_cache and os.path.exists(cache_path):
        print("Cached Version Found")
        df_master = pd.read_csv(cache_path)
        print("Master Data Loaded")
    else:
        print("Cached Version Not Found\nLoading from Excel")
        df_master = pd.read_excel('./data/master.xlsx')

        print("Creating New Cache")
        # Clear old cache files
        cache_dir = './data/cache'
        if os.path.exists(cache_dir):
            cache_files = os.listdir(cache_dir)
            for file in cache_files:
                os.remove(f'{cache_dir}/{file}')

        # Save new cache
        df_master.to_csv(cache_path, index=False)
        print("Master Data Loaded")

    return df_master


def extract_tag(
    tag_pattern: str,
    uids: Optional[List[str]] = None,
    expected_count: Optional[int] = None,
    allow_missing: bool = False,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Extract data for a single tag pattern from master.xlsx.

    This is the foundation function for all data extraction. It searches for
    tags matching the pattern and returns the corresponding data values.

    Parameters:
    -----------
    tag_pattern : str
        Tag pattern to search for. Use {UID} placeholder for participant IDs.
        Example: "{UID}-COG-X-RPM-Scor"
    uids : List[str], optional
        List of participant IDs to extract. If None, uses all 100 participants.
        Example: ["A010", "A011", "A012"]
    expected_count : int, optional
        Expected number of values to extract. Raises ValidationError if mismatch.
        This forces explicit expectations to catch regex errors.
    allow_missing : bool, default=False
        If True, allows "x" values (missing data) without error.
        If False, raises ValidationError if any missing data found.
    df_master : pd.DataFrame, optional
        Master dataframe. If None, loads automatically using load_master().

    Returns:
    --------
    pd.DataFrame
        DataFrame with columns ['UID', 'value'] containing extracted data.
        Missing data ("x") converted to NaN.

    Raises:
    -------
    ValidationError
        - If expected_count specified and actual count doesn't match
        - If allow_missing=False and missing data found
        - If tag pattern not found for any participant

    Example:
    --------
    >>> rpm_scores = extract_tag(
    ...     tag_pattern="{UID}-COG-X-RPM-Scor",
    ...     expected_count=100
    ... )
    >>> print(rpm_scores.head())
       UID  value
    0  A010    8.0
    1  A011   10.0
    2  A012    7.0
    3  A013    9.0
    4  A014   11.0
    """
    # Load master data if not provided
    if df_master is None:
        df_master = load_master()

    # Default to all 100 participants if not specified
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    results = []
    missing_count = 0

    for uid in uids:
        # Replace {UID} placeholder with actual participant ID
        tag = tag_pattern.replace('{UID}', uid)

        # Get the tag column and data column for this participant
        tag_col = uid
        data_col = f'{uid}-D'

        # Check if columns exist
        if tag_col not in df_master.columns or data_col not in df_master.columns:
            raise ValidationError(f"Columns for {uid} not found in master data")

        # Find row where tag matches
        matching_rows = df_master[tag_col].astype(str) == tag

        if not matching_rows.any():
            raise ValidationError(f"Tag '{tag}' not found in master data")

        if matching_rows.sum() > 1:
            raise ValidationError(f"Tag '{tag}' found multiple times (expected unique)")

        # Get the data value
        data_value = df_master.loc[matching_rows, data_col].values[0]

        # Handle missing data
        if data_value == 'x':
            missing_count += 1
            if not allow_missing:
                raise ValidationError(
                    f"Missing data found for {uid} at tag '{tag}' (value='x'). "
                    f"Set allow_missing=True to permit missing data."
                )
            value = np.nan
        else:
            # Try to convert to float, keep as string if conversion fails
            try:
                value = float(data_value)
            except (ValueError, TypeError):
                value = data_value

        results.append({'UID': uid, 'value': value})

    # Validate expected count
    if expected_count is not None:
        actual_count = len(results)
        if actual_count != expected_count:
            raise ValidationError(
                f"Expected {expected_count} values, got {actual_count}. "
                f"This suggests the tag pattern may be incorrect."
            )

    return pd.DataFrame(results)


def extract_tags(
    tag_patterns: Union[List[str], Dict[str, str]],
    uids: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    expected_cols: Optional[int] = None,
    allow_missing: Union[bool, Dict[str, int]] = False,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Extract data for multiple tag patterns from master.xlsx.

    This function builds on extract_tag() to handle multiple variables at once.
    It's the primary function for preparing RQ input data.

    Parameters:
    -----------
    tag_patterns : List[str] or Dict[str, str]
        If list: Tag patterns to extract. Column names derived automatically.
        If dict: {column_name: tag_pattern} pairs.
        Example (list): ["{UID}-COG-X-RPM-Scor", "{UID}-COG-X-NART-Scor"]
        Example (dict): {"RPM_Score": "{UID}-COG-X-RPM-Scor", "NART_Score": "{UID}-COG-X-NART-Scor"}
    uids : List[str], optional
        List of participant IDs. If None, uses all 100 participants.
    expected_rows : int, optional
        Expected number of rows in output. Validates dimensions.
    expected_cols : int, optional
        Expected number of columns in output. Validates dimensions.
    allow_missing : bool or Dict[str, int], default=False
        If bool: Apply to all columns
        If dict: Specify max missing count per column
        Example: {"RAVLT_T5": 5, "RPM_Score": 0}
    df_master : pd.DataFrame, optional
        Master dataframe. If None, loads automatically using load_master().

    Returns:
    --------
    pd.DataFrame
        DataFrame with UIDs as index and extracted variables as columns.

    Raises:
    -------
    ValidationError
        - If dimension validation fails
        - If missing data rules violated

    Example:
    --------
    >>> cognitive_data = extract_tags(
    ...     tag_patterns=[
    ...         "{UID}-COG-X-RPM-Scor",
    ...         "{UID}-COG-X-NART-Scor"
    ...     ],
    ...     expected_rows=100,
    ...     expected_cols=2
    ... )
    """
    # Load master data if not provided
    if df_master is None:
        df_master = load_master()

    # Default to all 100 participants if not specified
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    # Convert tag_patterns to dict format if it's a list
    if isinstance(tag_patterns, list):
        # Derive column names from tag patterns
        patterns_dict = {}
        for tag_pattern in tag_patterns:
            col_name = tag_pattern.replace('{UID}-', '').replace('-', '_')
            patterns_dict[col_name] = tag_pattern
    else:
        # Already a dict
        patterns_dict = tag_patterns

    # Extract each tag pattern
    data_dict = {}
    uid_column = None

    for col_name, tag_pattern in patterns_dict.items():
        # Determine if missing data allowed for this column
        if isinstance(allow_missing, dict):
            allow_missing_col = col_name in allow_missing
        else:
            allow_missing_col = allow_missing

        # Extract data for this tag
        df_tag = extract_tag(
            tag_pattern,
            uids=uids,
            expected_count=len(uids),
            allow_missing=allow_missing_col,
            df_master=df_master
        )

        # Store UID column (first time only)
        if uid_column is None:
            uid_column = df_tag['UID'].values

        # Add the 'value' column to data_dict with the column name
        data_dict[col_name] = df_tag['value'].values

    # Create DataFrame with UID as first column
    df = pd.DataFrame(data_dict)
    df.insert(0, 'UID', uid_column)

    # Validate dimensions
    if expected_rows is not None:
        actual_rows = len(df)
        if actual_rows != expected_rows:
            raise ValidationError(
                f"Expected {expected_rows} rows, got {actual_rows}"
            )

    if expected_cols is not None:
        actual_cols = len(df.columns)
        if actual_cols != expected_cols:
            raise ValidationError(
                f"Expected {expected_cols} columns, got {actual_cols}"
            )

    # Validate missing data if dict rules provided
    if isinstance(allow_missing, dict):
        for col_name, max_missing in allow_missing.items():
            if col_name in df.columns:
                missing_count = df[col_name].isna().sum()
                if missing_count > max_missing:
                    raise ValidationError(
                        f"Column '{col_name}' has {missing_count} missing values, "
                        f"but max allowed is {max_missing}"
                    )

    return df


def validate_extraction(
    df: pd.DataFrame,
    expected_rows: Optional[int] = None,
    expected_cols: Optional[int] = None,
    required_cols: Optional[List[str]] = None,
    missing_rules: Optional[Dict[str, int]] = None
) -> Dict[str, any]:
    """
    Validate extracted data against expectations.

    This function performs comprehensive validation checks to ensure data
    extraction worked correctly and catches silent failures.

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to validate
    expected_rows : int, optional
        Expected number of rows
    expected_cols : int, optional
        Expected number of columns
    required_cols : List[str], optional
        List of column names that must exist
    missing_rules : Dict[str, int], optional
        Maximum allowed missing values per column
        Example: {"RAVLT_T5": 5, "Age": 0}

    Returns:
    --------
    Dict[str, any]
        Validation report with keys:
        - 'valid': bool, overall validation status
        - 'errors': List[str], validation errors found
        - 'warnings': List[str], validation warnings
        - 'stats': Dict, basic statistics about the data

    Example:
    --------
    >>> result = validate_extraction(
    ...     df,
    ...     expected_rows=100,
    ...     expected_cols=4,
    ...     missing_rules={"RAVLT_T5": 5}
    ... )
    >>> if not result['valid']:
    ...     print(result['errors'])
    """
    errors = []
    warnings = []

    # Validate dimensions
    if expected_rows is not None:
        actual_rows = len(df)
        if actual_rows != expected_rows:
            errors.append(
                f"Row count mismatch: expected {expected_rows}, got {actual_rows}"
            )

    if expected_cols is not None:
        actual_cols = len(df.columns)
        if actual_cols != expected_cols:
            errors.append(
                f"Column count mismatch: expected {expected_cols}, got {actual_cols}"
            )

    # Validate required columns exist
    if required_cols is not None:
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            errors.append(
                f"Missing required columns: {', '.join(missing_cols)}"
            )

    # Validate missing data rules
    if missing_rules is not None:
        for col_name, max_missing in missing_rules.items():
            if col_name in df.columns:
                missing_count = df[col_name].isna().sum()
                if missing_count > max_missing:
                    errors.append(
                        f"Column '{col_name}': {missing_count} missing values "
                        f"exceeds maximum of {max_missing}"
                    )
                elif missing_count > 0:
                    warnings.append(
                        f"Column '{col_name}': {missing_count} missing values "
                        f"(within limit of {max_missing})"
                    )

    # Generate statistics
    stats = {
        'rows': len(df),
        'cols': len(df.columns),
        'total_missing': df.isna().sum().sum(),
        'columns': list(df.columns)
    }

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'stats': stats
    }


# ==============================================================================
# ADVANCED FUNCTIONS (TO BE IMPLEMENTED)
# ==============================================================================

def extract_vr_tags(
    paradigm: str,
    domain: str,
    item: str,
    measure: str,
    tests: Optional[List[int]] = None,
    uids: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Extract VR data across multiple tests with wildcard support.

    This function handles VR tags that vary by test number (T1, T2, T3, T4)
    and item-specific details (order, start location, finish location).

    Parameters:
    -----------
    paradigm : str
        Testing paradigm code.
        Options: 'RFR', 'IFR', 'TCR', 'ICR', 'RRE', 'IRE'
    domain : str
        Memory domain code.
        Options: 'N' (What), 'L' (Where-general), 'U' (Up/Pick-up), 'D' (Down/Put-down), 'O' (When)
    item : str
        Item identifier.
        Examples: 'i1CM', 'i2CM', 'i3CG', 'i4CG', 'i5IC', 'i6IC', 'OBJ1', 'WEAT', 'TSK1'
    measure : str
        Measurement type.
        Options: 'ANS' (Accuracy), 'CON' (Confidence)
    tests : List[int], optional
        List of test numbers to extract. Defaults to [1, 2, 3, 4].
        Example: [1, 3] to extract only T1 and T3
    uids : List[str], optional
        List of participant IDs. Defaults to all 100 if not specified.
    expected_rows : int, optional
        Expected total number of rows. Validates output.
    df_master : pd.DataFrame, optional
        Master dataframe. Loads automatically if not provided.

    Returns:
    --------
    pd.DataFrame
        Long-format dataframe with columns: ['UID', 'test', 'value']
        Each row represents one participant × one test.

    Example:
    --------
    >>> # Extract Item 1 accuracy across all 4 tests for all participants
    >>> item1_accuracy = extract_vr_tags(
    ...     paradigm='IFR',
    ...     domain='N',
    ...     item='i1CM',
    ...     measure='ANS',
    ...     expected_rows=400  # 100 participants × 4 tests
    ... )
    >>> print(item1_accuracy.head())
        UID  test  value
    0  A010     1    1.0
    1  A010     2    1.0
    2  A010     3    0.5
    3  A010     4    1.0
    4  A011     1    1.0
    """
    # Load master data if not provided
    if df_master is None:
        df_master = load_master()

    # Default to all participants
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    # Default to all 4 tests
    if tests is None:
        tests = [1, 2, 3, 4]

    results = []

    # For each test, extract data across all participants
    for test_num in tests:
        # Build tag pattern with test wildcard
        # Format: {UID}-RVR-T{test}-{paradigm}-{domain}-{item}-{details}-{measure}
        # The {details} part is wildcarded (n{order}s{start}f{finish})

        # For each participant
        for uid in uids:
            tag_col = uid
            data_col = f'{uid}-D'

            # Check if columns exist
            if tag_col not in df_master.columns or data_col not in df_master.columns:
                raise ValidationError(f"Columns for {uid} not found in master data")

            # Build search pattern with room wildcard
            # Format depends on paradigm:
            # Items paradigms (IFR, ICR, IRE): {UID}-RVR-T{test}-{ROOM}-{paradigm}-{domain}-{item}-{details}-{measure}
            #   Example: A010-RVR-T1-BAT-IFR-N-i1CM-n4siCfo3-ANS
            # Room/Task paradigms (RFR, RRE, TCR): {UID}-RVR-T{test}-{ROOM}-{paradigm}-{domain}-{item}-{measure}
            #   Example: A010-RVR-T1-BAT-RFR-N-OBJ1-ANS (NO item details!)
            # Room code (BAT, BED, KIT, LIV) varies per test - use wildcard
            import re

            # Check if this paradigm has item details
            if paradigm in ['IFR', 'ICR', 'IRE']:
                # Items paradigms have item details (n4siCfo3, etc.)
                pattern = f'{uid}-RVR-T{test_num}-[A-Z]{{3}}-{paradigm}-{domain}-{item}-.+?-{measure}'
            else:
                # Room/Task paradigms (RFR, RRE, TCR) have NO item details
                pattern = f'{uid}-RVR-T{test_num}-[A-Z]{{3}}-{paradigm}-{domain}-{item}-{measure}'

            # Find rows that match the pattern (allows any 3-letter room code)
            tag_series = df_master[tag_col].astype(str)
            matching_rows = tag_series.str.match(pattern)

            if matching_rows.sum() == 0:
                # No match found - this could be expected for some VR questions
                value = np.nan
            elif matching_rows.sum() == 1:
                # Exactly one match - extract value
                data_value = df_master.loc[matching_rows, data_col].values[0]

                # Handle missing data
                if data_value == 'x':
                    value = np.nan
                else:
                    try:
                        value = float(data_value)
                    except (ValueError, TypeError):
                        value = data_value
            else:
                # Multiple matches - this is unexpected
                matching_tags = df_master.loc[matching_rows, tag_col].tolist()
                raise ValidationError(
                    f"Multiple tags found for {uid} Test {test_num}:\n"
                    f"Pattern: {pattern_prefix}*{pattern_suffix}\n"
                    f"Matches: {matching_tags}"
                )

            results.append({
                'UID': uid,
                'test': test_num,
                'value': value
            })

    # Create dataframe
    result_df = pd.DataFrame(results)

    # Validate expected rows
    if expected_rows is not None:
        actual_rows = len(result_df)
        if actual_rows != expected_rows:
            raise ValidationError(
                f"Expected {expected_rows} rows, got {actual_rows}"
            )

    return result_df


def extract_cognitive_scores(
    test_name: str,
    scores_to_compute: Dict[str, List[str]],
    expected_count: Optional[int] = None,
    uids: Optional[List[str]] = None,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Extract cognitive test scores and compute derived totals.

    This function extracts individual cognitive test components and computes
    derived scores (e.g., RAVLT_Total = sum of T1-T5).

    Parameters:
    -----------
    test_name : str
        Name of the cognitive test.
        Options: 'RAVLT', 'BVMT', 'NART', 'RPM'
    scores_to_compute : Dict[str, List[str]]
        Dictionary mapping computed score names to list of component tags.
        Example: {'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc']}
    expected_count : int, optional
        Expected number of participants. Validates output row count.
    uids : List[str], optional
        List of participant IDs. Defaults to all 100 if not specified.
    df_master : pd.DataFrame, optional
        Master dataframe. Loads automatically if not provided.

    Returns:
    --------
    pd.DataFrame
        DataFrame with columns: UID + computed score columns.
        Missing data handled gracefully (NaN if any component missing).

    Example:
    --------
    >>> ravlt_totals = extract_cognitive_scores(
    ...     test_name='RAVLT',
    ...     scores_to_compute={
    ...         'RAVLT_Total': ['T1Sc', 'T2Sc', 'T3Sc', 'T4Sc', 'T5Sc'],
    ...         'Learning': ['T5Sc', 'T1Sc']  # T5 - T1 (computed as difference)
    ...     },
    ...     expected_count=100
    ... )
    """
    # Load master data if not provided
    if df_master is None:
        df_master = load_master()

    # Default to all 100 participants
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    # Map test names to tag prefixes
    test_tag_prefixes = {
        'RAVLT': 'COG-X-RAV',
        'BVMT': 'COG-X-BVM',
        'NART': 'COG-X-NAR',
        'RPM': 'COG-X-RPM'
    }

    if test_name not in test_tag_prefixes:
        raise ValidationError(
            f"Unknown test_name '{test_name}'. "
            f"Valid options: {list(test_tag_prefixes.keys())}"
        )

    tag_prefix = test_tag_prefixes[test_name]

    # Extract all component scores
    all_components = set()
    for component_list in scores_to_compute.values():
        all_components.update(component_list)

    # Build tag patterns for all components
    tag_patterns = {}
    for component in all_components:
        tag_patterns[component] = f'{{UID}}-{tag_prefix}-{component}'

    # Extract all component data (allow missing for cognitive tests)
    components_df = extract_tags(
        tag_patterns=tag_patterns,
        uids=uids,
        allow_missing=True,  # Some participants have missing T4/T5 etc.
        df_master=df_master
    )

    # Compute derived scores
    result = pd.DataFrame({'UID': components_df['UID']})

    for computed_name, component_list in scores_to_compute.items():
        # Sum across components (NaN if any component missing)
        score_sum = components_df[component_list].sum(axis=1)

        # If all components are NaN, result should be NaN
        all_nan = components_df[component_list].isna().all(axis=1)
        score_sum[all_nan] = np.nan

        result[computed_name] = score_sum

    # Validate expected count
    if expected_count is not None:
        actual_count = len(result)
        if actual_count != expected_count:
            raise ValidationError(
                f"Expected {expected_count} participants, got {actual_count}"
            )

    return result


def load_rq_output(
    file_path: str,
    expected_rows: Optional[int] = None,
    expected_cols: Optional[int] = None,
    required_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Load previous RQ output data from CSV file.

    This function is used to load results from previous RQs as input for
    subsequent analyses (e.g., theta scores from IRT analysis used in LMM).

    Parameters:
    -----------
    file_path : str
        Path to the RQ output CSV file.
        Example: "results/ch5/rq1/data/output.csv"
    expected_rows : int, optional
        Expected number of rows. Raises ValidationError if mismatch.
    expected_cols : int, optional
        Expected number of columns. Raises ValidationError if mismatch.
    required_cols : List[str], optional
        List of column names that must be present.
        Example: ['UID', 'theta_what', 'theta_where']

    Returns:
    --------
    pd.DataFrame
        Loaded data with all columns preserved.

    Raises:
    -------
    ValidationError
        - If file doesn't exist
        - If expected dimensions don't match
        - If required columns missing

    Example:
    --------
    >>> theta_scores = load_rq_output(
    ...     file_path="results/ch5/rq1/data/output.csv",
    ...     required_cols=['UID', 'theta_what', 'theta_where', 'theta_when']
    ... )
    >>> print(theta_scores.head())
        UID  theta_what  theta_where  theta_when
    0  A010        0.52         0.34        0.68
    1  A011        0.61         0.42        0.79
    """
    # Check file exists
    if not os.path.exists(file_path):
        raise ValidationError(f"RQ output file not found: {file_path}")

    # Load CSV
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValidationError(f"Failed to load RQ output file: {e}")

    # Validate dimensions
    if expected_rows is not None:
        actual_rows = len(df)
        if actual_rows != expected_rows:
            raise ValidationError(
                f"RQ output row count mismatch: expected {expected_rows}, got {actual_rows}"
            )

    if expected_cols is not None:
        actual_cols = len(df.columns)
        if actual_cols != expected_cols:
            raise ValidationError(
                f"RQ output column count mismatch: expected {expected_cols}, got {actual_cols}"
            )

    # Validate required columns
    if required_cols is not None:
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise ValidationError(
                f"RQ output missing required columns: {', '.join(missing_cols)}"
            )

    return df


def combine_data_sources(
    master_tags: Optional[Dict[str, str]] = None,
    rq_outputs: Optional[List[str]] = None,
    computed_scores: Optional[Dict[str, pd.Series]] = None,
    uids: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    expected_cols: Optional[int] = None,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Combine data from multiple sources into a single dataframe.

    This is the primary data preparation function used by the data-prep agent.
    It merges data from master.xlsx tags, previous RQ outputs, and computed scores.

    Parameters:
    -----------
    master_tags : Dict[str, str], optional
        Dictionary mapping column names to tag patterns from master.xlsx.
        Example: {'RPM_Score': '{UID}-COG-X-RPM-Scor', 'Age': '{UID}-DEM-X-Age'}
    rq_outputs : List[str], optional
        List of file paths to previous RQ output CSV files.
        Example: ['results/ch5/rq1/data/output.csv']
    computed_scores : Dict[str, pd.Series], optional
        Dictionary mapping computed score names to pandas Series.
        Example: {'Age_Centered': age_series - age_series.mean()}
    uids : List[str], optional
        List of participant IDs. Defaults to all 100 if not specified.
    expected_rows : int, optional
        Expected number of rows in final dataframe. Validates output.
    expected_cols : int, optional
        Expected number of columns in final dataframe. Validates output.
    df_master : pd.DataFrame, optional
        Master dataframe. Loads automatically if not provided.

    Returns:
    --------
    pd.DataFrame
        Combined dataframe with UID column + all requested data columns.

    Raises:
    -------
    ValidationError
        - If merge fails (mismatched UIDs)
        - If expected dimensions don't match
        - If required data missing

    Example:
    --------
    >>> # Combine master tags + previous RQ output
    >>> data = combine_data_sources(
    ...     master_tags={'Age': '{UID}-DEM-X-Age', 'Education': '{UID}-DEM-X-Education'},
    ...     rq_outputs=['results/ch5/rq1/data/output.csv'],
    ...     expected_rows=100
    ... )
    >>> print(data.head())
        UID  Age  Education  theta_what  theta_where  theta_when
    0  A010   25          7        0.52         0.34        0.68
    1  A011   28          9        0.61         0.42        0.79
    """
    # Start with UID column
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    result = pd.DataFrame({'UID': uids})

    # 1. Extract master.xlsx tags if provided
    if master_tags is not None:
        master_data = extract_tags(
            tag_patterns=master_tags,
            uids=uids,
            allow_missing=True,  # Allow missing data
            df_master=df_master
        )
        # Merge on UID
        result = result.merge(master_data, on='UID', how='left')

    # 2. Load and merge RQ outputs if provided
    if rq_outputs is not None:
        for rq_output_path in rq_outputs:
            rq_data = load_rq_output(rq_output_path)

            # Ensure UID column exists
            if 'UID' not in rq_data.columns:
                raise ValidationError(
                    f"RQ output file missing UID column: {rq_output_path}"
                )

            # Merge on UID
            result = result.merge(rq_data, on='UID', how='left')

    # 3. Add computed scores if provided
    if computed_scores is not None:
        for score_name, score_series in computed_scores.items():
            # Ensure series has same length as result
            if len(score_series) != len(result):
                raise ValidationError(
                    f"Computed score '{score_name}' has {len(score_series)} values, "
                    f"expected {len(result)}"
                )
            result[score_name] = score_series.values

    # Validate dimensions
    if expected_rows is not None:
        actual_rows = len(result)
        if actual_rows != expected_rows:
            raise ValidationError(
                f"Combined data has {actual_rows} rows, expected {expected_rows}"
            )

    if expected_cols is not None:
        actual_cols = len(result.columns)
        if actual_cols != expected_cols:
            raise ValidationError(
                f"Combined data has {actual_cols} columns, expected {expected_cols}"
            )

    return result


def extract_vr_items_wide(
    paradigms: List[str],
    domains: List[str],
    items: List[str],
    measure: str,
    tests: Optional[List[int]] = None,
    uids: Optional[List[str]] = None,
    expected_rows: Optional[int] = None,
    df_master: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Extract multiple VR items in wide format by calling extract_vr_tags() in a loop.

    This function is designed for data-prep agents that need to extract many VR items
    at once. It loops through all combinations of paradigm × domain × item, extracts
    each using extract_vr_tags(), and pivots the results into wide format.

    Parameters:
    -----------
    paradigms : List[str]
        List of testing paradigm codes.
        Options: 'RFR', 'IFR', 'TCR', 'ICR', 'RRE', 'IRE'
        Example: ['IFR', 'ICR'] for Items Free Recall and Items Cued Recall
    domains : List[str]
        List of memory domain codes.
        Options: 'N' (What), 'L' (Where-general), 'U' (Up/Pick-up), 'D' (Down/Put-down), 'O' (When)
        Example: ['N', 'U', 'D'] for What, Pick-up, Put-down
    items : List[str]
        List of item identifiers.
        Examples: ['i1CM', 'i2CM', 'i3CG', 'i4CG', 'i5IC', 'i6IC']
    measure : str
        Measurement type.
        Options: 'ANS' (Accuracy), 'CON' (Confidence)
    tests : List[int], optional
        List of test numbers to extract. Defaults to [1, 2, 3, 4].
        Example: [1, 3] to extract only T1 and T3
    uids : List[str], optional
        List of participant IDs. Defaults to all 100 if not specified.
    expected_rows : int, optional
        Expected total number of rows. Validates output.
        Example: 400 for 100 participants × 4 tests
    df_master : pd.DataFrame, optional
        Master dataframe. Loads automatically if not provided.

    Returns:
    --------
    pd.DataFrame
        Wide-format dataframe with columns: ['UID', 'Test', item1_col, item2_col, ...]
        Each row represents one participant × one test.
        Item columns are named: 'TQ_{paradigm}_{item}_{domain}_{measure}'

    Raises:
    -------
    ValidationError
        - If expected_rows doesn't match actual rows
        - If any item extraction fails

    Example:
    --------
    >>> # Extract all IFR What domain items (6 items) across all 4 tests
    >>> data = extract_vr_items_wide(
    ...     paradigms=['IFR'],
    ...     domains=['N'],
    ...     items=['i1CM', 'i2CM', 'i3CG', 'i4CG', 'i5IC', 'i6IC'],
    ...     measure='ANS',
    ...     expected_rows=400  # 100 participants × 4 tests
    ... )
    >>> print(data.shape)
    (400, 8)  # UID + Test + 6 items
    >>> print(data.columns.tolist())
    ['UID', 'Test', 'TQ_IFR_i1CM_N_ANS', 'TQ_IFR_i2CM_N_ANS', ...]

    Notes:
    ------
    - Internally calls extract_vr_tags() for each paradigm × domain × item combination
    - Results are merged into wide format on (UID, test)
    - Column names use consistent format: TQ_{paradigm}_{item}_{domain}_{measure}
    - This function is optimized for agent use cases that need many items at once
    """
    # Load master data once
    if df_master is None:
        df_master = load_master()

    # Default to all participants
    if uids is None:
        uids = [f'A{str(i).zfill(3)}' for i in range(10, 110)]

    # Default to all 4 tests
    if tests is None:
        tests = [1, 2, 3, 4]

    # Initialize result with UID × Test combinations
    # Create all combinations of UID × test
    uid_test_combinations = []
    for uid in uids:
        for test in tests:
            uid_test_combinations.append({'UID': uid, 'Test': test})

    result = pd.DataFrame(uid_test_combinations)

    # Loop through all combinations of paradigm × domain × item
    for paradigm in paradigms:
        for domain in domains:
            for item in items:
                # Create column name: TQ_{paradigm}_{item}_{domain}_{measure}
                col_name = f'TQ_{paradigm}_{item}_{domain}_{measure}'

                # Extract this specific item using extract_vr_tags()
                item_data = extract_vr_tags(
                    paradigm=paradigm,
                    domain=domain,
                    item=item,
                    measure=measure,
                    tests=tests,
                    uids=uids,
                    df_master=df_master
                )

                # Rename 'value' column to the item-specific column name
                item_data = item_data.rename(columns={'value': col_name, 'test': 'Test'})

                # Merge into result on (UID, Test)
                result = result.merge(item_data, on=['UID', 'Test'], how='left')

    # Validate dimensions
    if expected_rows is not None:
        actual_rows = len(result)
        if actual_rows != expected_rows:
            raise ValidationError(
                f"extract_vr_items_wide() produced {actual_rows} rows, expected {expected_rows}"
            )

    return result
