import  random

offset = 50
x = random.randrange(700 - offset, 700 + offset)
if x == 700 - offset or x == 700 + offset:
    y = random.randrange(250 - offset, 250 + offset)
else:
    y = random.choice([250 - offset, 250 + offset])

print(x)
print(y)