n, r = input().split()
n = int(n)
r = int(r)
list = []

for i in range(n): # 受け取ったボックス分ループ
    box = input().split()
    mi = min(int(m) for m in box) #配列の中身を数値にしないとミスる、受け取ったボックスの中の最小値を取得
    
    #print(mi)
    if int(mi) >= int(r*2): # ボックスの最小値（各ボックスの一辺）とボールのサイズを比較して収まっていればリストに追加する
        list.append(i+1) # ボックスの番号をappend
for i in list:
    print(i)