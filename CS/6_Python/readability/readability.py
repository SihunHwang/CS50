from cs50 import get_string

sentences = 0
words = 1
letters = 0

text = get_string('Text: ')

for c in text:
    if c in ['.', '?', '!']:
        sentences += 1
    elif c == ' ':
        words +=1
    elif c.isalpha():
        letters += 1;

L = 100 * (letters / words)
S = 100 * (sentences / words)


index = round(0.0588 * L - 0.296 * S - 15.8)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f'Grade {index}')