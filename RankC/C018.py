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

keys = []
for n in menus:
    if n not in have: # そもそも持っている素材に必要素材が存在しないならその時点で0を出して終了
        ans = 0
        break
    else: # それ以外の時、いくつ作れるか計算する
        key = have[n] // menus[n] # それぞれの素材同士で割り算する
        keys.append(key)
        ans = min(keys) # ０がなければ全素材数のうち最小を出力
print(ans)

# リファクタリング
recipe_count = int(input())
menus = {}
have = {}
ans = float('inf')  # 無限大で初期化 無限大で初期化しておくと最小値がとりやすくなる

# レシピの入力
for _ in range(recipe_count):
    name, number = input().split()
    menus[name] = int(number)

# 手元の材料の入力
my_ingredients_count = int(input())
for _ in range(my_ingredients_count):
    name, number = input().split()
    have[name] = int(number)

# レシピごとに計算
for name, number in menus.items():
    if name not in have:
        ans = 0  # 手元に足りない材料がある場合、作れる料理の数は0
        break
    else:
        # 作れる料理の数を計算し、最小値を更新
        possible_dishes = have[name] // number
        ans = min(ans, possible_dishes)

print(ans)