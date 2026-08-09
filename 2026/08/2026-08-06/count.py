count = 0
now = 0
row = 1
serch_row = 38
max = 39 * 16


        
while True:
    print(row, " :",count)
    count += 16
    now += 16
    row +=1
    if now > max:
        break
    if count > 39:
        count = count % 39
