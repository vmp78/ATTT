import os
import time


def file_to_bits(file_path):
    with open(file_path, "rb") as file:
        data = bytearray(file.read())
        bits = ''.join(format(byte, '08b') for byte in data)
        return bits


def genKey(key, IV, size):
    binary_key = bin(key)[2:].zfill(80)
    binary_IV = bin(IV)[2:].zfill(80)

    shiftA = [0 for i in range(93)]
    shiftB = [0 for i in range(84)]
    shiftC = [0 for i in range(111)]

    shiftA[:80] = list(map(int, binary_key))
    shiftB[:80] = list(map(int, binary_IV))
    shiftC[110] = shiftC[109] = shiftC[108] = 1

    # initializ shift
    for i in range(1152):
        t1 = shiftA[65] ^ shiftA[92]
        t2 = shiftB[68] ^ shiftB[83]
        t3 = shiftC[108] ^ shiftC[109]

        t1 = t1 ^ (shiftA[90] ^ shiftA[91]) ^ shiftB[77]
        t2 = t2 ^ (shiftB[81] ^ shiftB[82]) ^ shiftC[86]
        t3 = t3 ^ (shiftC[108] ^ shiftC[109]) ^ shiftA[68]

        shiftA.insert(0, t3)
        shiftB.insert(0, t1)
        shiftC.insert(0, t2)
        shiftA.pop()
        shiftB.pop()
        shiftC.pop()

    key_list = []
    for i in range(size):
        t1 = shiftA[65] ^ shiftA[92]
        t2 = shiftB[68] ^ shiftB[83]
        t3 = shiftC[108] ^ shiftC[109]

        t1 = t1 ^ (shiftA[90] ^ shiftA[91]) ^ shiftB[77]
        t2 = t2 ^ (shiftB[81] ^ shiftB[82]) ^ shiftC[86]
        t3 = t3 ^ (shiftC[108] ^ shiftC[109]) ^ shiftA[68]

        key_list.append(t1 ^ t2 ^ t3)

        shiftA.insert(0, t3)
        shiftB.insert(0, t1)
        shiftC.insert(0, t2)
        shiftA.pop()
        shiftB.pop()
        shiftC.pop()

    binary_string = ''.join(map(str, key_list))
    return binary_string

def encryption(filePath, key, IV):
    binText = file_to_bits(filePath)
    sizeOfText = len(binText)

    keySteam = genKey(key, IV, sizeOfText)

    for i in range(sizeOfText):
        ciphertext = int(keySteam[i], 2) ^ int(keySteam[i], 2)

key = 0x1a2a3a4a5a6a7a8aa9ab
IV = 0xaaaaeafa2adca4aaaa2a
folder_path = "testdata"
files = os.listdir(folder_path)

for file_name in files:
    #     # if os.path.isfile(os.path.join(folder_path, file_name)):
    file_path = os.path.join(folder_path, file_name)
    start_time = time.time()
    encryption(file_path, key, IV)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time of encrypt file {file_name}: {execution_time} s")