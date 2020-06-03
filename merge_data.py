import pandas as pd
import os

path = "/Users/vietnguyen/Workspace/Codes/Python/Knowledge-Graph-Intro/dataset/data_3"
files = os.listdir(path)
dfs = []
for file in files:
    df = pd.read_csv(os.path.join(path, file))
    print(df.head())
    if len(df.columns) > 3:
        df = df[list(df.columns)[1:]]
    dfs.append(df)
df_all = pd.concat(dfs)
df_all.drop_duplicates(inplace=True)
df_all.to_csv("data3.csv", index=False)
