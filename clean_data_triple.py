import pandas as pd

df = pd.read_csv("/Users/vietnguyen/Workspace/Codes/Python/Knowledge-Graph-Intro/dataset/data_dbpedia.csv")

i = 0
def clean_row(row):
    try:
        global i
        i+=1
        print(i)
        sub = row["subject"]
        pre = row["predicate"]
        obj = row["object"]
        row["subject"] = str(sub.replace("_", " ")).lower()
        row["predicate"] = str(pre.replace("_", " ")).lower()
        row["object"] = str(obj.replace("_", " ")).lower()
        return row
    except:
        print(row)
        return row