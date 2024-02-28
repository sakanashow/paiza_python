# 入力を受け取り、リストに分割
ans = input().split()
num = int(input())

# カウンターの初期化
counter = 0

# 各入力について処理を行う
for _ in range(num):
    # 入力をリストに分割
    i = input().split()
    # カウンターの初期化
    counter = 0
    # 入力の各要素について処理を行う
    for element in i:
        # element が ans に含まれている場合、カウンターを増やす
        if element in ans:
            counter += 1
    # カウンターの値を出力
    print(counter)