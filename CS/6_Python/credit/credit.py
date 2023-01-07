from sys import exit

card_num = input('Number: ')

checksum = 0

for d, i in enumerate(card_num[::-1]):
    i = int(i)

    if d % 2 == 1:
        i = str(i*2)
        for x in i:
            checksum += int(x)

    else:
        checksum += i

if checksum % 10 != 0:
    print('INVALID')
    exit()

if len(card_num) == 15 and (card_num[0:2] in ['34', '37']):
    print("AMEX")
elif len(card_num) == 16 and (int(card_num[0:2]) in range(51,56)):
    print('MASTERCARD')
elif (len(card_num) in range(13, 17)) and card_num[0] == '4':
    print("VISA")