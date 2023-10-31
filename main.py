import math
import re

quarters = {1: 'I', 2: 'II', 3: 'III', 4: 'IV'}


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        data = [line.strip().split() for line in lines]
        return data


def plan_summ_for_quarter_year(purchase_list):
    # приводит список вида ['дд.мм.гггг', 'номер_детали', 'количество']
    # к списку вида ['квартал.год', 'деталь', количество]
    # и суммирует количество всех деталей
    # по кварталу году и номреу детали

    purchasing_plan_dictionary = {}

    for item in purchase_list:
        date, detail, quantity = item

        quarter = ((int(date.split('.')[1]) - 1) // 3) + 1
        year = int(date.split('.')[2])

        purchase_id = f'{quarter}.{year} {detail}'

        if purchase_id in purchasing_plan_dictionary:
            purchasing_plan_dictionary[purchase_id] += int(quantity)
        else:
            purchasing_plan_dictionary[purchase_id] = int(quantity)

    purchasing_plan = []

    for item in purchasing_plan_dictionary:
        quarter, year, detail = re.split("[. ]+", item)
        purchasing_plan.append([quarter, year, detail, purchasing_plan_dictionary[item]])

    return purchasing_plan


def stock_summ(stock_items):
    # суммирует количество деталь на складе
    # и создает словарь вида {'номер_детали': количество}

    stock = {}
    for item in stock_items:
        detail, quantity = item
        if detail in stock:
            stock[detail] += int(quantity)
        else:
            stock[detail] = int(quantity)

    return stock


def generate_purchasing_plan_file(stock_data_input_file, plan_data_input_file, output_file):
    stock_data = read_file(stock_data_input_file)
    plan_data = read_file(plan_data_input_file)

    stock = stock_summ(stock_data)
    usage_plan = plan_summ_for_quarter_year(plan_data)

    purchasing_plan = []

    for item in usage_plan:
        quarter, year, detail, quantity = item
        stock_quantity = stock.get(detail, 0)
        deficit = quantity - stock_quantity
        if deficit > 0:
            quarter_quantity = int(math.ceil(deficit * 1.2))
            stock[detail] = stock[detail] + quarter_quantity - quantity
            purchasing_plan.append([
                4 if int(quarter) - 1 == 0 else int(quarter) - 1,
                int(year) - 1 if int(quarter) - 1 == 0 else int(year),
                detail,
                quarter_quantity])

        print(purchasing_plan)

        with open(output_file, 'w') as file:
            for purchasing_plan_item in purchasing_plan:
                quarter, year, detail, quarter_quantity = purchasing_plan_item
                file.write(f'{quarters[quarter]}.{year} {detail} {quarter_quantity}\n')


stock_from_file = 'skl.txt'
plan_from_file = 'plan.txt'
plan_file = 'purchase_plan.txt'
generate_purchasing_plan_file(stock_from_file, plan_from_file, plan_file)





'''generate_purchasing_plan_file('skl.txt', 'plan.txt', 'purchase_plan.txt')
print("Файл плана закупок успешно обновлен.")
'''
