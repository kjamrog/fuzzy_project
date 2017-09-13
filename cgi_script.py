#!/usr/bin/env python

from src.computers.computers import ComputersList
import cgi
import json

computers = ComputersList()
form = cgi.FieldStorage()
price = form.getvalue('price')

best = computers.get_best(1200, 10)


print("Content-type: text/html\n\n");
print("""\
<html>
<body>
<h2>Hello World!</h2>
</body>
</html>
""")
