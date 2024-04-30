def calculate_budget(waves):
    budget = 0
    for wave in range(1, waves + 1):
        budget += 5
        budget += round(budget / 5)
    return budget

waves = int(input("Введите количество волн: "))
result = calculate_budget(waves)
print(f"Бюджет на {waves} волне: {result}")

waves = int(input("Введите количество бюджета: "))
budget = 0
for wave in range(1, waves + 1):
    budget += 5
    budget += round(budget / 5)
    if budget >= waves:
        break
print(f"Бюджет на {budget} волне: {wave}")
