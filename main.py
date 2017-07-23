from src.computers.computers import ComputersList


computers = ComputersList()
best = computers.get_best(0, 10)

for i in best:
    print(i.name + '    ' + str(i.cpu_rate))
