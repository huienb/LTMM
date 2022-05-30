#chuyển sang bit 
def Hex_to_List_Bin(a, size):
	a = list(str(bin(a)))	
	a.pop(0)	
	a.pop(0)
	if(len(a) < size):	
		for i in range(size - len(a)):	
			a.insert(0,'0')
	return a

plaintext = 0xff7fbffffefdffef
key_input = 0xfedcba3005200130

bin_text = Hex_to_List_Bin(plaintext,64)

# Hoán vị khởi tạo
def Initial_permutation_Table(s1):
	table = [ 58, 50, 42, 34, 26, 18, 10, 2,#8
			  60, 52, 44, 36, 28, 20, 12, 4,#16
			  62, 54, 46, 38, 30, 22, 14, 6,#24
			  64, 56, 48, 40, 32, 24, 16, 8,#32
			  57, 49, 41, 33, 25, 17,  9, 1,#40
			  59, 51, 43, 35, 27, 19, 11, 3,#48
			  61, 53, 45, 37, 29, 21, 13, 5,#56
			  63, 55, 47, 39, 31, 23, 15, 7 #64
			  ]
	s = [ s1[table[i]-1] for i in range(64) ]
	return s

a = Initial_permutation_Table(bin_text)

# Bỏ parity bits và hoán đổi ví trị theo bảng PC1
def Parity_drop_table(key):
	table = [ 57, 49, 41, 33, 25, 17, 9, 
			1,  58, 50, 42, 34, 26, 18,
			10,  2, 59, 51, 43, 35, 27,
			19, 11,  3, 60, 52, 44, 36,
			
			63, 55, 47, 39,	31, 23, 15,
			 7, 62, 54, 46, 38, 30, 22,
			14,  6, 61, 53, 45, 37, 29, 
			21, 13,  5, 28, 20, 12,  4 ]
	s = [ key[table[i]-1] for i in range(56) ]
	return s

def Key_compression_table(key_left, key_right):
	k = key_left + key_right
	table = [ 14, 17, 11, 24,  1,  5,  3, 28,
			  15,  6, 21, 10, 23, 19, 12,  4,
			  26,  8, 16,  7, 27, 20, 13,  2,
			  41, 52, 31, 37, 47, 55, 30, 40,
			  51, 45, 33, 48, 44, 49, 39, 56,
			  34, 53, 46, 42, 50, 36, 29, 32 ]
	key_compress = [ k[table[i]-1] for i in range(48) ]
	return key_compress

def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1,len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = ""
    return k 

def Key_gereration(key):
	key = Hex_to_List_Bin(key, 64)
	key = Parity_drop_table(key) 


	key_left = key[0:28]   
	key_right = key[28:56] 
 
	shift = []
	for i in range(16):
		if i == 0 or i == 1 or i == 8 or i == 15:
			shift.append(1)
		else:
			shift.append(2)

	Round_key = []
	
	for count in range(16):
		key_left = shift_left(key_left,shift[count]) 
		key_right= shift_left(key_right,shift[count]) 
		Round_key.append(Key_compression_table(key_left, key_right))	
	return Round_key


key = Key_gereration(key_input)


round = []
round.append(a)

left = round[0][0:32]
right = round[0][32:]

def Expansion_Pbox(plaintext_right):
	expansion = [0 for i in range(48)]			
	count_top = 0
	for i in range(48):
	
		if i%6 ==0:
			expansion[i] = plaintext_right[count_top-1]
		elif i%6 == 1:
			expansion[i] = plaintext_right[count_top]
		elif i%6 == 2:
			expansion[i] = plaintext_right[count_top+1]
		elif i%6 == 3:
			expansion[i] = plaintext_right[count_top+2]
		elif i%6 == 4:
			expansion[i] = plaintext_right[count_top+3]
		elif i%6 == 5:
			if i < 46:
				expansion[i] = plaintext_right[count_top+4]
				count_top += 4
			else:
				expansion[47] = plaintext_right[0]	
	return expansion

b = Expansion_Pbox(right)

def XOR(expansion, key, size):
	xor = []
	for i in range(size):
		if expansion[i] == key[i]:
			xor.extend('0')
		else:
			xor.extend('1')	
	return xor

c = XOR(b,key[0],48)

def S_Boxes_table(input, index):
	Convert_str_to_dec = {  '00' :  0,   '01' :  1,   '10' :  2,   '11' :  3, 
						  '0000' :  0, '0001' :  1, '0010' :  2, '0011' :  3, 
						  '0100' :  4, '0101' :  5, '0110' :  6, '0111' :  7, 
						  '1000' :  8, '1001' :  9, '1010' : 10, '1011' : 11, 
						  '1100' : 12, '1101' : 13, '1110' : 14, '1111' : 15 }
	s_box = [0]*8	# Tạo 8 bảng s-box
	s_box[0] = [[14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7],
				[ 0, 15,  7,  4, 14,  2, 13, 10,  3,  6, 12, 11,  9,  5,  3,  8],
				[ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0],
				[15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13]]

	s_box[1] = [[15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10],
				[ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5],
				[ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15],
				[13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9]]

	s_box[2] = [[10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8],
				[13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1],
				[13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7],
				[ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12]]

	s_box[3] = [[ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15],
				[13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9],
				[10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4],
				[ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14]]

	s_box[4] = [[ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9],
				[14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6],
				[ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14],
				[11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3]]

	s_box[5] = [[12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11],
				[10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8],
				[ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6],
				[ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7, 10,  0,  8, 13]]

	s_box[6] = [[ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1],
				[13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6],
				[ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2],
				[ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12]]

	s_box[7] = [[13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7],
				[ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11, 10, 14,  9,  2],
				[ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 10, 15,  3,  5,  8],
				[ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  9,  3,  5,  6, 11]]
	
	return s_box[index] [Convert_str_to_dec[input[0]+input[5]]] [Convert_str_to_dec[input[1]+input[2]+input[3]+input[4]]]	

