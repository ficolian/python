
import json
def find(name):
  data = {}  
  data['phone'] = []
  print(name)
  try:
    f = open("phonebook.txt", "r")
    data= json.load(f)
    f.close()
    result = [x for x in data['phone'] if x["name"]== name]
    print(result)
    return result
  except:
    return "no data on phone book"

x=False
if(x):
  insertData()
else:
  find('fifi')
