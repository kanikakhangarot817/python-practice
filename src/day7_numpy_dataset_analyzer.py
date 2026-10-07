import numpy as np


class NumpyDatasetAnalyzer:

    def __init__(self, data):
        self.data = data
        self.array = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Dataset must be a list.")

        if len(self.data) == 0:
            raise ValueError("Dataset cannot be empty.")

        for row in self.data:
            if not isinstance(row, list):
                raise TypeError("Each row must be a list.")

        column_count = len(self.data[0])

        if column_count == 0:
            raise ValueError("Rows cannot be empty.")

        for row in self.data:
            if len(row) != column_count:
                raise ValueError(
                    "All rows must contain the same number of columns."
                )

        for row in self.data:
            for value in row:
                if not isinstance(value, (int, float, np.number)):
                    raise TypeError(
                        "Dataset contains non-numeric values."
                    )

    def convert_to_array(self):
        self.array = np.array(self.data)
        return self.array

    def get_dataset_info(self):
        rows, columns = self.array.shape

        print("\n===== DATASET INFORMATION =====")
        print("Rows:", rows)
        print("Columns:", columns)
        print("Dimensions:", self.array.ndim)
        print("Size:", self.array.size)
        print("Data Type:", self.array.dtype)

    def get_column(self, column_index):
        return self.array[:, column_index]

    def get_row(self, row_index):
        return self.array[row_index, :]

    def calculate_column_mean(self):
        return np.mean(self.array, axis=0)

    def calculate_column_minimum(self):
        return np.min(self.array, axis=0)

    def calculate_column_maximum(self):
        return np.max(self.array, axis=0)

    def calculate_column_std(self):
        return np.std(self.array, axis=0)

    def scale_features(self):
        minimum = np.min(self.array, axis=0)
        maximum = np.max(self.array, axis=0)

        denominator = maximum - minimum

        denominator = np.where(denominator == 0, 1, denominator)

        scaled = (self.array - minimum) / denominator

        return scaled

    def feature_summary(self):
        return {
            "mean": self.calculate_column_mean(),
            "minimum": self.calculate_column_minimum(),
            "maximum": self.calculate_column_maximum(),
            "std": self.calculate_column_std()
        }

    def split_features_target(self, target_index):
        X = np.delete(self.array, target_index, axis=1)
        y = self.array[:, target_index]

        return X, y

    def display_report(self):
        self.get_dataset_info()

        print("\n===== ROW AND COLUMN EXTRACTION =====")
        print("First Column:", self.get_column(0))
        print("First Row:", self.get_row(0))

        print("\n===== FEATURE STATISTICS =====")
        print("Column Mean:", self.calculate_column_mean())
        print("Column Minimum:", self.calculate_column_minimum())
        print("Column Maximum:", self.calculate_column_maximum())
        print("Column Standard Deviation:", self.calculate_column_std())

        print("\n===== SCALED FEATURES =====")
        print(self.scale_features())

        print("\n===== FEATURE SUMMARY =====")
        summary = self.feature_summary()

        print("Mean:", summary["mean"])
        print("Minimum:", summary["minimum"])
        print("Maximum:", summary["maximum"])
        print("Standard Deviation:", summary["std"])

        print("\n===== X AND y =====")
        X, y = self.split_features_target(2)

        print("X (Features):")
        print(X)

        print("y (Target):")
        print(y)


def main():

    data = [
        [25, 30000, 2],
        [30, 45000, 5],
        [35, 60000, 8],
        [40, 80000, 12],
        [45, 100000, 15]
    ]

    analyzer = NumpyDatasetAnalyzer(data)

    try:
        analyzer.validate_input()
        analyzer.convert_to_array()
        analyzer.display_report()

    except (TypeError, ValueError) as e:
        print("Error:", e)


if __name__ == "__main__":
    main()