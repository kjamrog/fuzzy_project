#!/usr/bin/env python

from src.computers.computers import ComputersList
import cgi
import json


def generateHeaders(headers):
  head = '<thead class="thead-inverse"><tr>'
  for header in headers:
    head += '<th>' + header + '</th>'
  head += '</tr></thead>'
  return head

def generateRows(computers):
  body = '<tbody>'
  for i in range(len(computers)):
    row = '<tr>'
    row += '<th scope="row">' + str(i+1) + '</th>'
    row += '<td>' + str(computers[i].name) + '</td>'
    row += '<td>' + '$' + str(computers[i].price) + '</td>'
    row += '<td>' + str(computers[i].calculated_rate) + '</td>'
    row += '</tr>'
    body += row
  body += '</tbody>'
  return body

def generateTable(headers, computers):
  return '<table class="table table-hover table-lg">' + generateHeaders(headers) + generateRows(computers) + '</table>'

def generateOutput(headers, computers):
  return '<html><body>'+generateTable(headers, computers)+'</body></html>'


computers = ComputersList()
form = cgi.FieldStorage()
price = float(form.getvalue('price'))

screen_size = form.getvalue('screen_size')
if screen_size.startswith('17'):
  screen_size = 17
elif screen_size.startswith('15'):
  screen_size = 15
else:
  screen_size = 14

best = computers.get_best(price, 10, screen_size)
headers = ['#', 'model', 'price', 'rate']

print("Content-type: text/html\n\n");
print(generateOutput(headers, best))
