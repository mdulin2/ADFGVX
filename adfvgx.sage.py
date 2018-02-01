# This file was *autogenerated* from the file adfvgx.sage
from sage.all_cmdline import *   # import sage library
_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_65 = Integer(65); _sage_const_48 = Integer(48); _sage_const_10 = Integer(10); _sage_const_26 = Integer(26); _sage_const_6 = Integer(6)
import random
import math
import numpy as np

def make_num_list():
	"""
	Creates a list to reference the spots in the matrix.
	Returns:
		num_list(list of tuples(int,int)): each spot in the list is a tuple that corresponds
				to a different spot on the matrix.
	"""

	num_list = list()
	for row in range(6):
		for col in range(6):
			num_list.append((row,col))
	return num_list

def make_key():
	"""
	Creates a key for the algorithm using randomly generated numbers.
	If the test is being returned, then the answer will always be the same.
	Returns:
		key(matrix, 6 by 6, chars: a matrix representing the ADFGVX key.
	"""
	
	xy_letters = ['A','D','F','G','V','X']
	all_letters = []
	#creates a list to represent each spot in the key.
	num_list = make_num_list()
	x = _sage_const_0 ;
	y = _sage_const_0 ;

	#puts all of the letters and numbers into an array
	for letter in range(_sage_const_10 ):
		all_letters.append(chr(letter + _sage_const_48 ))
	for letter in range(_sage_const_26 ):
		all_letters.append(chr(letter + _sage_const_65 ))
	#creates a
	key = np.chararray((6,6))
	size = len(num_list)
	#randomly puts the key together
	for spot in num_list:
		#matrix indexes
		row = spot[0]
		col = spot[1]
		#spot in the all_letters list
		rand_spot = random.randint(0,size-1)
		#random letter
		rand_letter = all_letters[rand_spot]
		#remove the letter from the list
		all_letters.remove(rand_letter)
		#inserting into a numpy matrix (starts at (0,0), not (1,1)
		key[row,col] = rand_letter
		#subtracts one from size
		size-=1


	row1 = ['F','L','1','A','O','2']
	row2 = ['J','D','W','3','G','U']
	row3 = ['C','I','Y','B','4','P']
	row4 = ['R','5','Q','8','V','E']
	row5 = ['6','K','7','Z','M','X']
	row6 = ['S','N','H','0','T','9']

	my_list = [row1,row2,row3,row4,row5,row6]
	test = np.chararray((6,6))

	for row in range(6):
		for col in range(6):
			test[row,col] = my_list[row][col]
	return test

def get_spot(key, letter):
	"""
	Gets the location of a character of a letter on the key
	Args:
		key(matrix): the key for the encryption algorithm, 6x6 matrix
		letter(string): the character that is being searched for.
	Returns:
		row,col(tuple of ints): the location of the character in the matrix
	"""

	go = True
	for row in range(6):
		for col in range(6):
			if(letter == key[row,col]):
				return row,col

def get_letter_encrypt(key, letter):
	"""
	Gets the encrypted form of the letter
	Args:
		key(matrix): the key for the encryption algorithm, 6x6 matrix
		letter(string): the letter that is being encrypted
	Returns:
		tuple: the two characters that directly reflects the matrix.
	"""

	xy_letters = ['A','D','F','G','V','X']
	#the indexes of the letter on the key
	top,bottom = get_spot(key, letter)
	#the new encryted spot
	# in the form of a tuple, this could be changed for something nicer...
	return xy_letters[top],xy_letters[bottom]

def parse(message):
	"""
	Takes out all non alpha-numeric characters
	Args:
		message(string): the string to be parsed
	Returns:
		message(string): the original message with only alpha-numeric characters
	"""

	message = message.upper()
	outmessage = ""
	for char in message:
		if char.isalpha() or char.isdigit():
			outmessage += char
	return outmessage #outmessage

#	"""
#	Creates a list of the second step in the encryption.
#	"""
def col_encrypt(key,message):
	col_list = list()
	for char in message:
		letter1, letter2 = get_letter_encrypt(key,char)
		col_list.append(letter1)
		col_list.append(letter2)
	return col_list

def horizontal_matrix_encrypt(word_key, col_list):
	"""
	Returns the third step of the encryption algorithm
	Args:
		word_key(string): the word key of theh algorithm
		col_list(list of the 2 by n matrix, string): third step of encryption algorithm
				in the form ['A','T'...]
	Returns:
		The final encrypted string
	"""

	#Gets the size of the matrix needed
	col_num = len(word_key)

	row_num = math.ceil((len(col_list)) / float(len(word_key)))

	#fills the matrix with all X's
	encrypted = np.chararray((int(row_num),col_num))
	encrypted[:] = 'X'
	row = 0
	col = 0

	#Changes the list of char's into the matrix.
	for iteration in range(len(col_list)):
		encrypted[row,col] = col_list[iteration]
		if(col_num-1 == col):
			col = 0
			row +=1
		else:
			col+=1
	return alphabetize(word_key, encrypted)

def create_dict_order(word_key):
	"""
	Creates a dictionary that represents the spot of the column swap in the alphabetize step
	Args:
		word_key(string): the word that the algorithm is encrypting by
	Returns:
		dictionary(key: letter; value: location in matrix)
	"""

	char_order = dict()
	spot = 0
	for char in word_key:
		char_order[char] = spot
		spot+=1
	return char_order

def swap_col(matrix_swap, encrypt, col_num, new_col):
	"""
	Swaps a single column
	Args:
		matrix_swap(matrix): full of the encrypted string, but not the swap.
		encrypt(matrix): the final project of the swapping encryption.
		col_num(int): the spot in matrix_swap that's being put into encrypt
		new_col(int): the spot in encrypt matrix that the swap is being put into

	"""

	row,col = matrix_swap.shape
	for i in range(row):
		encrypt[i,new_col] = matrix_swap[i,col_num]
	return encrypt

