def greatest_factor_of_a_smaller_than_b(a, b):
    greatest_factor = 1
    for i in range(2, a + 1):
        factor = a / i
        if a % i == 0 and factor < b:
            greatest_factor = factor
    return greatest_factor

# Example usage:
a = 2
b = 0.6
greatest_c = greatest_factor_of_a_smaller_than_b(a, b)
print("The greatest c such that c < b and c is a factor of a is:", greatest_c)
