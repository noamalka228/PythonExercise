class CacheDecorator(dict):
    # constructor
    def __init__(self, func_name):
        self.func_name = func_name

    # if the function is already cached, return the cached value
    def __call__(self, *args):
        return self[args]

    # if the result is not cached, return the function call and cache the result for future calls
    def __missing__(self, key):
        result = self[key] = self.func_name(*key)
        return result

# calling the class of the CacheDecorator
@CacheDecorator
# this function gets a number as parameter and recursively sums all numbers from 1 to num
def sum_all(num):
    if type(num) is int:
        if num == 0 or num == 1:
            return 1
        return num + sum_all(num - 1)

def main():
    print("Sum: ", sum_all(5)) # the call caches all sums from 1-5
    print("Cached sums: ", sum_all)  # therefore, calling the func without parameter prints sum(5)
    print("Sum: ", sum_all(10)) # the call caches all sums from 5-10
    print("Cached sums: ", sum_all) # therefore, calling the func without parameter prints sum(10)


if __name__ == "__main__":
    main()
