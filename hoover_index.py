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
        df_copy = df_copy.sort_values(by=[column])
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
df_france = pd.read_csv(r"data/france.csv")
year_columns = df_france.iloc[:, -21:].columns
france = hoover_index(df_france, columns=year_columns, as_dataframe=False)
df_france = hoover_index(df_france, columns=year_columns, as_dataframe=True)
print(f"France GDP hoover index results as list of tuples:"
      f"\n{france}\n")

# Great Britain
df_gbr = pd.read_csv(r"data/great_britain.csv")
year_columns = df_gbr.iloc[:, -21:].columns
df_gbr = hoover_index(df_gbr, columns=year_columns, as_dataframe=True)
print(f"Great Britain GDP hoover index results as dataframe:"
      f"\n{df_gbr}")

# Saving results
# df_france.to_csv(r"results/france_hoover.csv")
# df_gbr.to_csv(r"results/great_britain_hoover.csv")
