import csv
import pandas as pd

def read_and_preprocess(file_path, value_column, quality_column, scale_factor=1):
    rows = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i >= 21:  # Skipping metadata and the actual header row
                rows.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(rows, columns=['SOUID', 'DATE', value_column, quality_column])

    # Convert columns to appropriate types
    df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
    df[quality_column] = pd.to_numeric(df[quality_column], errors='coerce')
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d', errors='coerce')

    # Filter valid values (exclude missing values and suspect quality codes)
    df = df[(df[value_column] != -9999) & (df[quality_column] == 0)]
    df = df.dropna(subset=['DATE', value_column])

    # Scale the values
    df[value_column] = df[value_column] / scale_factor

    return df[['DATE', value_column]]  # Return only the DATE and scaled value column

def preprocess_and_label(file_path, value_column, quality_column, label, scale_factor=1):
    # Preprocess using the existing function
    df = read_and_preprocess(file_path, value_column, quality_column, scale_factor)
    df.rename(columns={value_column: label}, inplace=True)  # Rename column with the label
    return df
