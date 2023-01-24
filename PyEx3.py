import names

def namelen(value):
    return(len(value) - 1)

for i in range(5):
    name = names.get_full_name()
    length = namelen(name)
    print(name + " - " + str(length))
