import pandas as pd


def get_retention_limit(issue_year: int) -> float:
    if issue_year < 2018:
        return 3_000_000
    return 2_000_000


def calculate_reinsured_amount(face_amount: float, retention_limit: float) -> float:
    return max(0, face_amount - retention_limit)


def calculate_ceded_premium(reinsured_amount: float, reinsurance_rate: float = 0.0015) -> float:
    return reinsured_amount * reinsurance_rate


def apply_reinsurance(valuation_df: pd.DataFrame) -> pd.DataFrame:
    df = valuation_df.copy()

    df["retention_limit"] = df["issue_year"].apply(get_retention_limit)

    df["reinsured_amount"] = df.apply(
        lambda row: calculate_reinsured_amount(
            row["face_amount"],
            row["retention_limit"]
        ),
        axis=1
    )

    df["ceded_premium"] = df["reinsured_amount"].apply(calculate_ceded_premium)

    df["net_amount_at_risk"] = df["face_amount"] - df["reserve"]

    return df