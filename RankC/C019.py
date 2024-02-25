n = int(input())
num_list = []
for _ in range(n):
    num_list.append(int(input()))
num_list_number = len(num_list)

counter = 0
for j in range(num_list_number):
    for n in range(1, int(num_list[j])+1):
        if num_list[j] % n == 0:
            counter += n 
          
    counter -= int(num_list[j])    
     
    if counter == num_list[j]:
        print('perfect')
    elif counter == int(num_list[j]-1):
        print('nearly')
    else:
        print('neither')
    counter = 0
#print(counter)
    

# リファクタリング
def is_perfect_or_nearly(num):
    sum_divisors = sum(i for i in range(1, num) if num % i == 0) # リスト内法表記で約数の合計を計算
    if sum_divisors == num:
        return 'perfect'
    elif sum_divisors == num - 1:
        return 'nearly'
    else:
        return 'neither'

n = int(input())
for _ in range(n):
    num = int(input())
    print(is_perfect_or_nearly(num))