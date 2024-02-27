# 入力を受け取る
numbers = input().split()

# 数字を降順にソートする
numbers.sort(reverse=True)

# 2つの整数を結合する
x = int(numbers[0] + numbers[2])
y = int(numbers[1] + numbers[3])

# 和を計算して出力する
print(x + y)