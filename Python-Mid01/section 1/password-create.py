# 2 make password list
import random
import string


upper = list(string.ascii_uppercase)
lower = list(string.ascii_lowercase)
all_letters = list(string.ascii_letters)
numbers = list(string.digits)
punc = list(string.punctuation)

all_characters = all_letters + numbers + punc

random.shuffle(all_characters)


length = int(input("please enter the length of password")) # 8
file = open("password_list.txt","a")
for step in range(100000):
    password = ""
    for i in range(length):
        password += random.choice(all_characters)

    file.write(password + "\n")