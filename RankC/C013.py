n = input()
num = int(input())
h = []
x = 0
for i in range(num):
    r = input()
    #print(r)
    if n in r:
        continue
    else:
        h.append(r)
        x += 1
    
if x == 0:
    h.append('none')
for ans in h:
    print(ans)