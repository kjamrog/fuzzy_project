#!/usr/bin/env python

#this script must be stored in cgi-bin/fuzzy_project

from src.computers.computers import ComputersList
import cgi
import json

computers = ComputersList()
best = computers.get_best(0, 10)

form = cgi.FieldStorage()
price = form.getValue('price')

print(json.dumps({'price': price}))
# for i in best:
#     print(i.name + '    ' + str(i.cpu_rate))
