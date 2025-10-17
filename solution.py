import pandas as pd
import re

def add_virtual_column(df: pd.DataFrame, rule: str, new_column: str) -> pd.DataFrame:
    """
    Add a virtual column to a DataFrame based on a mathematical rule.
    
    Args:
        df: Input pandas DataFrame
        rule: String defining the computation (e.g., "column1 + column2")
        new_column: Name of the new column to be added
    
    Returns:
        DataFrame with the new column, or empty DataFrame if validation fails
    """
    # validations
    if not re.match(r'^[a-zA-Z_]+$', new_column):
        return pd.DataFrame()
    
    for col in df.columns:
        if not re.match(r'^[a-zA-Z_]+$', col):
            return pd.DataFrame()
    
    rule = rule.strip()
    
    if not re.match(r'^[a-zA-Z_\s+\-*]+$', rule):
        return pd.DataFrame()
    
    # extract column names from rule
    columns_in_rule = re.findall(r'[a-zA-Z_]+', rule)
    
    # check if all columns in rule exist in the DataFrame
    for col in columns_in_rule:
        if col not in df.columns:
            return pd.DataFrame()
    
    result_df = df.copy()
    
    # build the expression by replacing column names with df references
    # we need to be careful to replace whole words only
    expression = rule
    for col in df.columns:
        expression = re.sub(r'\b' + col + r'\b', f'result_df["{col}"]', expression)
    
    try:
        result_df[new_column] = eval(expression)
        return result_df
    except Exception:
        return pd.DataFrame()