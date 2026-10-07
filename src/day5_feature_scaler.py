class FeatureScaler:
    def __init__(self, data):
        self.data = data
        self.scaled_data = []

    def validate_input(self):
        if not isinstance(self.data, list):
            raise TypeError("Input must be a list.")

        if len(self.data) == 0:
            raise ValueError("Input list cannot be empty.")

        for value in self.data:
            if value is None:
                raise ValueError("None values are not allowed.")

            if not isinstance(value, (int, float)):
                raise TypeError("Dataset contains invalid values.")

        return True

    def find_minimum(self):
        return min(self.data)

    def find_maximum(self):
        return max(self.data)

    def scale_data(self):
        minimum = self.find_minimum()
        maximum = self.find_maximum()

        if minimum == maximum:
            raise ValueError(
                "Cannot scale data because all values are identical."
            )

        self.scaled_data = []

        for value in self.data:
            scaled = (value - minimum) / (maximum - minimum)
            self.scaled_data.append(round(scaled, 4))

        return self.scaled_data

    def display_report(self):
        self.scale_data()

        print("========================================")
        print("         FEATURE SCALING REPORT")
        print("========================================")
        print()
        print("Original Data :", self.data)
        print()
        print("Minimum       :", self.find_minimum())
        print("Maximum       :", self.find_maximum())
        print()
        print("Scaled Data   :", self.scaled_data)
        print()
        print("========================================")


def main():
    try:
        data = [10, 20, 30, 40, 50]

        obj = FeatureScaler(data)

        obj.validate_input()

        obj.display_report()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()