import pandas as pd


def load_mortality_table(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def get_mortality_rate(age: int, gender: str, mortality_table: pd.DataFrame) -> float:
    row = mortality_table[mortality_table["age"] == age]

    if row.empty:
        raise ValueError(f"No mortality rate found for age {age}")
    if gender.upper() == "M":
        return float(row.iloc[0]["male_qx"])
    elif gender.upper() == "F":
        return float(row.iloc[0]["female_qx"])
    else:
        raise ValueError(f"Invalid gender: {gender}")