def unary_sum_manual(input_str):
    count = 0
    sum_ones = 0
    for char in input_str:
        if char == '1':
            count += 1
        elif char == '+':
            sum_ones += count
            count = 0
    sum_ones += count  # Add the remaining '1's after '+'
    return '1' * sum_ones


input_str = "111+11"
result = unary_sum_manual(input_str)
print(result)  # Output: "11111"