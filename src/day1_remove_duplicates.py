class RemoveDuplicates:
    """
    A class to remove duplicate values from a list
    while preserving the original order.
    """

    def __init__(self, numbers):
        """
        Initialize the object with a list of numbers.

        Parameters:
            numbers (list): List containing integer values.
        """
        self.numbers = numbers

    def validate_input(self):
        """
        Validate that the input is a list.

        Raises:
            TypeError: If input is not a list.
        """
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

    def remove_duplicates(self):
        """
        Remove duplicate values while preserving order.

        Returns:
            list: List containing only unique values.
        """
        unique_numbers = []

        for value in self.numbers:
            if value not in unique_numbers:
                unique_numbers.append(value)

        return unique_numbers

    def display_result(self):
        """
        Display the original list and the unique list.
        """
        unique_list = self.remove_duplicates()

        print("Original List :", self.numbers)
        print("Unique List   :", unique_list)


def main():
    """
    Main function of the program.
    """
    numbers = [10, 20, 10, 30, 40, 20, 50, 30]

    try:
        obj = RemoveDuplicates(numbers)

        obj.validate_input()

        obj.display_result()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()