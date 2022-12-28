import pandas as pd

df = pd.read_csv("trials/trials_split_cogsciSelection.csv")
selected_cols = ["itemName", "vignette_start", "competitor", "sameCategory", "otherCategory", "vignette_continuation", "question", "taciturn", "competitor", "sameCategory", "otherCategory"]

txt_out = ""

for i, r in df.iterrows():
    txt = ""
    for c in selected_cols:
        txt = txt + r[c] + "\n"
    txt_out = txt_out + txt + "\n\n"

with open("trials/trials_split_cogsciSelection.txt", 'w') as f:
    f.write(txt_out)
    f.close()