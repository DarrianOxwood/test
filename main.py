def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [line.strip().split() for line in lines]
        return data


stock_data = read_file('skl.txt')

stock = {}

for item in stock_data:
    detail, quantity = item
    if detail in stock:
        stock[detail] += int(quantity)
    else:
        stock[detail] = int(quantity)


expenditure_plan_data = read_file('plan.txt')

expenditure_plan = []

for item in expenditure_plan_data:
    date, detail, quantity = item
    expenditure_plan.append(item)

print(expenditure_plan)
