recipe = int(input())
menus = {}
have = {}
ans = 0

for a in range(recipe):
    name, number = (input().split())
    menus[name] = int(number)

my = int(input())

for a in range(my):
    name, number = (input().split())
    have[name] = int(number)
# print(have)
for n in menus:
    # print(n)
    # print(have[n])
    # print(menus[n])
    if(menus[n] // have[n] == 0):
        print(menus[n])        


# それぞれの素材同士で割り算して一つでも０があればその時点で０を出力
# ０がなければ全素材数のうち最小を出力