class FrequencyCounter:
    def __init__(self, numbers):
        self.numbers = numbers

    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Input list cannot be empty.")

    def count_frequency(self):
        frequency = {}

        for num in self.numbers:
            if num in frequency:
                frequency[num] += 1
            else:
                frequency[num] = 1

        return frequency

    def display_result(self):
        result = self.count_frequency()
        print(result)


def main():
    numbers = [1, 2, 2, 3, 1, 5, 4, 2, 5, 5]

    try:
        counter = FrequencyCounter(numbers)
        counter.validate_input()
        counter.display_result()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()