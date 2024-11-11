import re

import pandas as pd

df = pd.read_csv("scraped_data.csv")

custom_values = {
    "adresse": "",
    "by_og_zip": "",
    "ejendomsværdi_2024": 0,
    "grundværdi_2024": 0,
    "ejendomsværdi_2022": 0,
    "grundværdi_2022": 0,
}

df.fillna(value=custom_values, inplace=True)


def convert_to_number(value):
    if isinstance(value, str):
        value = re.sub(r"\D", "", value)
    return int(value)


print(df)

df["ejendomsværdi_2024"] = df["ejendomsværdi_2024"].apply(convert_to_number)
df["grundværdi_2024"] = df["grundværdi_2024"].apply(convert_to_number)
df["ejendomsværdi_2022"] = df["ejendomsværdi_2022"].apply(convert_to_number)
df["grundværdi_2022"] = df["grundværdi_2022"].apply(convert_to_number)

print(df)

print(len(df))
df.drop_duplicates(subset="property_id", inplace=True)
print(len(df))

df.sort_values(by="property_id", inplace=True)

df.to_csv("cleaned_data.csv", index=False)
