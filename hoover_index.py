import pandas as pd


def hoover_index(data, columns=None, as_dataframe=False):
    """

    df -> a pandas dataframe object that contains the information

    columns -> the column names of the pandas dataframe that contain the values required for computation; can be a list
    or a string

    as_dataframe -> True if the results returned are preferred as a dataframe, otherwise a list of tuples will be
                    returned

    """

    df_copy = data.copy()
    results = []

    if type(columns) != list:
        columns = list(columns)

    for column in columns:
        df_copy = df.sort_values(by=[column])
        row_number = len(df_copy.index)

        df_copy['rank'] = list(range(1, row_number + 1))
        df_copy['%labels'] = df_copy['rank'] / row_number

        values_sum = df_copy[column].sum()
        df_copy['%values'] = (df_copy[column] / values_sum)
        df_copy['%values'] = df_copy['%values'].cumsum(axis=0)

        df_copy['difference'] = df_copy['%labels'] - df_copy['%values']

        hoover = max(df_copy['difference'].values)
        results.append((column, hoover))

    if as_dataframe:
        results = pd.DataFrame(results, columns=['label', 'hoover_index'])

    return results


# These CSV files contain OECD GDP per capita data for France and Great Britain
# Data source: https://www.oecd.org/regional/regional-statistics/

# France
df = pd.read_csv(r"data/france.csv")
year_columns = df.iloc[:, -21:].columns
print(f"France GDP hoover index results as list of tuples:"
      f"\n{hoover_index(df, columns=year_columns, as_dataframe=False)}\n")

# Great Britain
df = pd.read_csv(r"data/gbr.csv")
year_columns = df.iloc[:, -21:].columns
print(f"Great Britain GDP hoover index results as dataframe:"
      f"\n{hoover_index(df, columns=year_columns, as_dataframe=True)}")