def S_Boxes(s):
	s_box = [0,0,0,0,0,0,0,0]	
	count = 0
	for i in range(8):
		s_box[i] = s[count:count+6]	
		count += 6
	a = []		
	for i in range(8):	
		a.extend( Hex_to_List_Bin(S_Boxes_table(s_box[i], i), 4) ) 
	return a

d = S_Boxes(c)

def Straight_permutation_table(a):
	table = [ 16,  7, 20, 21, 29, 12, 28, 17,
			   1, 15, 23, 26,  5, 18, 31, 10,
			   2,  8, 24, 14, 32, 27,  3,  9,
			  19, 13, 30,  6, 22, 11,  4, 25 ]
	b = [ a[table[i]-1] for i in range(32) ]	
	return b

e= Straight_permutation_table(d)

f = XOR(e,left,32)
g = right + f
round.append(g)

for i in range(1,16):
    left = round[i][0:32]
    right = round[i][32:]
    b = Expansion_Pbox(right)
    c = XOR(b,key[i],48)
    d = S_Boxes(c)
    e = Straight_permutation_table(d)
    f = XOR(e,left,32)
    if (i!= 15):
        g = right + f
    else:
        g = f +right
    round.append(g)

def Final_permutation_Table(s1):
	table = [ 40,  8, 48, 16, 56, 24, 64, 32,
			  39,  7, 47, 15, 55, 23, 63, 31,
			  38,  6, 46, 14, 54, 22, 62, 30,
			  37,  5, 45, 13, 53, 21, 61, 29,
			  36,  4, 44, 12, 52, 20, 60, 28,
			  35,  3, 43, 11, 51, 19, 59, 27,
			  34,  2, 42, 10, 50, 18, 58, 26,
			  33,  1, 41,  9, 49, 17, 57, 25 ]
	s = [ s1[table[i]-1] for i in range(64) ]
	return s    

round.pop(0)
final = Final_permutation_Table(round[15])

def Hexa_out(plaintext, size):
	copy = plaintext.copy()
	copy = [ord(i)-ord('0') for i in copy] # Chuyển các kí tự '0', '1' sang dạng số
	Tong = 0
	for i in range(len(copy)): # Chuyển sang dạng thập phân
		Tong += (2**(size-i-1)) * copy[i]
	return hex(Tong)

Hexa_out(final,64)

def Encrypt(plaintext,key):
    A = Initial_permutation_Table(Hex_to_List_Bin(plaintext,64))
    round = []
    round.append(A)
    key_round = Key_gereration(key)
    for i in range(16):
        left_block = round[i][0:32]
        right_block = round[i][32:]
        B = Expansion_Pbox(right_block)
        C = XOR(B,key_round[i],48)
        D = S_Boxes(C)
        E = Straight_permutation_table(D)
        F = XOR(E, left_block,32)
        if i != 15:
            G = right_block + F
        else:
            G = F + right_block
        round.append(G)
    round.pop(0)
    return Final_permutation_Table(round[15])

def Decrypt(plaintext,key):
    A = Initial_permutation_Table(Hex_to_List_Bin(plaintext,64))
    round = []
    round.append(A)
    key_round = Key_gereration(key)
    for i in range(16):
        left_block = round[i][0:32]
        right_block = round[i][32:]
        B = Expansion_Pbox(right_block)
        C = XOR(B,key_round[15-i],48)
        D = S_Boxes(C)
        E = Straight_permutation_table(D)
        F = XOR(E, left_block,32)
        if i != 15:
            G = right_block + F
        else:
            G = F + right_block
        round.append(G)
    round.pop(0)
    return Final_permutation_Table(round[15])

file_name1 = input("Enter file name encode: ")
import binascii
inp = binascii.hexlify(open(file_name1,"rb").read())
plaintext = open("plaintext.txt","wb+")
plaintext.write(inp)
plaintext.close()

enc = open("plaintext.txt","rb")
enc = enc.read()
dec = open("ciphertext.txt","w+")
for i in range(0,len(enc),16):
    base16 =int(enc[i:i+16],16)
    out = Hexa_out(Encrypt((base16),0x020040080002401),64)[2:]
    if(len(out)<16):
        for i in range(16-len(out)):
            out = '0'+out
    dec.write(out)
dec.close()
    
dec = open("ciphertext.txt","rb").read()

file_name2 = input("Enter file name decode: ")
rec_img = open(file_name2,"wb")
rec = open("rec_text.txt","w+")
for i in range(0,len(dec),16):
    base16 =int(dec[i:i+16],16)
    out = Hexa_out(Decrypt((base16),0x020040080002401),64)[2:]
    if(len(out)<16):
        for i in range(16-len(out)):
            out = '0'+out
    rec.write(out)
rec.close()
rec = open("rec_text.txt","rb").read()
rec_img.write(binascii.unhexlify(rec))
rec_img.close()