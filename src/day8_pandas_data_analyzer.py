import pandas as pd

class PandasDataAnalyzer:

    REQUIRED_COLUMNS = [
        "Customer",
        "Age",
        "Income",
        "Experience",
        "Purchased"
    ]

    def __init__(self, data):
        self.data = data
        self.df = None
        self.cleaned_df = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input data must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input dataset cannot be empty.")

        for record in self.data:
            if not isinstance(record, (list, tuple)):
                raise TypeError("Each record must be a list or tuple.")

            if len(record) != len(self.REQUIRED_COLUMNS):
                raise ValueError(
                    "Each record must contain exactly 5 values."
                )

        return True

    def create_dataframe(self):
        self.df = pd.DataFrame(
            self.data,
            columns=self.REQUIRED_COLUMNS
        )

        return self.df

    def get_dataset_info(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        print("\n===== DATASET INFORMATION =====")
        print("Rows:", self.df.shape[0])
        print("Columns:", self.df.shape[1])
        print("Column Names:", list(self.df.columns))
        print("\nData Types:")
        print(self.df.dtypes)
        print("\nShape:", self.df.shape)

    def find_missing_values(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        missing = self.df.isnull()

        print("\n===== MISSING VALUE LOCATIONS =====")
        print(missing)

        return missing

    def count_missing_values(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        missing_counts = self.df.isnull().sum()

        print("\n===== MISSING VALUE COUNTS =====")
        print(missing_counts)

        return missing_counts

    def find_duplicates(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        duplicate_count = self.df.duplicated().sum()

        print("\n===== DUPLICATE RECORDS =====")
        print("Duplicate Records:", duplicate_count)

        return duplicate_count

    def remove_duplicates(self):
        if self.df is None:
            raise ValueError("DataFrame has not been created.")

        self.cleaned_df = self.df.drop_duplicates().copy()

        print("\n===== DUPLICATE REMOVAL =====")
        print("Original Rows:", len(self.df))
        print("Rows After Cleaning:", len(self.cleaned_df))

        return self.cleaned_df

    def fill_missing_values(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        mean_income = self.cleaned_df["Income"].mean()

        self.cleaned_df["Income"] = (
            self.cleaned_df["Income"].fillna(mean_income)
        )

        print("\n===== MISSING VALUE IMPUTATION =====")
        print("Mean Income Used:", mean_income)

        return self.cleaned_df

    def filter_customers(self, min_income):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        filtered = self.cleaned_df[
            self.cleaned_df["Income"] >= min_income
        ]

        print(f"\n===== CUSTOMERS WITH INCOME >= {min_income} =====")
        print(filtered)

        return filtered

    def sort_by_income(self, ascending=True):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        sorted_df = self.cleaned_df.sort_values(
            by="Income",
            ascending=ascending
        )

        print("\n===== SORTED BY INCOME =====")
        print(sorted_df)

        return sorted_df

    def calculate_statistics(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        numerical_columns = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        statistics = {}

        for column in numerical_columns:
            statistics[column] = {
                "Mean": self.cleaned_df[column].mean(),
                "Minimum": self.cleaned_df[column].min(),
                "Maximum": self.cleaned_df[column].max(),
                "Std Dev": self.cleaned_df[column].std()
            }

        print("\n===== STATISTICS =====")

        for column, values in statistics.items():
            print(f"\n{column}")

            for name, value in values.items():
                print(f"{name}: {value:.2f}")

        return statistics

    def analyze_features(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        features = [
            "Age",
            "Income",
            "Experience",
            "Purchased"
        ]

        print("\n===== FEATURE ANALYSIS =====")

        for feature in features:
            print(f"\n{feature}")
            print("Mean:", self.cleaned_df[feature].mean())
            print("Minimum:", self.cleaned_df[feature].min())
            print("Maximum:", self.cleaned_df[feature].max())
            print("Std Dev:", self.cleaned_df[feature].std())

    def analyze_target(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        purchased = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        not_purchased = (
            self.cleaned_df["Purchased"] == 0
        ).sum()

        print("\n===== PURCHASE ANALYSIS =====")
        print("Purchased:", purchased)
        print("Not Purchased:", not_purchased)

        return purchased, not_purchased

    def perform_eda(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        customer_count = len(self.cleaned_df)
        average_age = self.cleaned_df["Age"].mean()
        average_income = self.cleaned_df["Income"].mean()
        highest_income = self.cleaned_df["Income"].max()
        average_experience = self.cleaned_df["Experience"].mean()

        number_of_purchasers = (
            self.cleaned_df["Purchased"] == 1
        ).sum()

        print("\n===== EDA =====")
        print("Customer Count:", customer_count)
        print("Average Age:", average_age)
        print("Average Income:", average_income)
        print("Highest Income:", highest_income)
        print("Average Experience:", average_experience)
        print("Number of Purchasers:", number_of_purchasers)

        return {
            "Customer Count": customer_count,
            "Average Age": average_age,
            "Average Income": average_income,
            "Highest Income": highest_income,
            "Average Experience": average_experience,
            "Number of Purchasers": number_of_purchasers
        }

    def group_by_purchase_status(self):
        if self.cleaned_df is None:
            raise ValueError("Cleaned DataFrame has not been created.")

        grouped = self.cleaned_df.groupby("Purchased").agg(
            Customer_Count=("Customer", "count"),
            Average_Age=("Age", "mean"),
            Average_Income=("Income", "mean"),
            Average_Experience=("Experience", "mean")
        )

        print("\n===== GROUP BY PURCHASE STATUS =====")
        print(grouped)

        return grouped

    def display_report(self):
        if self.df is None or self.cleaned_df is None:
            raise ValueError(
                "Dataset must be created and cleaned first."
            )

        missing_income = self.df["Income"].isnull().sum()
        duplicate_records = self.df.duplicated().sum()

        print("\n" + "=" * 50)
        print("        CUSTOMER DATA ANALYSIS")
        print("=" * 50)

        print("Original Dataset Shape:", self.df.shape)
        print("Missing Income Values:", missing_income)
        print("Duplicate Records:", duplicate_records)
        print("Rows After Cleaning:", len(self.cleaned_df))

        print("\nFeature Statistics:")
        self.calculate_statistics()

        print("\nPurchase Analysis:")
        purchased, not_purchased = self.analyze_target()

        print("Purchased:", purchased)
        print("Not Purchased:", not_purchased)

        print("=" * 50)


def main():

    data = [
        ["C001", 25, 30000, 2, 0],
        ["C002", 30, 45000, 5, 1],
        ["C003", 35, None, 8, 1],
        ["C004", 40, 80000, 12, 1],
        ["C005", 45, 100000, 15, 0],
        ["C002", 30, 45000, 5, 1]
    ]

    try:
        analyzer = PandasDataAnalyzer(data)

        analyzer.validate_input()
        analyzer.create_dataframe()

        analyzer.get_dataset_info()
        analyzer.find_missing_values()
        analyzer.count_missing_values()
        analyzer.find_duplicates()

        analyzer.remove_duplicates()
        analyzer.fill_missing_values()

        analyzer.filter_customers(50000)
        analyzer.sort_by_income()
        analyzer.sort_by_income(ascending=False)

        analyzer.calculate_statistics()
        analyzer.analyze_features()
        analyzer.perform_eda()
        analyzer.analyze_target()

        analyzer.group_by_purchase_status()

        analyzer.display_report()

    except (TypeError, ValueError) as error:
        print("\nError:", error)

    except Exception as error:
        print("\nUnexpected error:", error)


if __name__ == "__main__":
    main()