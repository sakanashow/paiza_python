n = input()
num = int(input())
h = []
for i in range(num):
    r = input()
    if n in r:
        continue
    else:
        h.append(r)
      
if not h: #リストが空のとき、Falseを、空でなければTrueを返す
    print('none')
else:
    for ans in h:
        print(ans)