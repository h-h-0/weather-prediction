import pandas as pd
from data_processing import preprocess_and_label

def create_master_dataset(files_and_columns, scale_factors):
    master_df = None

    for i, (file_path, value_column, quality_column, label) in enumerate(files_and_columns):
        # Preprocess and label the dataset
        df = preprocess_and_label(file_path, value_column, quality_column, label, scale_factors[i])

        # Merge with the master DataFrame
        if master_df is None:
            master_df = df  # Initialize master_df
        else:
            master_df = pd.merge(master_df, df, on='DATE', how='inner')  # Inner join on DATE

    return master_df

def main():
    # List of files, columns, and labels
    files_and_columns = [
        ('TG_SOUID121044.txt', 'TG', 'Q_TG', 'Temperature_Mean'),
        ('TX_SOUID121046.txt', 'TX', 'Q_TX', 'Temperature_Max'),
        ('TN_SOUID121045.txt', 'TN', 'Q_TN', 'Temperature_Min'),
        ('FX_SOUID121049.txt', 'FX', 'Q_FX', 'Wind_Gust'),
        ('HU_SOUID121047.txt', 'HU', 'Q_HU', 'Humidity'),
        ('CC_SOUID121039.txt', 'CC', 'Q_CC', 'Cloud_Cover'),
        ('FG_SOUID121048.txt', 'FG', 'Q_FG', 'Wind_Speed'), 
        ('PP_SOUID121041.txt', 'PP', 'Q_PP', 'Sea_Level_Pressure'),
        ('QQ_SOUID210447.txt', 'QQ', 'Q_QQ', 'Global_Radiation'),
        ('RR_SOUID121042.txt', 'RR', 'Q_RR', 'Precipitation'), 
        ('SD_SOUID121043.txt', 'SD', 'Q_SD', 'Snow_Depth'), 
        ('SS_SOUID121040.txt', 'SS', 'Q_SS', 'Sunshine'),
    ]

    # Scale factors (adjust units as needed)
    scale_factors = [10, 10, 10, 10, 1, 1, 10, 10, 1, 10, 100, 10]  # e.g., temperatures in 0.1°C, wind speed in 0.1 m/s

    # Create the master dataset
    master_df = create_master_dataset(files_and_columns, scale_factors)

    # Save to a CSV file
    master_df.to_csv('master_dataset.csv', index=False)

    print("Master dataset created and saved as 'master_dataset.csv'.")

if __name__ == '__main__':
    main()
