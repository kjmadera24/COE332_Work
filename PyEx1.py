long5 = []
with open('words', 'r') as f:
    long5 = f.read().splitlines()

long5.sort(key=len, reverse = True)
for x in range(5):
    print(long5[x])
