class MissingValueHandler:
    def __init__(self, data):
        self.data = data
        self.cleaned_data = list(data)

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is not None and not isinstance(value, (int, float)):
                raise TypeError("Dataset contains invalid values.")

    def count_missing(self):
        count = 0
        for value in self.data:
            if value is None:
                count += 1
        return count

    def get_missing_indexes(self):
        indexes = []
        for index in range(len(self.data)):
            if self.data[index] is None:
                indexes.append(index)
        return indexes

    def get_available_values(self):
        values = []
        for value in self.data:
            if value is not None:
                values.append(value)
        return values

    def calculate_mean(self):
        values = self.get_available_values()

        if len(values) == 0:
            raise ValueError("No valid values exist to calculate the mean.")

        total = 0
        for value in values:
            total += value

        mean = total / len(values)
        return round(mean, 2)

    def fill_with_mean(self):
        mean = self.calculate_mean()

        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(mean)
            else:
                self.cleaned_data.append(value)

        return self.cleaned_data

    def fill_with_median(self):
        values = self.get_available_values()

        if len(values) == 0:
            raise ValueError("No valid values exist to calculate the median.")

        values.sort()
        n = len(values)

        if n % 2 == 1:
            median = values[n // 2]
        else:
            median = (values[n // 2 - 1] + values[n // 2]) / 2

        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(median)
            else:
                self.cleaned_data.append(value)

        return self.cleaned_data

    def fill_with_zero(self):
        self.cleaned_data = []

        for value in self.data:
            if value is None:
                self.cleaned_data.append(0)
            else:
                self.cleaned_data.append(value)

        return self.cleaned_data

    def fill_missing_values(self, strategy):
        if strategy == "mean":
            return self.fill_with_mean()
        elif strategy == "median":
            return self.fill_with_median()
        elif strategy == "zero":
            return self.fill_with_zero()
        else:
            raise ValueError("Invalid strategy. Choose: mean, median, or zero.")

    def display_report(self):
        mean = self.calculate_mean()
        cleaned = self.fill_with_mean()

        print("\n        MISSING VALUE REPORT")
        print("========================================")

        print("\nOriginal Data:")
        print(self.data)

        print(f"\nTotal Values       : {len(self.data)}")
        print(f"Missing Values     : {self.count_missing()}")
        print(f"Missing Indexes    : {self.get_missing_indexes()}")
        print(f"Available Values   : {len(self.get_available_values())}")
        print(f"Mean               : {mean}")

        print("\nCleaned Data:")
        print(cleaned)

        print("\n========================================")


if __name__ == "__main__":
    try:
        # Change this dataset to test different test cases
        data = [25, 30, None, 40, None, 35, 28]

        handler = MissingValueHandler(data)

        handler.validate_input()

        handler.display_report()

        # Bonus examples
        print("\nFill with median:", handler.fill_missing_values("median"))
        print("Fill with zero:", handler.fill_missing_values("zero"))

    except Exception as e:
        print("Error:", e)