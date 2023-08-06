import random
import math

async def customencrypt(string:str):
    asciis = []
    biggest = 0
    for char in enumerate(string):
        charascii = ord(char[1])
        rand = math.floor(random.random() * (126-charascii))
        if (charascii + rand) > biggest:
            biggest = charascii + rand
        asciis.append({"Ascii":charascii, "Rand":rand, "Total":charascii + rand})
    randadd = math.floor(random.random() * (126-biggest))
    firststring = ""
    secondstring = ""
    for charascii in asciis:
        firststring += chr(charascii["Total"] + randadd)
        secondstring += chr(charascii["Rand"] + 65 + randadd)
    middle = chr(randadd + 65)
    finalstring = firststring + middle + secondstring
    return finalstring

async def customdecrypt(string:str):
    middle = string[(len(string)-1)//2:(len(string)+2)//2]
    randadd = ord(middle) - 65
    h = len(string)//2
    mod = (len(string) + 1) % 2
    string = string[:h - mod] + string[h + 1:]
    encoded, added = string[:len(string)//2], string[len(string)//2:]
    finalstring = ""
    iternum = 0
    for ascii in enumerate(added):
        add = ord(ascii[1]) - 65 - randadd
        finalstring += chr(ord(encoded[iternum]) - add - randadd)
        iternum += 1
    return finalstring

async def customencrypttimes(string:str, times:int):
    iternum = 0
    while iternum < times:
        string = await customencrypt(string)
        iternum += 1
    return string

async def customdecrypttimes(string:str, times:int):
    iternum = 0
    while iternum < times:
        string = await customdecrypt(string)
        iternum += 1
    return string