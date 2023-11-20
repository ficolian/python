filename = "example new.txt"
input_file = open(filename, 'r')


content = input_file.read()

items = content.split()


dict = {}
for item in items:
    if item not in dict:
        dict[item] = 1
    else:
        dict[item] += 1


for k in sorted(dict):
    print(k, dict[k])