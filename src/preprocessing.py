import csv
import pandas as pd
import matplotlib.pyplot as plt
import os

# Function to read and preprocess the dataset
def read_and_preprocess(file_path, variable_column, quality_column):
    rows = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i >= 21:  # Skiping the metadata and the actual header row
                rows.append(row)

    df = pd.DataFrame(rows, columns=['SOUID', 'DATE', variable_column, quality_column])

    # Convert variable and quality columns to numeric types
    df[variable_column] = pd.to_numeric(df[variable_column], errors='coerce')
    df[quality_column] = pd.to_numeric(df[quality_column], errors='coerce')

    # Convert DATE to datetime
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y%m%d', errors='coerce')

    # Filter rows with valid variable values and quality code == 0
    df = df[(df[variable_column] != -9999) & (df[quality_column] == 0)]
    
    # Drop rows with NaN values in DATE or variable column
    df = df.dropna(subset=['DATE', variable_column])

    # Adjust temperature to degrees Celsius
    df[variable_column] = df[variable_column] / 10.0

    # Add a decade column
    df['Decade'] = (df['DATE'].dt.year // 10) * 10
    return df

# Function to plot climactic variable data by decades
def plot_decades(df, temperature_column):
    # Get unique decades
    decades = sorted(df['Decade'].unique())

    # Set up the subplot grid (square layout)
    num_decades = len(decades)
    cols = int(num_decades**0.5)  # Number of columns for square layout
    rows = -(-num_decades // cols)  # Calculate rows (ceiling division)

    fig, axes = plt.subplots(rows, cols, figsize=(15, 15), constrained_layout=True)

    # Plot each decade in a subplot
    for i, decade in enumerate(decades):
        # Get current axis
        ax = axes.flatten()[i]

        # Filter data for the current decade
        decade_data = df[df['Decade'] == decade]
        dates = decade_data['DATE']
        temps = decade_data[temperature_column]

        # Plot the data
        # change Temperature with the appropriate climactic variable
        ax.plot(dates, temps, label=f'Temperature ({decade}s)', linewidth=0.7, color='blue')
        ax.set_title(f'{decade}s', fontsize=12)
        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Temperature (°C)', fontsize=10)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(fontsize=8)

    # Remove empty subplots (if any)
    for i in range(len(decades), rows * cols):
        fig.delaxes(axes.flatten()[i])

    # Show the plot
    plt.show()

def save_csv(file_path, df):
    # to save the csv file after preprocessing
    file_name, ext = os.path.splitext(os.path.basename(file_path))
    df.to_csv(f"res/preprocessed_data/{file_name}_processed.csv", index=False)

# Main function to process and plot a given dataset
def main():
    # File path and column names
    file_path = r'res/raw_data/TG_SOUID121044.txt'  # Replace with your file path
    variable_column = 'TG'  # Replace with your temperature column (e.g., 'TX', 'TN')
    quality_column = 'Q_TG'  # Replace with your quality column (e.g., 'Q_TX', 'Q_TN')

    # Read and preprocess the data
    df = read_and_preprocess(file_path, variable_column, quality_column)
    
    # Plot the data by decades
    plot_decades(df, variable_column)

    # to save the csv file of the processed data
    save_csv(file_path, df)

# Run the main function
if __name__ == '__main__':
    main()
