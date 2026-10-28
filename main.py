import numpy as np

class DataAnalytics:
    """NumPy Analyzer - menu driven toolkit for common array operations."""

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------
    def __init__(self, arr=None):
        # private attribute (encapsulation)
        self.__arr = None if arr is None else np.array(arr)

    # ------------------------------------------------------------------
    # Class-level and static utility methods
    # ------------------------------------------------------------------
    @classmethod
    def from_list(cls, values):
        """Create an object directly from a Python list."""
        return cls(values)

    @staticmethod
    def read_int(prompt):
        return int(input(prompt))

    @staticmethod
    def read_numbers(prompt):
        """Read space separated numbers (int if possible, else float)."""
        parts = input(prompt).split()
        try:
            return [int(p) for p in parts]
        except ValueError:
            return [float(p) for p in parts]

    @staticmethod
    def __parse_range(text):
        """'1:3' -> slice(1, 3), ':' -> slice(None, None)"""
        start, end = text.split(":")
        return slice(int(start) if start.strip() else None,
                     int(end) if end.strip() else None)


    # ------------------------------------------------------------------
    # Private helper methods
    # ------------------------------------------------------------------
    def __read_second(self):
        size = self.__arr.size
        values = self.read_numbers(
            f"Enter the same-size array elements ({size} elements separated by space): ")
        if len(values) != size:
            raise ValueError(f"You must enter exactly {size} numbers.")
        return np.array(values).reshape(self.__arr.shape)


    def __show_two(self, other, title="Second Array"):
        print("\nOriginal Array:")
        print(self.__arr)
        print(f"\n{title}:")
        print(other)


    # ------------------------------------------------------------------
    # 1. Array creation, indexing, slicing
    # ------------------------------------------------------------------
    def create_array(self):
        print("\nSelect the type of array to create:")
        print("1. 1D Array")
        print("2. 2D Array")
        print("3. 3D Array")
        choice = self.read_int("Enter your choice: ")


        if choice == 1:
            shape = (self.read_int("Enter the number of elements: "),)
        elif choice == 2:
            rows = self.read_int("Enter the number of rows: ")
            cols = self.read_int("Enter the number of columns: ")
            shape = (rows, cols)
        elif choice == 3:
            layers = self.read_int("Enter the number of layers: ")
            rows = self.read_int("Enter the number of rows: ")
            cols = self.read_int("Enter the number of columns: ")
            shape = (layers, rows, cols)
        else:
            print("❌ Invalid choice. Please try again :)")
            return


        size = int(np.prod(shape))
        values = self.read_numbers(
            f"Enter {size} elements for the array separated by space: ")
        if len(values) != size:
            raise ValueError(f"You must enter exactly {size} numbers.")


        self.__arr = np.array(values).reshape(shape)
        print("\n✅ Array created successfully:")
        print(self.__arr)
        self.index_slice()


    def index_slice(self):
        while True:
            print("\nChoose an operation:")
            print("1. Indexing")
            print("2. Slicing")
            print("3. Go Back")
            choice = self.read_int("Enter your choice: ")


            if choice == 1:
                index = tuple(map(int, input(
                    "Enter index (space separated, e.g. 1 2): ").split()))
                print("Value:", self.__arr[index])
            elif choice == 2:
                if self.__arr.ndim == 1:
                    names = ["element"]
                elif self.__arr.ndim == 2:
                    names = ["row", "column"]
                else:
                    names = ["layer", "row", "column"]
                slices = tuple(
                    self.__parse_range(input(f"Enter the {n} range (start:end): "))
                    for n in names)
                print("\nSliced Array:")
                print(self.__arr[slices])
            elif choice == 3:
                break
            else:
                print("❌ Invalid choice. Please try again :)")


    # ------------------------------------------------------------------
    # 2. Mathematical operations
    # ------------------------------------------------------------------
    def maths_ops(self):
        print("\nChoose a mathematical operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Dot Product (1D arrays)")
        print("6. Matrix Multiplication (2D arrays)")
        choice = self.read_int("Enter your choice: ")


        if choice in (1, 2, 3, 4, 5):
            other = self.__read_second()
            self.__show_two(other)


            if choice == 1:
                print("\nResult of Addition:\n", self.__arr + other)
            elif choice == 2:
                print("\nResult of Subtraction:\n", self.__arr - other)
            elif choice == 3:
                print("\nResult of Multiplication:\n", self.__arr * other)
            elif choice == 4:
                if 0 in other:
                    print("❌ Cannot divide by zero!")
                else:
                    print("\nResult of Division:\n", self.__arr / other)
            else:
                if self.__arr.ndim != 1:
                    print("⚠️ Dot product works here only for 1D arrays.")
                else:
                    print("\nDot Product:", np.dot(self.__arr, other))
        elif choice == 6:
            if self.__arr.ndim != 2:
                print("⚠️ Matrix multiplication needs a 2D array.")
                return
            rows = self.read_int(
                f"Second matrix rows (must be {self.__arr.shape[1]}): ")
            cols = self.read_int("Second matrix columns: ")
            if rows != self.__arr.shape[1]:
                print("❌ Rows of 2nd matrix must equal columns of 1st matrix.")
                return
            values = self.read_numbers(f"Enter {rows * cols} elements: ")
            if len(values) != rows * cols:
                raise ValueError(f"You must enter exactly {rows * cols} numbers.")
            other = np.array(values).reshape(rows, cols)
            self.__show_two(other, "Second Matrix")
            print("\nMatrix Multiplication Result:\n", np.matmul(self.__arr, other))
        else:
            print("❌ Invalid choice. Please try again :)")


    # ------------------------------------------------------------------
    # 3. Combine / Split
    # ------------------------------------------------------------------
    def combine_split(self):
        print("\nChoose an option:")
        print("1. Combine Arrays")
        print("2. Split Array")
        choice = self.read_int("Enter your choice: ")


        if choice == 1:
            other = self.__read_second()
            self.__show_two(other)
            print("\nCombined Array (Vertical Stack):")
            print(np.vstack((self.__arr, other)))
        elif choice == 2:
            n = self.read_int("Number of parts: ")
            print("\nSplit Result:")
            for part in np.array_split(self.__arr, n):
                print(part)
        else:
            print("❌ Invalid choice. Please try again :)")


    # ------------------------------------------------------------------
    # 4. Search / Sort / Filter
    # ------------------------------------------------------------------
    def search_sort_filter(self):
        print("\nChoose an option:")
        print("1. Search a value")
        print("2. Sort the array")
        print("3. Filter values")
        choice = self.read_int("Enter your choice: ")


        if choice == 1:
            x = float(input("Value to search: "))
            positions = np.argwhere(self.__arr == x)
            if len(positions) > 0:
                print("✅ Found at index:")
                print(positions)
            else:
                print("❌ Value not found.")
        elif choice == 2:
            print("1. Ascending\n2. Descending")
            order = self.read_int("Enter your choice: ")
            print("\nOriginal Array:")
            print(self.__arr)
            result = np.sort(self.__arr, axis=-1)
            if order == 2:
                result = result[..., ::-1]
            print("\nSorted Array:")
            print(result)
            if self.__arr.ndim > 1:
                print("(Sorting applied row-wise.)")
        elif choice == 3:
            x = float(input("Threshold value: "))
            print("1. Less than\n2. Greater than\n3. Equal to")
            option = self.read_int("Enter filter option: ")
            if option == 1:
                print("Filtered Array:", self.__arr[self.__arr < x])
            elif option == 2:
                print("Filtered Array:", self.__arr[self.__arr > x])
            elif option == 3:
                print("Filtered Array:", self.__arr[self.__arr == x])
            else:
                print("⚠️ Invalid filter option!")
        else:
            print("❌ Invalid choice!")


    # ------------------------------------------------------------------
    # 5. Aggregates and Statistics
    # ------------------------------------------------------------------
    def aggregates_stats(self):
        print("\nChoose an aggregate/statistical operation:")
        print("1. Sum")
        print("2. Mean")
        print("3. Median")
        print("4. Standard Deviation")
        print("5. Variance")
        print("6. Minimum")
        print("7. Maximum")
        print("8. Percentile")
        print("9. Correlation Coefficient")
        choice = self.read_int("Enter your choice: ")


        print("\nOriginal Array:")
        print(self.__arr)
        print()


        if choice == 1:
            print("Sum of Array:", np.sum(self.__arr))
        elif choice == 2:
            print("Mean of Array:", np.mean(self.__arr))
        elif choice == 3:
            print("Median of Array:", np.median(self.__arr))
        elif choice == 4:
            print("Standard Deviation of Array:", np.std(self.__arr))
        elif choice == 5:
            print("Variance of Array:", np.var(self.__arr))
        elif choice == 6:
            print("Minimum value:", np.min(self.__arr))
        elif choice == 7:
            print("Maximum value:", np.max(self.__arr))
        elif choice == 8:
            q = float(input("Enter percentile (0-100): "))
            print(f"{q}th Percentile:", np.percentile(self.__arr, q))
        elif choice == 9:
            other = self.__read_second()
            corr = np.corrcoef(self.__arr.flatten(), other.flatten())[0, 1]
            print("Correlation Coefficient:", corr)
        else:
            print("❌ Invalid choice!")


    # ------------------------------------------------------------------
    # Main menu
    # ------------------------------------------------------------------
    def run(self):
        print("Welcome to the NumPy Analyzer!")
        print("=" * 40)
        while True:
            print("\nChoose an option:")
            print("1. Create a Numpy Array")
            print("2. Perform Mathematical Operations")
            print("3. Combine or Split Arrays")
            print("4. Search, Sort, or Filter Arrays")
            print("5. Compute Aggregates and Statistics")
            print("6. Exit")
            try:
                choice = int(input("Enter your choice: "))


                if choice == 6:
                    print("\nThank you for using the NumPy Analyzer! Goodbye!")
                    break
                elif choice == 1:
                    self.create_array()
                elif self.__arr is None:
                    print("⚠️ Please create an array first (option 1).")
                elif choice == 2:
                    self.maths_ops()
                elif choice == 3:
                    self.combine_split()
                elif choice == 4:
                    self.search_sort_filter()
                elif choice == 5:
                    self.aggregates_stats()
                else:
                    print("⚠️ Invalid choice!")
            except ValueError as e:
                print("⚠️ Invalid input:", e)
            except Exception as e:
                print("Error:", e)




if __name__ == "__main__":
    DataAnalytics().run()





