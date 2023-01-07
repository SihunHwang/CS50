while True:
    h = input('Height: ')
    
    try:
        h = int(h)
    except:
        continue

    if h > 0 and h <= 8:
        break

for i in range(1, h + 1):
    print(' '*(h-i) + '#'*i + '  ' + '#'*i)