def alphabetize(word_key, encrypted_matrix):
	"""
	Reordered the matrix based upon the realphabetize technique of the key
	Args:
		word_key(string): a word that's the key encryption
		encrypted(matrix): the encrypted matrix to be alphabetized
	Returns:
		final(matrix): the matrix that has the columns properly switched.
	"""

	#the reordered string
	char_order = list()

	for char in word_key:
		#print char
		char_order.append(char)
	char_order.sort()
	spot_dict = create_dict_order(word_key)

	#Creates a new matrix
	final = np.copy(encrypted_matrix)
	for spot in range(len(word_key)):
		old_col = spot_dict[char_order[spot]]
		final = swap_col(encrypted_matrix,final,old_col,spot)
	return final

def set_string(encrypt_string):
	"""
	Changes the matrix into a string
	Args:
		encrypt_string(matrix): the matrix being transferred into a string
	Returns:
		string: the final encryted string
	"""

	#turns the matrix into a string
	final_string = ""
	row_num, col_num = encrypt_string.shape
	#these are switched because of the matrix to string algorithm
	for row in range(col_num):
		for col in range(row_num):
			final_string+= encrypt_string[col,row]

	"""
	#adds more X's to the string if not divided into groups of 6.
	go = True
	while(go == True):
		if(len(final_string) % 6 == 0):
			go = False
		else:
			final_string+='X'
	"""

	#Divides the string into groups of 6.
	spot = 0
	format_string = ""
	for char in final_string:
		if(spot % 6 == 0):
			format_string += " "
		format_string += char
		spot+=1

	return format_string

def createCENPRTY(decKeyword, wKeyRows, wKeyCols):
	#create 2D matrix/ array with dimensions wKeyRows x wKeyCols
	#initialzed to lowerclase x so we can see if the characters are being
	#inputted correctly
	grid = np.chararray((wKeyRows,wKeyCols))
	#iterate through nested for loops to enter the characters of decKeyword
	#into the grid
	count = 0
	for i in range(0,wKeyCols):
		for j in range(0,wKeyRows):
			grid[j,i] = decKeyword[count]
			count+=1

	return grid

def decryptAlphabatize(gridCENPRTY,wKeyRows, wKeyCols, jumbledKeyword,alphabatizedKeyword):
	# Unalphabetize the CENPRTY table to match the letters in the key word.
	# Returns the dealphabetized table.
	gridENCRYPT = np.chararray((wKeyRows,wKeyCols))
	for i in range(len(alphabatizedKeyword)):
		for j in range(len(jumbledKeyword)):
			if(jumbledKeyword[j] == alphabatizedKeyword[i]):
				swap_col(gridCENPRTY, gridENCRYPT, i, j)

	return gridENCRYPT

def getFinalMessage(gridENCRYPT, keyword, wKeyCols, wKeyRows, key):
	print "Our key from before:"
	ciphertext = ""
	for i in range(wKeyRows):
		for j in range(wKeyCols):
			ciphertext += gridENCRYPT[i][j]

	print "Ciphertext: " + ciphertext
	message = ""
	i = 0
	while i < len(ciphertext) - 1:
		message += getChar(ciphertext[i], ciphertext[i + 1], key)
		i += 2

	#print "Message: " + message
	return message

def getChar(rowChar, colChar, gridEncrypt):
	word = "ADFGVX"

	rowIndex = getIndex(rowChar, word)
	colIndex = getIndex(colChar, word)

	if(rowIndex == -1 or colIndex == -1):
		print "CANNOT DECRYPT"
	else:
		character = gridEncrypt[rowIndex, colIndex]
		return character

	raise Exception("Decryption Error")


def getIndex(thisChar, word):
	for i in range(len(word)):
		if(thisChar == word[i]):
			return i

	return -1


def encrypt(message,word_key, key):
	#probably should be parsing stuff here...
	#need to take out spaces and such
	message = parse(message)
	print message
	col_list = col_encrypt(key,message)
	final_matrix = horizontal_matrix_encrypt(word_key, col_list)
	return set_string(final_matrix)
	#return horizontal_matrix_encrypt(key, col_list)

def decrypt(ciphertext, keyword, key):
	# takes ciphertext, returns playtext.
	#1. alphabetize keyword
	decKeyword = sorted(keyword)
	ciphertext = ciphertext.replace(" ","")
	#2. floor[length of ciphertext/ length of keyword]
	wKeyRows = floor(len(ciphertext) / len(keyword))
	#3. put remaining letters in grid
	#insert alg to create 2D array of dimensions wKeyRows x wKeyCols
	wKeyCols = len(keyword)


	gridCENPRTY = createCENPRTY(ciphertext, wKeyRows, wKeyCols)
	#4. rearrange columns to match non- alphabetized keyword
	#rearrange to match decKeyword
	gridENCRYPT = decryptAlphabatize(gridCENPRTY,wKeyRows, wKeyCols, keyword, decKeyword)
	#5. translate rows/cols to string
	#extract letters in sets of two, copy to string letterRowCols
	finalString = getFinalMessage(gridENCRYPT, keyword, wKeyCols, wKeyRows, key)

	return finalString

def main():
	word_key = "ENCRYPT"
	plaintext = "super cali fragilistic expialidocious"

	key = make_key()
	ciphertext = encrypt(plaintext,word_key, key)
	print ciphertext
	decrypted = decrypt(ciphertext, word_key, key)
	print "Decrypted: " + decrypted

main()
