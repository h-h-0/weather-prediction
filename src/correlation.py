import pandas as pd
import seaborn as sns # type: ignore
import matplotlib.pyplot as plt

def calculate_correlation(master_file):
    # Load the master dataset
    master_df = pd.read_csv(master_file)

    # Ensure only numeric columns are included in the correlation calculation
    numeric_df = master_df.select_dtypes(include=['float64', 'int64'])

    # Calculate the correlation matrix
    correlation_matrix = numeric_df.corr(method='spearman')  
    print("Correlation Matrix:\n", correlation_matrix)

    # Visualize the correlation matrix as a heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True)
    plt.title('Correlation Matrix Heatmap')
    plt.show()

    return correlation_matrix

    

def main():
    # Path to the master dataset
    master_file = 'master_dataset.csv'  # Replace with the path to your dataset

    # Calculate correlations
    correlation_matrix = calculate_correlation(master_file)

if __name__ == '__main__':
    main()
