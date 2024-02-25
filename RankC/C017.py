pareent_1, pareent_2 = map(int, input().split())
num = int(input())

for _ in range(num):
    child_1, child_2 = map(int, input().split())
    if pareent_1 == child_1: # 一つ目の要素同士を比較して同じだった時は2つ目の要素同士を比較
        if pareent_2 >= child_2: # ２つ目の要素の場合は親のほうが大きい数字であればLowを出力
            print("Low")
        else:
            print("High")
    elif pareent_1 >= child_1: # １つ目の要素の比較で親が大きければHighを出力する
        print("High")
    else:
        print("Low")