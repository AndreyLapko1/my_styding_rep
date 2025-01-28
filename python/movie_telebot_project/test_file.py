
def summ(numb: list) -> int:
    total = sum(int(num) for num in numb)
    return total
print(summ(list(map(int, input('Enter 3 digits separated by a space: ').split()))))



