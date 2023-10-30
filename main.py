import math

quarters = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [line.strip().split() for line in lines]
        return data


def generate_purchasing_plan_file(stock_data_input_file, plan_data_input_file, output_plan_file):
    stock_data = read_file(stock_data_input_file)
    plan_data = read_file(plan_data_input_file)

    stock = {}
    purchasing_plan = []

    for item in stock_data:
        detail, quantity = item
        if detail in stock:
            stock[detail] += int(quantity)
        else:
            stock[detail] = int(quantity)

    for item in plan_data:
        date, detail, quantity = item
        stock_quantity = stock.get(detail, 0)
        deficit = int(quantity) - stock_quantity
        if deficit > 0:
            quarter = ((int(date.split('.')[1]) - 1) // 3) + 1
            year = int(date.split('.')[2])
            quarter_quantity = int(math.ceil(deficit * 1.2))
            purchasing_plan.append((
                4 if quarter - 1 == 0 else quarter - 1,
                year - 1 if quarter - 1 == 0 else year,
                detail,
                quarter_quantity
            ))

    with open(output_plan_file, 'w') as file:
        for item in purchasing_plan:
            quarter, year, detail, quarter_quantity = item
            file.write(f'{quarters[quarter]}.{year} {detail} {quarter_quantity}\n')


generate_purchasing_plan_file('skl.txt', 'plan.txt', 'purchase_plan.txt')
