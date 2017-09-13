from src.computers.computers import ComputersList


computers = ComputersList()
best = computers.get_best(1000, 10)

for i in best:
    print(i.name + '    ' + str(i.calculated_rate))