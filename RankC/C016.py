# n = input()
# line =[]
# for i in n:
#     if i == 'A':
#         line.append(4)
#     elif i == 'E':
#         line.append(3)
#     elif i == 'G':
#         line.append(6)
#     elif i == 'I':
#         line.append(1)
#     elif i == 'O':
#         line.append(0)
#     elif i == 'S':
#         line.append(5)
#     elif i == 'Z':
#         line.append(2)
#     else:
#         line.append(i)
# for i in line:
#     print(i, end="")


def convert_to_numbers(input_str):
    conversion_dict = {'A': '4', 'E': '3', 'G': '6', 'I': '1', 'O': '0', 'S': '5', 'Z': '2'} # 変換対象の辞書
    converted_str = ''
    for char in input_str:
        converted_str += conversion_dict.get(char, char) # 入力が変換対象の辞書に存在したら変換したものを追加、なければinputそのものを追加　辞書のgetは第一引数があればそれを、なければ第二引数（デフォルト値）を返す
    return converted_str

print(convert_to_numbers(input()))