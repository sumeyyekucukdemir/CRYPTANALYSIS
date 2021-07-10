#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="sumeyyekucukdemir"
__date__ ="$July 8, 2021 10:03:00 AM$"


import numpy as np
import random

S_box={0:0xE, 1:0x4, 2:0xD, 3:0x1, 4:0x2, 5:0xF, 6:0xB, 7:0x8, 8:0x3, 9:0xA, 0xA:0x6, 0xB:0xC, 0xC:0x5,
      0xD:0x9, 0xE:0x0, 0xF:0x7}
S_box_inverse = {value : key for (key, value) in S_box.items()}
P_box={1:1, 2:5, 3:9, 4:13, 5:2, 6:6, 7:10, 8:14, 9:3, 10:7, 11:11, 12:15, 13:4, 14:8, 15:12, 16:16}
P_box_inverse = {value : key for (key, value) in P_box.items()}

def s_box(x):
    s_box_inputs=[]
    for i in range(4):
        s_box_inputs.append((x>>4*(3-i)) & 15)
    s_box_output=0
    for s_box_input in s_box_inputs:
        s_box_output= s_box_output<<4
        s_box_output= s_box_output ^ S_box[s_box_input]
    return  s_box_output
def inverse_s_box(x):
    inv_s_box_inputs=[]
    for i in range(4):
        inv_s_box_inputs.append((x>>4*(3-i)) & 15)
    inv_s_box_output=0
    for inv_s_box_input in inv_s_box_inputs:
        inv_s_box_output= inv_s_box_output<<4
        inv_s_box_output= inv_s_box_output ^ S_box_inverse[inv_s_box_input]
    return  inv_s_box_output

def p_box(x):
    p_box_inputs=[]
    p_box_outputs=[]
    for i in range(16):
        p_box_inputs.append((x>>(15-i)) & 1)
    for j in range(16):
        p_box_outputs.append(p_box_inputs[(P_box[j+1])-1])
    p_box_output=0
    for p_box_out in p_box_outputs:
        p_box_output=p_box_output<<1
        p_box_output=p_box_output ^ p_box_out
    return  p_box_output

#generate random plaintexts
#format(random.getrandbits(16),'#018b')
plaintexts=[]
def init_plaintexts():
    for i in range(10):
        plaintexts.append(random.getrandbits(16))

#generate random key
sub_keys=[]
master_key=0
def init_master_key():
    master_key=random.getrandbits(32)
    for i in range (5):
        sub_key=(master_key>>4*(4-i)) & 65535
        sub_keys.append(sub_key)
    for sub_key in sub_keys:
        print(format(sub_key,'#018b'))

#divide plaintext in to sub-blocks
all_sub_blocks=[]
def divide_plaintext_into_subblocks():
    for plaintext in plaintexts:
        sub_blocks=[]
        for i in range(4):
            sub_block=(plaintext>>4*(3-i)) & 15
            sub_blocks.append(sub_block)
        all_sub_blocks.append(sub_blocks)

#encryption 
def encryption(plaintext,key):
    keys=[]
    for i in range (5):
        sub_key=(master_key>>4*(4-i)) & 65535
        keys.append(sub_key)
    for i in range(3):
        s_box_input=plaintext ^ keys[i]
        s_box_output=s_box(s_box_input)
        p_box_output=p_box(s_box_output)
        plaintext=p_box_output
    s_box_input=plaintext ^ keys[3]
    s_box_output=s_box(s_box_input)
    ciphertext=s_box_output ^ keys[4]
    return ciphertext

key_list=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
x_new_list=[]
x_xor_dictionary = {}
def init_x_xor_dict():
    for k in range(16):
        k_list=[]
        for i in range(16):
            for j in range(16):
                if(i ^ j==k):
                    k_list.append((i,j))
        x_new_list.append(k_list)
    x_xor_dictionary = dict(zip(key_list, x_new_list))

def s_box_operation(x):
    result=S_box[x[0]] ^ S_box[x[1]]
    return result

#Differential distrubiton table of S_box
def print_ddt():
    init_x_xor_dict()
    table=np.zeros(256).reshape(16,16)
    for key in x_xor_dictionary:
        for pair in x_xor_dictionary[key]:
            table[key][s_box_operation(pair)]+=1       
print(table)

if __name__ == "__main__":
    init_plaintexts()
    init_masterkey()
    divide_plaintext_into_subblocks()
    key_pairs_counter=np.zeros(256)
    for plaintext_1 in plaintexts:
        ciphertext_1=encryption(plaintext_1,master_key)
        for plaintext_2 in plaintexts:
            ciphertext_2=encryption(plaintext_2,master_key)
            delta_plain=plaintext_1 ^ plaintext_2
            delta_cipher= ciphertext_1 ^ ciphertext_2
            if(delta_plain==2816 and (delta_cipher>>4)&15==0 and (delta_cipher>>12)&15==0):
                for key in range(256):
                    L_1=(key>>4) & 15
                    L_2=key & 15
                    v_42=L_1 ^ ((ciphertext_1>>8)&15)
                    v_44=L_2 ^ (ciphertext_1 &15)
                    u_42=S_box_inverse[v_42]
                    u_44=S_box_inverse[v_44]
                    _v_42=L_1 ^ ((ciphertext_2>>8)&15)
                    _v_44=L_2 ^ (ciphertext_2 &15)
                    _u_42=S_box_inverse[_v_42]
                    _u_44=S_box_inverse[_v_44]
                    U_42=u_42 ^ _u_42
                    U_44=u_44 ^ _u_44
                    if(U_42==6 and U_44==6):
                        key_pairs_counter[key]+=1
    max_count=-1
    max_key=-1
    for key in range(256):
        if(key_pairs_counter[key]>max_count):
            max_count=key_pairs_counter[key]
            max_key=key
    K_52=(max_key>>4) & 15
    K_54=max_key & 15
    print("second block subkey of last round can be %s,fourth block subkey of last roundcan be %s"%(format(K_52,'#010b'),format(K_54,'#010b')))