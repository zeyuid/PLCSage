from math import log
import numpy as np
import struct




def entropy_user(data):
    H = 0
    # build the probability of the distribution for 1-dimension stochastic
    pdf = {}

    if data.size != 0:
        # data.sort() # sort list
        # sortData = np.array(data)
        sortData = data[np.argsort(data[:, 0])]

        [m, n] = sortData.shape
        last = sortData[0, :]
        p = 1
        for k in range(1, m):
            e = sortData[k, :]

            if sum(e == last) == n:
                p = p + 1
            else:
                if n == 1:
                    # build the pdf, only if the dimension equals to 1
                    pdf[str(last)] = p/m

                last = e
                H = H - p/m * log(p/m, 2)
                p = 1
        H = H - p / m * log(p/m, 2)
    else:
        sortData = data

    return H  # pdf, sortData

# H, sortData = entropy_user([[1,0], [1,0]])
# print(H)

def hex2float_big(hex_num):
    # hex_num = '41973333'
    if len(hex_num) == 8:
        float_num = struct.unpack('!f', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    elif len(hex_num) == 16:
        float_num = struct.unpack('!d', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    else:
        float_num = 0
        print("Error bytes number")
    return float_num

def hex2int_big(hex_num):
    # hex_num = '41973333'
    if len(hex_num) == 4:
        int_num = struct.unpack('!h', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    elif len(hex_num) == 8:
        int_num = struct.unpack('!i', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    else:
        int_num = 0
        print("Error bytes number")
    return int_num

def hex2float_little(hex_num):
    # hex_num = '41973333'
    if len(hex_num) == 8:
        float_num = struct.unpack('f', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    elif len(hex_num) == 16:
        float_num = struct.unpack('d', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    else:
        float_num = 0
        print("Error bytes number")
    return float_num

def hex2int_little(hex_num):
    # hex_num = '41973333'
    if len(hex_num) == 4:
        int_num = struct.unpack('h', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    elif len(hex_num) == 8:
        int_num = struct.unpack('i', bytes.fromhex(hex_num))[0]  # '!' means the network flow (big-endian)
    else:
        int_num = 0
        print("Error bytes number")
    return int_num


def hex_filtering_user(hexsamples):
    
    total_sum = 0
    for i in range(len(hexsamples)):
        total_sum = total_sum + int(hexsamples[i], 16)

    averaged_hex = hex(int(total_sum/len(hexsamples)))[2:]
    averaged_hex = format(averaged_hex, '0>{}'.format(2))  # append the higher bits

    return averaged_hex



def non_zeros_ratio(data):
    H = sum(abs(data))/data.shape[0]
    return H  # pdf, sortData
