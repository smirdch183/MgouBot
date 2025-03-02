import os
import requests

os.chdir(r'C:\Users\strai\source\repos\VSK\MGOPA')

dls = "https://docs.google.com/spreadsheets/d/1HNDgDzD2fOQPib_bPQbjc_AtscbMwLui/export?format=xlsx"
resp = requests.get(dls)
output = open('test.xlsx', 'wb')
output.write(resp.content)
output.close()