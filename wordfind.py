from random import randint
import numpy as np
import copy



# Edit this with words you want to find
w_list = ['learn', 'cat', 'howdy', 'commit', 'python']

# Edit this if you want to output the hidden words in capital letters
print_key = False

class Puzzle():
	'''Creates a word search puzzle '''
	
	def __init__(self, word_list, rows = 15, cols = 15):
		
		self.rows = rows
		self.cols = cols
		self.word_list = word_list
		
		max_length = 0
		for word in word_list: 
			length = len(word)
			if length > max_length:
				max_length = length
 
 		min_length = max([max_length + 4, int(np.floor( 0.002* (len(word_list)-20) - 0.05 * (len(word_list)-20)**2 + 25)), 10])
		
		if self.rows < min_length: 
			self.rows = min_length

		if self.cols < min_length:
			self.cols = min_length
		
		# initialize the board
		self.board = [["a"] * self.cols for i in range(self.rows)]
		self.num_diagonals = self.rows + self.cols - 1

		# fill the board with random letters
		for i in range(self.rows):
			for j in range(self.cols):
				self.board[i][j] = chr(randint(97, 122))
				
		
	def print_board(self, board = None):
		'''print either self.board or another board'''
		if board == None:
			board = copy.deepcopy(self.board)
		board = board[::-1]
		for row in board:
			print('   '.join(row))
		print()
	
	def s_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = [[] for x in range(self.cols)]
		for row in board:
			for i, letter in enumerate(row):
				rows[i].append(letter)
		rows = [''.join(x) for x in rows]
		return rows
	
	def n_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = self.s_rows(board)
		for i,row in enumerate(rows):
			rows[i] = row[::-1]
		return rows
	
	def e_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = []
		for row in board:
			rows.append(''.join(row))
		return rows
	
	def w_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = self.e_rows(board)
		for i,row in enumerate(rows):
			rows[i] = row[::-1]
		return rows
		
	def ne_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
			
		rows = [[] for x in range(self.num_diagonals)]
		max_length = min([self.rows, self.cols])
		for i in range(self.num_diagonals):
			if i < max_length:
				for j in range(i+1):
					rows[i].append(board[i-j][j])
			elif i <= self.num_diagonals - max_length:
				if self.rows > self.cols:
					for j in range(max_length):
						rows[i].append(board[i-j][j])
				else:
					for j in range(max_length):
						rows[i].append(board[self.rows - 1 - j][i - self.rows + 1 + j])
			else:
				for j in range(self.num_diagonals - i):
					rows[i].append(board[self.rows - 1 - j][i - self.rows + 1 + j])
			
		rows = [''.join(x) for x in rows]	
		return rows
	
	def nw_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = self.se_rows(board)
		for i,row in enumerate(rows):
			rows[i] = row[::-1]
		return rows
			
	
	def se_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		board = board[::-1]
		rows = self.ne_rows(board)
		return rows
	
	def sw_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
		rows = self.ne_rows(board)
		for i,row in enumerate(rows):
			rows[i] = row[::-1]
		return rows
	
	def all_rows(self, board = None):
		if board == None:
			board = copy.deepcopy(self.board)
			
		rows = [self.n_rows(board), self.s_rows(board), self.e_rows(board), self.w_rows(board), self.ne_rows(board), self.se_rows(board), self.nw_rows(board), self.sw_rows(board)]
		
		for i,row in enumerate(rows):
			rows[i] = '|'.join(row)
		
		rows = '^'.join(rows)

		return rows
		
	def add_word(self, word, position = 'random', orientation = 'random'):
		'''You can optionally add a word at a given [x, y] pair, and at a given direction [dir_x, dir_y]
			where dir_x and dir_y can be -1, 0, or 1'''
		new_board = copy.deepcopy(self.board)
		word_length = len(word)
		
		n = len(new_board[0])
		m = len(new_board)

		
		if position == 'random':
			position = [randint(0, n-1), randint(0, m-1)]
		if orientation == 'random':
			or1 = randint(-1, 1)
			or2 = randint(-1, 1)
			while or1 == 0 and or2 == 0: # orientation can't be [0,0], or the word won't go anywhere
				or1 = randint(-1, 1)
				or2 = randint(-1, 1)
			orientation = [or1, or2]
		
		loop_iteration = 0
		fit = 1
		while position[1] + orientation[1] * word_length > m -1 or position[1] + orientation[1] * word_length < 0 or position[0] + orientation[0] * word_length > n -1 or position[0] + orientation[0] * word_length < 0:
		# the while loop checks to make sure that for a given orientation and starting position,
		# the word will fit in the board
			position = [randint(0, n-1), randint(0, m-1)]
			or1 = randint(-1, 1)
			or2 = randint(-1, 1)
			while or1 == 0 and or2 == 0:
				or1 = randint(-1, 1)
				or2 = randint(-1, 1)
			orientation = [or1, or2]
			loop_iteration+=1
			if loop_iteration > 10: 
				fit = 0
				break
		if fit == 1:
			for i, letter in enumerate(word): # replace the old letters with the letters of the word
				new_board[position[1] + orientation[1] * i][position[0] + orientation[0] * i] = letter
		return new_board

	
	def generate_board(self):
		'''Iterates through the words, calling the add_word function. Ensures that the new word placed
		   doesn't overwrite any old words'''
		remaining_words = [word.upper() for word in self.word_list]
		remaining_words.sort(key = len)
		remaining_words = remaining_words[::-1] # Longer words are placed first
		used_words = []
		
		while len(remaining_words) > 0:
			proposed_board = self.add_word(remaining_words[0])
			used_words.append(remaining_words[0])
			all_r = self.all_rows(proposed_board)
			loop_it = 0
			while not (all([word in all_r for word in used_words])):
				proposed_board = self.add_word(remaining_words[0])
				all_r = self.all_rows(proposed_board)
				loop_it += 1
				if loop_it > 10:
					print('Board not able to be created, please try again, specifying a larger board size...')
					quit()

			remaining_words = remaining_words[1:]
			self.board = proposed_board
			
	def print_hidden(self):
		'''Prints out the final board, with the letters converted back to lowercase'''
		board = copy.deepcopy(self.board)
		words = '   '.join(self.word_list)
		for i in range(self.rows):
			for j in range(self.cols):
				board[i][j] = board[i][j].lower()
		self.print_board(board)
		print('\nWords to find:')
		print(words)

MyPuzzle = Puzzle(w_list)
MyPuzzle.generate_board()
MyPuzzle.print_hidden()
if print_key == True:
	print('\nKey:')
	MyPuzzle.print_board()
