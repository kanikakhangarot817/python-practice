class Statistical_analyzer:
    def __init__(self, numbers):
            self.numbers = numbers
            numbers = [10,20,20,30,40,50]
            analyzer = Statistical_analyzer(numbers)
    def validate_input(self):
        if not isinstance(self.numbers, list):
            raise TypeError("Input must be a list.")

        if len(self.numbers) == 0:
            raise ValueError("Input list cannot be empty.")
        
        for value in self.numbers:
            if not isinstance(value, (int, float)):
             raise TypeError("Input must contain only numerical values.")
    
    def calculate_mean(self):
         total = 0
         for value in self.numbers:
          total += value
         return total / len(self.numbers)
    def calculate_median(self):
         data = sorted(self.numbers)
         n = len(data)
         mid = n // 2

         if n % 2 == 1:
            return data[mid]
         else:
            return (data[mid - 1] + data[mid]) / 2
        
    def calculate_mode(self):
         frequency = {}

         for value in self.numbers:
          if value in frequency:
            frequency[value] += 1
         else:
            frequency[value] = 1

         max_count = max(frequency.values())

         if max_count == 1:
           return "No unique mode"

         modes = []

         for key, value in frequency.items():
          if value == max_count:
            modes.append(key)

         if len(modes) == 1:
          return modes[0]

         return modes
    def find_minimum(self):
         minimum = self.numbers[0]

         for value in self.numbers:
          if value < minimum:
             minimum = value

         return minimum
    def find_maximum(self):
          maximum = self.numbers[0]

          for value in self.numbers:
           if value > maximum:
            maximum = value

          return maximum
    def count_unique_values(self):
         unique = {}

         for value in self.numbers:
          unique[value] = True

         return len(unique)
    def calculate_range(self):
          return self.find_maximum() - self.find_minimum()
      
    def calculate_variance(self):
         mean = self.calculate_mean()
         total = 0

         for value in self.numbers:
          total += (value - mean) ** 2

         return total / len(self.numbers)
    def display_result(self):
         print("================================")
         print("       STATISTICAL REPORT")
         print("================================")
         print(f"Original Data : {self.numbers}")
         print()
         print(f"Mean          : {self.calculate_mean():.2f}")
         print(f"Median        : {self.calculate_median()}")
         print(f"Mode          : {self.calculate_mode()}")
         print(f"Minimum       : {self.find_minimum()}")
         print(f"Maximum       : {self.find_maximum()}")
         print(f"Unique Values : {self.count_unique_values()}")
         print(f"Range         : {self.calculate_range()}")
         print(f"Variance      : {self.calculate_variance():.2f}")
         print()
         print("================================")
    def main():
         numbers = [10, 20, 20, 30, 40, 50]

         try:
             analyzer = StatisticalAnalyzer(numbers)
             analyzer.validate_input()
             analyzer.display_result()

         except Exception as e:
             print("Error:", e)


         if __name__ == "__main__":
             main()