# write fibonacci Code

def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

print(fibonacci(10))