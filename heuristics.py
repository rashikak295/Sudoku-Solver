import math
import random
import time

def degreeHeuristics( square, puzzle ):
	row = square[0]
	col = square[1]
	d = 0
	for i in range(9):
		if i == col:
			continue                
		if puzzle[row][i] == 0:
			d+=1
	for i in range(9):
		if i == row:
			continue
		if puzzle[i][col] == 0:
			d+=1
	block_row = row/3
	block_col = col/3  
	for i in range(3):
		for j in range(3):            
			if [block_row*3+i, block_col*3+j] == [row, col]:
				continue        
			if puzzle[block_row*3+i][block_col*3+j] == 0:
				d+=1
	return d         

def leastConstraintingValueHeuristics( values, row, col, forwardboard ):
	lcvList = []
	for v in values: 
		count = 0   
		for i in range(9):
			if i == col:
				continue           
			x = forwardboard[row*9+i]                    
			if v in x:
				count += 1
		for i in range(9):
			if i == row:
				continue                
			x = forwardboard[col+9*i]
			if v in x:
				count += 1
		block_row = row/3
		block_col = col/3  
		for i in range(3):
			for j in range(3):                
				if [block_row*3+i, block_col*3+j] == [row, col]:
					continue            
				x = forwardboard[block_col*3+j+(block_row*3+i)*9]
				if v in x:
					count += 1 
		lcvList.append( count )
	return lcvList

def forwardCheck( forwardboard, value, row, col ):    
	for i in range(9):
		if i == col:
			continue
		x = forwardboard[row*9+i]
		if len(x) == 1:
			if x[0] == value:
				return 0
	for i in range(9):
		if i == row:
			continue
		x = forwardboard[col+9*i]
		if len(x) == 1:
			if x[0] == value:
				return 0
	block_row = row/3
	block_col = col/3  
	for i in range(3):
		for j in range(3):
			if [block_row*3+i, block_col*3+j] == [row, col]:
				continue            
			x = forwardboard[block_col*3+j+(block_row*3+i)*9]
			if len(x) == 1:
				if x[0] == value:
					return 0                                  
	return 1                          

def getvalues( puzzle ):
	forwardboard = []
	[forwardboard.append( range(1,10) ) for i in range(81) ]    
	for row in range( len(puzzle) ):
		for col in range( len(puzzle[1]) ):
			if puzzle[row][col] != 0:  
				value = puzzle[row][col]  
				forwardboard = removeValues( row, col, value, forwardboard )   
	return forwardboard     

def removeValues( row, col, value, forwardboard ):
	forwardboard[col+row*9] = [0]
	for x in forwardboard[row*9:row*9+9]:
		try:
			x.remove( value )
		except ValueError:  
		   pass 
	for i in range(9):
		try:
			forwardboard[col+9*i].remove( value )
		except ValueError:
			pass
	block_row = row/3
	block_col = col/3  
	for i in range(3):
		for j in range(3):
			try:
				forwardboard[block_col*3+j+(block_row*3+i)*9].remove( value )
			except ValueError:
				pass
	return forwardboard
		
def empty(puzzle):
	empty_squares = []
	for row in range(len( puzzle )):
		for col in range(len( puzzle[1] )):
			if puzzle[row][col] == 0:
				empty_squares.append( [row,col] ) 
	return empty_squares  

def solve( puzzle ):    
	empty_squares = empty( puzzle )
	if len(empty_squares) == 0: 
		print "Solution:"
		printPuzzle( puzzle )
		return 1
	forwardboard = getvalues( puzzle )
	mvrList = []
	[ mvrList.append( len( forwardboard[ square[0]*9+square[1] ] ) ) for square in empty_squares ]
	mvrSquares = []
	minimum = min( mvrList )
	for i in range(len(mvrList)):
		val = mvrList[i]
		if val == minimum:
			mvrSquares.append( empty_squares[i] )
	if len( mvrSquares ) == 1:
		square = mvrSquares[0]
	else:
		degree_list = []
		for cell in mvrSquares:  
			d = degreeHeuristics( cell, puzzle )
			degree_list.append( d )
			maxDegree = max( degree_list )
			maxDegreeSquares = []
			for i in range(len(degree_list)):      
				val = degree_list[i]
				if val == maxDegree:
					maxDegreeSquares.append( mvrSquares[i] )
			square = maxDegreeSquares[0]
	row = square[0]
	col = square[1]
	values = list( forwardboard[col+row*9] )
	while len( values ) != 0:        
		lcvList = leastConstraintingValueHeuristics( values, row, col, forwardboard )
		val = values[ lcvList.index( min( lcvList ) ) ]
		values.remove(val)        
		if forwardCheck( forwardboard, val, row, col ):
			puzzle[row][col] = val
			if solve( puzzle ):
				return 1
			else:
				puzzle[row][col] = 0
	return 0

def printPuzzle(lst):
	for i in range(9):
		if (i) % 3 == 0:
			print "-------------------------"
		for j in range(9):
			if j == 0:
				print "|", 
			print lst[i][j],
			if (j+1) % 3 == 0:
				print "|",
		print " "
	print "-------------------------"

def main():
	choice = input("""Run on default test cases? (Type 1 for yes and 0 for no): """)
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
			print "Solving the following puzzle using backtracking with forward checking and heuristics on vertex order and value/vertex order: "
			printPuzzle (puzzle)
			start_time = time.time()
			result = solve(puzzle)
			end_time = time.time()
			if result:
				print "It took ", end_time - start_time," seconds to solve this puzzle."
			else:
				print "No solution exists"
	else:
		path = str(input("Mention the path in double-quotes: "))
		print "\nSolving puzzle "
		fd = open(path,"r+")
		puzzle = eval(fd.readline())
		print "Solving the following puzzle using backtracking with forward checking and heuristics on vertex order and value/vertex order: "
		printPuzzle (puzzle)
		start_time = time.time()
		result = solve(puzzle)
		end_time = time.time()
		if result:
			print "It took ", end_time - start_time," seconds to solve this puzzle."
		else:
			print "No solution exists"
main()