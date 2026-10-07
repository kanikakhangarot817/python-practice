import os
import pandas as pd
import numpy as np


class CustomerDataPipeline:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.summary = {}

    # ---------------------------------------------------------
    # 1. Validate File
    # ---------------------------------------------------------
    def validate_file(self):
        if not isinstance(self.file_path, str):
            raise TypeError("File path must be a string.")

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"CSV file does not exist: {self.file_path}"
            )

        if not self.file_path.lower().endswith(".csv"):
            raise ValueError("Only CSV files are supported.")

        print("File validation successful.")

    # ---------------------------------------------------------
    # 2. Load CSV Data
    # ---------------------------------------------------------
    def load_data(self):
        self.df = pd.read_csv(self.file_path)

        print("\nDataset loaded successfully.")
        print(self.df)

    # ---------------------------------------------------------
    # 3. Validate Required Columns
    # ---------------------------------------------------------
    def validate_columns(self):
        required_columns = [
            "CustomerID",
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in self.df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Required columns are missing: {missing_columns}"
            )

        print("\nColumn validation successful.")

    # ---------------------------------------------------------
    # 4. Inspect Dataset
    # ---------------------------------------------------------
    def inspect_dataset(self):
        print("\n--- DATASET INSPECTION ---")

        print("Shape:", self.df.shape)
        print("Row Count:", self.df.shape[0])
        print("Column Count:", self.df.shape[1])

        print("\nColumn Names:")
        print(self.df.columns.tolist())

        print("\nData Types:")
        print(self.df.dtypes)

        print("\nMemory Information:")
        self.df.info()

    # ---------------------------------------------------------
    # 5. Generate Data Quality Report
    # ---------------------------------------------------------
    def generate_quality_report(self):
        print("\n--- DATA QUALITY REPORT ---")

        total_rows = len(self.df)

        quality_report = pd.DataFrame({
            "Data Type": self.df.dtypes.astype(str),
            "Missing Count": self.df.isnull().sum(),
            "Missing Percentage":
                (self.df.isnull().sum() / total_rows) * 100,
            "Unique Values": self.df.nunique()
        })

        print(quality_report)

        self.summary["quality_report"] = quality_report

        return quality_report

    # ---------------------------------------------------------
    # 6. Find Duplicate Records
    # ---------------------------------------------------------
    def find_duplicates(self):
        duplicates = self.df[self.df.duplicated()]

        print("\n--- DUPLICATE RECORDS ---")

        if duplicates.empty:
            print("No duplicate records found.")
        else:
            print(duplicates)
            print(
                "Number of duplicate records:",
                len(duplicates)
            )

        return duplicates

    # ---------------------------------------------------------
    # 7. Remove Duplicate Records
    # ---------------------------------------------------------
    def remove_duplicates(self):
        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\n--- DUPLICATE REMOVAL ---")
        print("Original rows:", len(self.df))
        print("Rows after removing duplicates:",
              len(self.cleaned_df))

    # ---------------------------------------------------------
    # 8. Handle Missing Values
    # ---------------------------------------------------------
    def handle_missing_values(self):
        numerical_columns = [
            "Age",
            "Income",
            "PurchaseAmount"
        ]

        print("\n--- MISSING VALUE HANDLING ---")

        for column in numerical_columns:

            missing_before = self.cleaned_df[column].isnull().sum()

            if missing_before > 0:

                median_value = self.cleaned_df[column].median()

                self.cleaned_df[column] = (
                    self.cleaned_df[column].fillna(median_value)
                )

                print(
                    f"{column}: "
                    f"{missing_before} missing value(s) "
                    f"filled with median {median_value}"
                )

        print("Missing value handling completed.")

    # ---------------------------------------------------------
    # 9. Detect Invalid Values
    # ---------------------------------------------------------
    def detect_invalid_values(self):
        print("\n--- INVALID VALUE CHECK ---")

        invalid_found = False

        # Age must be greater than 0
        invalid_age = self.cleaned_df[
            self.cleaned_df["Age"] <= 0
        ]

        if not invalid_age.empty:
            print("Invalid Age values detected:")
            print(invalid_age)
            invalid_found = True

        # Income must be >= 0
        invalid_income = self.cleaned_df[
            self.cleaned_df["Income"] < 0
        ]

        if not invalid_income.empty:
            print("Invalid Income values detected:")
            print(invalid_income)
            invalid_found = True

        # Experience must be >= 0
        invalid_experience = self.cleaned_df[
            self.cleaned_df["Experience"] < 0
        ]

        if not invalid_experience.empty:
            print("Invalid Experience values detected:")
            print(invalid_experience)
            invalid_found = True

        # PurchaseAmount must be >= 0
        invalid_purchase = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] < 0
        ]

        if not invalid_purchase.empty:
            print("Invalid PurchaseAmount values detected:")
            print(invalid_purchase)
            invalid_found = True

        # Purchased must be 0 or 1
        invalid_purchased = self.cleaned_df[
            ~self.cleaned_df["Purchased"].isin([0, 1])
        ]

        if not invalid_purchased.empty:
            print("Invalid Purchased values detected:")
            print(invalid_purchased)
            invalid_found = True

        if not invalid_found:
            print("No invalid values detected.")

        return invalid_found

    # ---------------------------------------------------------
    # 10. Validate Cleaned Data
    # ---------------------------------------------------------
    def validate_cleaned_data(self):
        print("\n--- CLEANED DATA VALIDATION ---")

        # Check missing values
        total_missing = self.cleaned_df.isnull().sum().sum()

        if total_missing > 0:
            raise ValueError(
                "Missing values still exist after cleaning."
            )

        # Check duplicates
        duplicate_count = self.cleaned_df.duplicated().sum()

        if duplicate_count > 0:
            raise ValueError(
                "Duplicate records still exist after cleaning."
            )

        # Check numerical data types
        numerical_columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount"
        ]

        for column in numerical_columns:
            if not pd.api.types.is_numeric_dtype(
                self.cleaned_df[column]
            ):
                raise TypeError(
                    f"{column} must be numeric."
                )

        # Check Purchased values
        if not self.cleaned_df["Purchased"].isin([0, 1]).all():
            raise ValueError(
                "Purchased must contain only 0 or 1."
            )

        print("Cleaned data validation successful.")

    # ---------------------------------------------------------
    # 11. Create Features
    # ---------------------------------------------------------
    def create_features(self):

        # Income per Experience
        self.cleaned_df["IncomePerExperience"] = np.where(
            self.cleaned_df["Experience"] == 0,
            0,
            self.cleaned_df["Income"] /
            self.cleaned_df["Experience"]
        )

        # Purchase Category
        self.cleaned_df["PurchaseCategory"] = np.select(
            [
                self.cleaned_df["PurchaseAmount"] < 2000,
                self.cleaned_df["PurchaseAmount"].between(
                    2000, 5000
                ),
                self.cleaned_df["PurchaseAmount"] > 5000
            ],
            [
                "Low",
                "Medium",
                "High"
            ],
            default="Unknown"
        )

        print("\n--- FEATURE ENGINEERING ---")
        print("Created:")
        print("1. IncomePerExperience")
        print("2. PurchaseCategory")

    # ---------------------------------------------------------
    # 12. Create Age Group
    # ---------------------------------------------------------
    def create_age_group(self):

        self.cleaned_df["AgeGroup"] = np.select(
            [
                self.cleaned_df["Age"] < 30,
                self.cleaned_df["Age"].between(30, 40),
                self.cleaned_df["Age"] > 40
            ],
            [
                "Young",
                "Adult",
                "Senior"
            ],
            default="Unknown"
        )

        print("3. AgeGroup created.")

    # ---------------------------------------------------------
    # 13. Get High Value Customers
    # ---------------------------------------------------------
    def get_high_value_customers(self):

        high_value_customers = self.cleaned_df[
            self.cleaned_df["PurchaseAmount"] > 5000
        ]

        print("\n--- HIGH VALUE CUSTOMERS ---")

        if high_value_customers.empty:
            print("No high-value customers found.")
        else:
            print(high_value_customers)

        return high_value_customers

    # ---------------------------------------------------------
    # 14. Sort By Purchase Amount
    # ---------------------------------------------------------
    def sort_by_purchase_amount(self):

        sorted_data = self.cleaned_df.sort_values(
            by="PurchaseAmount",
            ascending=False
        )

        print("\n--- SORTED BY PURCHASE AMOUNT ---")
        print(sorted_data)

        return sorted_data

    # ---------------------------------------------------------
    # 15. Calculate Statistics
    # ---------------------------------------------------------
    def calculate_statistics(self):

        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "IncomePerExperience"
        ]

        statistics = self.cleaned_df[columns].agg([
            "mean",
            "median",
            "min",
            "max",
            "std"
        ])

        print("\n--- STATISTICS ---")
        print(statistics)

        self.summary["statistics"] = statistics

        return statistics

    # ---------------------------------------------------------
    # 16. Calculate Correlation
    # ---------------------------------------------------------
    def calculate_correlation(self):

        columns = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "Purchased"
        ]

        correlation = self.cleaned_df[columns].corr()

        print("\n--- CORRELATION MATRIX ---")
        print(correlation)

        self.summary["correlation"] = correlation

        return correlation

    # ---------------------------------------------------------
    # 17. Analyze By Purchase Status
    # ---------------------------------------------------------
    def analyze_by_purchase_status(self):

        result = self.cleaned_df.groupby(
            "Purchased"
        ).agg(
            CustomerCount=("CustomerID", "count"),
            AverageAge=("Age", "mean"),
            AverageIncome=("Income", "mean"),
            AveragePurchaseAmount=(
                "PurchaseAmount",
                "mean"
            )
        )

        print("\n--- PURCHASE STATUS ANALYSIS ---")
        print(result)

        self.summary["purchase_status_analysis"] = result

        return result

    # ---------------------------------------------------------
    # 18. Perform EDA
    # ---------------------------------------------------------
    def perform_eda(self):

        total_customers = len(self.cleaned_df)

        average_age = self.cleaned_df["Age"].mean()

        average_income = self.cleaned_df["Income"].mean()

        median_income = self.cleaned_df["Income"].median()

        highest_purchase = (
            self.cleaned_df["PurchaseAmount"].max()
        )

        average_purchase = (
            self.cleaned_df["PurchaseAmount"].mean()
        )

        purchasers = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        non_purchasers = (
            self.cleaned_df["Purchased"] == 0
        ).sum()

        most_common_age_group = (
            self.cleaned_df["AgeGroup"].mode()[0]
        )

        most_common_purchase_category = (
            self.cleaned_df["PurchaseCategory"].mode()[0]
        )

        self.summary["total_customers"] = total_customers
        self.summary["average_age"] = average_age
        self.summary["average_income"] = average_income
        self.summary["median_income"] = median_income
        self.summary["highest_purchase"] = highest_purchase
        self.summary["average_purchase"] = average_purchase
        self.summary["purchasers"] = purchasers
        self.summary["non_purchasers"] = non_purchasers
        self.summary["most_common_age_group"] = (
            most_common_age_group
        )
        self.summary["most_common_purchase_category"] = (
            most_common_purchase_category
        )

        print("\n--- EDA SUMMARY ---")

        print("Total Customers:", total_customers)
        print("Average Age:", average_age)
        print("Average Income:", average_income)
        print("Median Income:", median_income)
        print("Highest Purchase:", highest_purchase)
        print("Average Purchase:", average_purchase)
        print("Purchasers:", purchasers)
        print("Non-Purchasers:", non_purchasers)
        print(
            "Most Common Age Group:",
            most_common_age_group
        )
        print(
            "Most Common Purchase Category:",
            most_common_purchase_category
        )

        return self.summary

    # ---------------------------------------------------------
    # 19. Export Cleaned Data
    # ---------------------------------------------------------
    def export_clean_data(self):

        output_directory = "output"

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        output_path = os.path.join(
            output_directory,
            "cleaned_customer_data.csv"
        )

        self.cleaned_df.to_csv(
            output_path,
            index=False
        )

        print(
            "\nCleaned dataset exported successfully to:"
        )
        print(output_path)

    # ---------------------------------------------------------
    # 20. Bonus - Generate ML Ready Data
    # ---------------------------------------------------------
    def generate_ml_ready_data(self):

        features = [
            "Age",
            "Income",
            "Experience",
            "PurchaseAmount",
            "IncomePerExperience"
        ]

        X = self.cleaned_df[features]

        y = self.cleaned_df["Purchased"]

        print("\n--- ML READY DATA ---")

        print("\nFeatures (X):")
        print(X)

        print("\nTarget (y):")
        print(y)

        return X, y

    # ---------------------------------------------------------
    # 21. Run Complete Pipeline
    # ---------------------------------------------------------
    def run_pipeline(self):

        print("=" * 60)
        print("CUSTOMER DATA PIPELINE")
        print("=" * 60)

        # Step 1
        self.validate_file()

        # Step 2
        self.load_data()

        # Step 3
        self.validate_columns()

        # Step 4
        self.inspect_dataset()

        # Step 5
        self.generate_quality_report()

        # Step 6
        self.find_duplicates()

        # Step 7
        self.remove_duplicates()

        # Step 8
        self.handle_missing_values()

        # Step 9
        self.detect_invalid_values()

        # Step 10
        self.validate_cleaned_data()

        # Step 11
        self.create_features()

        # Step 12
        self.create_age_group()

        # Step 13
        self.get_high_value_customers()

        # Step 14
        self.sort_by_purchase_amount()

        # Step 15
        self.calculate_statistics()

        # Step 16
        self.calculate_correlation()

        # Step 17
        self.analyze_by_purchase_status()

        # Step 18
        self.perform_eda()

        # Step 19
        self.export_clean_data()

        # Step 20 - Bonus
        self.generate_ml_ready_data()

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)


# -------------------------------------------------------------
# Main Function
# -------------------------------------------------------------
def main():

    file_path = "data/customer_data.csv"

    pipeline = CustomerDataPipeline(file_path)

    try:
        pipeline.run_pipeline()

    except FileNotFoundError as e:
        print("\nERROR:", e)

    except ValueError as e:
        print("\nERROR:", e)

    except TypeError as e:
        print("\nERROR:", e)

    except Exception as e:
        print("\nUNEXPECTED ERROR:", e)


# -------------------------------------------------------------
# Program Entry Point
# -------------------------------------------------------------
if __name__ == "__main__":
    main()