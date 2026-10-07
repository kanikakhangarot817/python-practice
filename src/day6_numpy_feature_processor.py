import numpy as np

class NumpyFeatureProcessor:

    def __init__(self, data):
        self.data = data
        self.array = None
        self.min_max_data = None
        self.standardized_data = None

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        if not all(isinstance(value, (int, float)) for value in self.data):
            raise TypeError("Dataset contains non-numeric values.")

    def convert_to_array(self):
        self.array = np.array(self.data)

    def get_array_info(self):
        print("\nNumPy Array:")
        print(self.array)
        print("Data Type:", self.array.dtype)
        print("Dimensions:", self.array.ndim)
        print("Shape:", self.array.shape)
        print("Size:", self.array.size)

    def calculate_minimum(self):
        return np.min(self.array)

    def calculate_maximum(self):
        return np.max(self.array)

    def calculate_mean(self):
        return np.mean(self.array)

    def calculate_standard_deviation(self):
        return np.std(self.array)

    def min_max_scale(self):
        minimum = self.calculate_minimum()
        maximum = self.calculate_maximum()

        if maximum == minimum:
            raise ValueError(
                "Min-Max Scaling cannot be performed because all values are constant."
            )

        self.min_max_data = (
            self.array - minimum
        ) / (maximum - minimum)

        return self.min_max_data

    def standardize(self):
        mean = self.calculate_mean()
        standard_deviation = self.calculate_standard_deviation()

        if standard_deviation == 0:
            raise ValueError(
                "Z-Score Standardization cannot be performed because standard deviation is zero."
            )

        self.standardized_data = (
            self.array - mean
        ) / standard_deviation

        return self.standardized_data

    def display_report(self):
        print("=" * 50)
        print("       NUMPY FEATURE PROCESSING REPORT")
        print("=" * 50)

        print("\nOriginal Data:")
        print(self.data)

        self.get_array_info()

        print("\nMinimum:", self.calculate_minimum())
        print("Maximum:", self.calculate_maximum())
        print("Mean:", self.calculate_mean())
        print(
            "Standard Deviation:",
            round(self.calculate_standard_deviation(), 4)
        )

        print("\nMin-Max Scaled:")
        print(np.round(self.min_max_scale(), 4))

        print("\nZ-Score Standardized:")
        print(np.round(self.standardize(), 4))

        print("\n" + "=" * 50)


def main():
    data = [10, 20, 30, 40, 50]

    try:
        obj = NumpyFeatureProcessor(data)

        obj.validate_input()
        obj.convert_to_array()
        obj.display_report()

    except (TypeError, ValueError) as error:
        print("Error:", error)


if __name__ == "__main__":
    main()