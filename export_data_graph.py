import pandas as pd
import graphPopulation
from sklearn.model_selection import train_test_split

graph = graphPopulation.GraphPopulation()

df = graph.get_all_triple()
df.to_csv("graph_data.csv", index=False)
df_train, df_test = train_test_split(df, test_size=0.2)
df_train, df_val = train_test_split(df_train, test_size=0.2)
df_train.to_csv("tennis-train.txt", sep="\t", index=False, header=False)
df_test.to_csv("tennis-test.txt", sep="\t", index=False, header=False)
df_val.to_csv("tennis-valid.txt", sep="\t", index=False, header=False)