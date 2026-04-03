# %%
import re

import pandas as pd

# %%
patients_df = pd.read_csv("patients.csv")
print(patients_df.head())

# %%
treatments_df = pd.read_csv("treatments.csv")
treatments_cut_df = pd.read_csv("treatments_cut.csv")
adverse_reaction_df = pd.read_csv("adverse_reactions.csv")

# %%
# patients_df[patients_df.isnull
patients_df.info()

# %%
patients_df = patients_df.fillna("No data")

# %%
treatments_df = pd.concat([treatments_df, treatments_cut_df])

# %%
treatments_df["hba1c_change"] = (
    treatments_df["hba1c_start"] - treatments_df["hba1c_end"]
)
print(treatments_df.sample(5))


# %%
# so all completeness done
# %%
def separate_contact(contact):
    if pd.isna(contact):
        return pd.Series({"mobile": None, "email": None})

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    mobile_pattern = (
        r"(\+?1?\s*\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\d{3}[-.\s]\d{3}[-.\s]\d{4})"
    )

    email = re.search(email_pattern, contact)
    remaining = re.sub(email_pattern, "", contact) if email else contact

    email_match = email.group() if email else None
    mobile_match = re.search(mobile_pattern, remaining.replace(" ", ""))
    mobile = mobile_match.group() if mobile_match else None

    return pd.Series({"mobile": mobile, "email": email_match})


patients_df[["mobile", "email"]] = patients_df["contact"].apply(separate_contact)
print(patients_df.sample(5))


# %%
patients_df = patients_df.drop(columns=["contact"])

patients_df.info()
treatments_df.info()


# %%
def separate_dosage(value):
    if pd.isna(value) or value == "-":
        return pd.Series({"start": None, "end": None})
    parts = str(value).split(" - ")
    return pd.Series(
        {
            "start": parts[0].replace("u", "") if len(parts) > 0 else None,
            "end": parts[1].replace("u", "") if len(parts) > 1 else None,
        }
    )


treatments_df[["auralin_start", "auralin_end"]] = treatments_df["auralin"].apply(
    separate_dosage
)
treatments_df[["novodra_start", "novodra_end"]] = treatments_df["novodra"].apply(
    separate_dosage
)

treatments_df.sample(5)


# %%
treatments_df = treatments_df.drop(columns=["auralin", "novodra"])


# %% cell1
treatments_df.info()


# %%
treatments_df.sample(5)
# or we can


# %%
treatments_df = pd.read_csv("treatments.csv")
treatments_df = pd.concat([treatments_df, treatments_cut_df])
treatments_df["hba1c_change"] = (
    treatments_df["hba1c_start"] - treatments_df["hba1c_end"]
)
treatments_df.info()


# %%
treatments_df = treatments_df.melt(
    id_vars=["given_name", "surname", "hba1c_start", "hba1c_end", "hba1c_change"],
    var_name="type",
    value_name="dosage",
)
# %%
treatments_df.sample(2)
# %%
treatments_df = treatments_df[treatments_df["dosage"] != "-"]
treatments_df.sample(4)
# %%
treatments_df.info()
# %%
treatments_df["dosage_start"] = treatments_df["dosage"].str.split("-").str.get(0)
treatments_df["dosage_end"] = treatments_df["dosage"].str.split("-").str.get(1)


# %%
treatments_df = treatments_df.drop(columns=["dosage"])


# %% cell1
treatments_df.sample(3)
# %%
treatments_df["dosage_start"] = treatments_df["dosage_start"].str.replace("u", "")
treatments_df["dosage_end"] = treatments_df["dosage_end"].str.replace("u", "")
treatments_df.head(2)
# %%
treatments_df.info()
# %%
treatments_df = treatments_df.merge(
    adverse_reaction_df, how="left", on=["given_name", "surname"]
)
# %%
treatments_df.sample(4)
# %%
treatments_df["dosage_start"] = treatments_df["dosage_start"].astype("int")
treatments_df["dosage_end"] = treatments_df["dosage_end"].astype("int")
treatments_df["given_name"] = treatments_df["given_name"].str.capitalize()
treatments_df["surname"] = treatments_df["surname"].str.capitalize()
# %%
treatments_df
"""typo in name of the patient_id 9 --->accuracy

short forms in state --->consistency

problem in zip code it sholud be in 5 digit some contains 4 digit--->validity

some patients do not contains address and zip ,stae ,city ,country contact --->completeness

there are 5 given_name and surname == john doe---> accuracy

one patients have weight == 48 which i wrong --->accuracy

one patients have height == 4.411297 which is wrong --->accuracy

incorrect data type data type of birthday to datetype--->validity

incorrect data type of zip code--->validity

incorect datat type for sex --"""


#  %%
patients_df
