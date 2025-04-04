def func(x):
    def func2(y):
        return x + y
    return func2
c = func(10)
print(c(5))
