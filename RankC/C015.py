n = int(input())

total_points = 0
for _ in range(n): # ループ変数が実際に使用されない場合は_を使用する
    day, amount = input().split()
    amount = int(amount)
    if '3' in day:
        total_points += amount * 0.03
    elif '5' in day:
        total_points += amount * 0.05
    else:
        total_points += amount * 0.01
    
print(int(total_points))