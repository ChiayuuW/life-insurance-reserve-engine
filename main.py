import pandas as pd

from src.assumptions.mortality import load_mortality_table
from src.valuation.reserve_engine import value_policies
from src.reinsurance.reinsurance_engine import apply_reinsurance
from src.reports.report_generator import generate_reports


def main():
    policy_df = pd.read_csv("data/policies.csv")
    mortality_table = load_mortality_table("data/mortality_table.csv")

    valuation_df = value_policies(policy_df, mortality_table)
    final_df = apply_reinsurance(valuation_df)

    generate_reports(final_df)

    print("Reserve engine completed successfully.")
    print(final_df)


if __name__ == "__main__":
    main()