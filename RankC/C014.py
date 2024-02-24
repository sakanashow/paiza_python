# n, r = input().split()
# n = int(n)
# r = int(r)
# list = []

# for i in range(n): # 受け取ったボックス分ループ
#     box = input().split()
#     mi = min(int(m) for m in box) #配列の中身を数値にしないとミスる、受け取ったボックスの中の最小値を取得
    
#     #print(mi)
#     if int(mi) >= int(r*2): # ボックスの最小値（各ボックスの一辺）とボールのサイズを比較して収まっていればリストに追加する
#         list.append(i+1) # ボックスの番号をappend
# for i in list:
#     print(i)

n, r = map(int, input().split()) # この形にすると複数項目を一度に整数変換できる

boxes_with_room = []  # 収納可能なボックスのリスト

for box_num in range(1, n + 1):  # ボックスの数だけループ
    box = list(map(int, input().split()))  # ボックスの各辺の長さをリストとして受け取る
    if min(box) >= r * 2:  # ボックスの一辺の最小値とボールの直径を比較して収納可能かチェック
        boxes_with_room.append(box_num)  # 収納可能なボックスの番号を追加

for box_num in boxes_with_room:
    print(box_num)
