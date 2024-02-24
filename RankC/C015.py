n = int(input())

point = 0
for i in range(n):
    day, amount = input().split()
    if '3' in day:
        point += int(int(amount)*0.03)
    elif '5' in day:
        point += int(int(amount)*0.05)
    else:    
        point += int(int(amount)*0.01)
    
print(point)