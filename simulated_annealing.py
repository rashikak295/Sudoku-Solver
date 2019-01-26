import time
import numpy as np
from random import shuffle, random, sample, randint
from copy import deepcopy
from math import exp

def get_column_indices(i, type="data index"):
	if type=="data index":
		column=1%9
	elif type=="column index":
		column = i
	indices = [column + 9 * j for j in range(9)]
	return indices
        
def score_board(input):
	score = 0
	for row in range(9):
		score-= len(set(input[get_row_indices(row, type="row index")]))
	for col in range(9):
		score -= len(set(input[get_column_indices(col,type="column index")]))
	return score

def make_neighborBoard(input, initialEntries):
    new_data = deepcopy(input)
    block = randint(0,8)
    num_in_block = len(get_block_indices(block,initialEntries,ignore_originals=True))
    random_squares = sample(range(num_in_block),2)
    square1, square2 = [get_block_indices(block,initialEntries,ignore_originals=True)[ind] for ind in random_squares]
    new_data[square1], new_data[square2] = new_data[square2], new_data[square1]
    return new_data
    
def get_block_indices(k,initialEntries,ignore_originals=False):
	row_offset = (k//3)*3
	col_offset= (k%3)*3
	indices=[col_offset+(j%3)+9*(row_offset+(j//3)) for j in range(9)]
	if ignore_originals:
		indices = filter(lambda x:x not in initialEntries, indices)
	return indices
    
def randomAssign(input, initialEntries):
	for num in range(9):
		block_indices=get_block_indices(num, initialEntries)
		block= input[block_indices]
		zero_indices=[ind for i,ind in enumerate(block_indices) if block[i] == 0]
		to_fill = [i for i in range(1,10) if i not in block]
		shuffle(to_fill)
		for ind, value in zip(zero_indices, to_fill):
			input[ind]=value	

def get_row_indices(i, type="data index"):
    if type=="data index":
        row = i // 9
    elif type=="row index":
        row = i
    indices = [j + 9*row for j in range(9)]
    return indices

def viewResults(input):
	def checkZero(s):
		if s != 0: return str(s)
		if s == 0: return "0"
	results = np.array([input[get_row_indices(j, type="row index")] for j in range(9)])
	s=""
	for i, row in enumerate(results):
		if i%3==0:
			s +="-"*25+'\n'
		s += "| " + " | ".join([" ".join(checkZero(s) for s in list(row)[3*(k-1):3*k]) for k in range(1,4)]) + " |\n"
	s +="-"*25+''
	print s

def solve(input, initialEntries):
	start_time = time.time()
	print "Solving the following puzzle using simulated annealing: "
	viewResults(input)
	randomAssign(input, initialEntries)
	best_input = deepcopy(input)
	current_score = score_board(input)
	best_score = current_score
	T = .5
	count = 0
	while (count < 400000):
		try:
			if (count % 10000 == 0): 
				print "Iteration %s,     \tTemperaure = %.5f,\tBest score = %s,\tCurrent score = %s"%(count, T, best_score, current_score)
			neighborBoard = make_neighborBoard(input, initialEntries)
			neighborBoardScore = score_board(neighborBoard)
			delta = float(current_score - neighborBoardScore)
			if (exp((delta/T)) - random() > 0):
				input = neighborBoard
				current_score = neighborBoardScore 
			if (current_score < best_score):
				best_input = deepcopy(input)
				best_score = score_board(best_input)
			if neighborBoardScore == -162:
				input = neighborBoard
				break
			T = .99999*T
			count += 1
		except:
			print "Numerical error occurred. It's a random algorithm so try again."            
	end_time = time.time() 
	if best_score == -162:
		print "Solution:"
		viewResults(input)
		print "It took", end_time - start_time, "seconds to solve this puzzle."
	else:
		print "Couldn't solve! (%s/%s points). It's a random algorithm so try again."%(best_score,-162)

if __name__=="__main__":
		choice = input("""Run on default testcases? (Type 1 for yes and 0 for no): """)
		if choice == 1: 
			puzzles =  ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015']
			level = ['EASY PUZZLES', 'MEDIUM PUZZLES', 'HARD PUZZLES']
			counter = 0
			for i in puzzles:
				if((int(i) - 1 )%5==0):
					print "\n",str(level[counter]),"\n***************"
					counter+=1
				print "\nSolving puzzle ",i
				fd = open("./puzzles/puzzle-"+i+".txt","r+")
				puzzle = eval(fd.readline())
				array = []
				for row in puzzle:
					for col in row:
						array.append(col)
				puzzle=np.array(array)
				original_entries=np.arange(81)[puzzle > 0]
				solve(puzzle, original_entries)
		else:
			path = str(input("Mention the path in double-quotes: "))
			print "\nSolving puzzle "
			fd = open(path,"r+")
			puzzle = eval(fd.readline())
			array = []
			for row in puzzle:
				for col in row:
					array.append(col)
			puzzle=np.array(array)
			original_entries=np.arange(81)[puzzle > 0]
			solve(puzzle, original_entries)