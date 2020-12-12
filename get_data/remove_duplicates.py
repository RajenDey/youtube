import pandas as pd
import numpy as np

df = pd.read_csv("videos.csv")

df = df.drop_duplicates(subset=["id"])

print(df)

df.to_csv("videos_no_dups.csv")