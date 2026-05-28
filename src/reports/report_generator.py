import pandas as pd


def generate_reports(df: pd.DataFrame) -> None:
    reserve_report = df[
        [
            "policy_id",
            "insured_id",
            "product_type",
            "policy_status",
            "current_age",
            "face_amount",
            "annual_premium",
            "expected_claim",
            "reserve"
        ]
    ]

    reinsurance_report = df[
        [
            "policy_id",
            "insured_id",
            "issue_year",
            "product_type",
            "face_amount",
            "retention_limit",
            "reinsured_amount",
            "ceded_premium"
        ]
    ]

    premium_report = df[
        [
            "policy_id",
            "insured_id",
            "product_type",
            "payment_mode",
            "annual_premium",
            "ceded_premium"
        ]
    ]

    reserve_report.to_csv("output/reserve_report.csv", index=False)
    reinsurance_report.to_csv("output/reinsurance_report.csv", index=False)
    premium_report.to_csv("output/premium_report.csv", index=False)