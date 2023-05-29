import pandas as pd
import json

with open('gamerating.json') as json_file:
    data = json.load(json_file)

df = pd.DataFrame(data)

# df = df.drop_duplicates(subset=['name'])

# print(df['platforms'])
df.to_excel('output.xlsx', index=False)


