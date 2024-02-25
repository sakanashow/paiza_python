pareent_1, pareent_2 = map(int, input().split())
num = int(input())

for _ in range(num):
    child_1, child_2 = map(int, input().split())
    if pareent_1 == child_1:
        if pareent_2 >= child_2:
            print("Low")
        else:
            print("High")
    elif pareent_1 >= child_1:
        print("High")
    else:
        print("Low")