import pandas as pd
import os
import csv

def read_preprocess(files_path, filename):
    rows = []
    with open(files_path + filename, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i >= 20: 
                rows.append(row)
    df = pd.DataFrame(rows)
    df = df.drop(df.columns[0], axis=1)
    headers = list(df.iloc[0])
    df  = pd.DataFrame(df.values[1:], columns=headers)
    df = df.reset_index(drop=True)

    df[headers[0]] = pd.to_datetime(df[headers[0]], format='%Y%m%d', errors='coerce')
    df[headers[1]] = pd.to_numeric(df[headers[1]], errors='coerce')
    df[headers[2]] = pd.to_numeric(df[headers[2]], errors='coerce')
    return df

def save_csv(file_name, df):
    # to save the csv file after preprocessing
    base, ext = os.path.splitext(file_name)
    df.to_csv(f"./res/preprocessed_data/{base}_processed.csv", index=False)

if __name__ == "__main__":
    files_path = "./res/raw_data/"
    files = os.listdir(files_path)
    for _, file in enumerate(files): 
        df = read_preprocess(files_path, file)
        save_csv(file, df)
    