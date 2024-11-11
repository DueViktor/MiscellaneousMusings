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

import re


def convert_to_number(value):
    # Only proceed if value is a string
    if isinstance(value, str):
        # Use regex to remove all non-digit characters
        value = re.sub(r"\D", "", value)
    return int(value)  # Convert to integer


print(df)

# Apply the function to the relevant column
df["ejendomsværdi_2024"] = df["ejendomsværdi_2024"].apply(convert_to_number)
df["grundværdi_2024"] = df["grundværdi_2024"].apply(convert_to_number)
df["ejendomsværdi_2022"] = df["ejendomsværdi_2022"].apply(convert_to_number)
df["grundværdi_2022"] = df["grundværdi_2022"].apply(convert_to_number)

print(df)

df.to_csv("cleaned_data.csv", index=False)
