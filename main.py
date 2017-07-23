from src.computers.computers import ComputersList
import cgi


computers = ComputersList()
best = computers.get_best(0, 10)

form = cgi.FieldStorage()
print(form.getValue('price'))


for i in best:
    print(i.name + '    ' + str(i.cpu_rate))
