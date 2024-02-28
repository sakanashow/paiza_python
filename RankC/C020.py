def calculate_seisen(kg, row, seisen):
    weight_after_row = kg * ((100 - row) * 0.01)
    seisen_weight = weight_after_row * ((100 - seisen) * 0.01)
    return seisen_weight

kg, row, seisen = map(int, input().split())
result = calculate_seisen(kg, row, seisen)
print(result)