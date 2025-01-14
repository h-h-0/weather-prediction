import pandas as pd
import os

if __name__ == "__main__":
    dir = os.listdir("./res/preprocessed_data/")
    master_df = pd.DataFrame()
    
    for i, file in enumerate(dir):
        with open("./res/preprocessed_data/" + file, 'r') as f:
            df = pd.read_csv(f)
            master_df = pd.concat([master_df, df], axis=1)
    
    print(master_df)
    master_df.to_csv("./res/preprocessed_data/master.csv")
    
