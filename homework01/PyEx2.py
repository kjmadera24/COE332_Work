import names

names8 = []

while (len(names8)) < 5:
    name = names.get_first_name()
    if len(name) == 8:
        names8.append(name)

print(names8)
