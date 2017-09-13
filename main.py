#!/usr/bin/python

import sys
from src.computers.computers import ComputersList

if len(sys.argv) < 2:
    print('Error: Invalid number of command line parameters.\nRequired: 1, Found: ', len(sys.argv)-1)
    sys.exit()

try:
    price = float(sys.argv[1])
except:
    print('Invalid command line parameter. Must be number')
    sys.exit()


computers = ComputersList()
best = computers.get_best(price, 10, 15)

for i in best:
    print("{}   {}  {}".format(i.name, i.price, i.calculated_rate))