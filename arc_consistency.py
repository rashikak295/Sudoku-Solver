import math
import itertools
import time

def print_board(Sudoku):
	print "-------------------------"
	for i in range(0,9):
		if(i%3==0 and i!=0):
			print "-------------------------"
			print "|",
		else:
			print '|', 
		for j in range(0,9):
			var=rowvalues[i]+colvalues[j]
			if(j%3==0 and j!=0):
				print "|", 
			if len(domains[var])==1:
				value=domains[var].pop()
				print str(value) + "",
				domains[var].add(value)
			else:
				print '0', 
		print '|', 
		print ""
	print "-------------------------" 
	
def AC3 (queue):
	removals=[]
	if queue is None:
		queue = []
		for x in variables:
			queue = queue + [(x, y) for y in constraints[x]]
	while queue:
		x,y= queue.pop()
		b,r=arc_reduce(x,y)
		if r:
			removals.extend(r)
		if(b):
			if(len(domains[x])==0):
				return False, removals
			else:
				queue = queue + [(x, z) for z in constraints[x] if z!=y]
	return True, removals

def arc_reduce(x,y):
		removals=[]
		change=False
		for vx in domains[x].copy():
			found=False
			for vy in domains[y]:
				if vx!=vy:
					found=True
			if(not found):
				domains[x].remove(vx)   
				removals.append((x,vx))
				change=True
		return change,removals

def readfile(puzzle):
	global variables,domains,constraints
	def constraints(x, listOfNeighbours):
		constrain_to = set()
		for pair in listOfNeighbours:
			if x in pair:
				if x==pair[0]:
					constrain_to.add(pair[1])
				elif x==pair[1]:
					constrain_to.add(pair[0])
		return constrain_to
	matrix = [[int(x) if x!=0 else 0 for x in line] for line in puzzle]
	neighbours=[]
	for r in rowvalues:
		row = [r+c for c in colvalues]
		neighbours.extend(itertools.combinations(row, 2))
	for c in colvalues:
		col = [r+c for r in rowvalues]
		neighbours.extend(itertools.combinations(col, 2))
	for y in range(0,9,3):
		for x in range(0,9,3):
			box=[rowvalues[i+y]+colvalues[x+j] for i in range(0,3) for j in range(0,3)]
			neighbours.extend(itertools.combinations(box, 2))
	variables = [x+y for x in rowvalues for y in colvalues]
	domains={rowvalues[y]+colvalues[x]:{1,2,3,4,5,6,7,8,9} if matrix[y][x]==0 else {matrix[y][x]} for y in range(0,9) for x in range(0,9)}
	constraints = {x:constraints(x, neighbours) for x in variables}
	return variables,domains,constraints

def selectUnassignedVariable(assigned):
	for var in variables:
		if var not in assigned:
			return var

def OrderDomainValues(assignment, var):
	values = [val for val in domains[var]] 
	return values

def backTrackingSearch():
	return backtrack({})

def backtrack(assignment):
	if not any(len(domains[var])!=1 for var in variables):
		return True
	var = selectUnassignedVariable(assignment)
	for value in OrderDomainValues(assignment, var):
		assignment[var] = value
		removals = [(var, a) for a in domains[var] if a != value]
		domains[var] = {value}
		consistent, removed = AC3([(x,var) for x in constraints[var]])
		if removed:
			removals.extend(removed)
		if(consistent):
			result = backtrack(assignment)
			if(result!=False):
				return result
		for variable, value in removals:
			domains[variable].add(value)
	del assignment[var]
	return False

def main():
	choice = input("""Run on default test cases? (Type 1 for yes and 0 for no): """)
	if choice == 1:
		puzzles = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015']
		level = ['EASY PUZZLES', 'MEDIUM PUZZLES', 'HARD PUZZLES']
		counter = 0
		for i in puzzles:
			if((int(i) - 1 )%5==0):
				print "\n",str(level[counter]),"\n***************"
				counter+=1
			print "\nSolving puzzle ",i
			fd = open("./puzzles/puzzle-"+i+".txt","r+")
			puzzle = eval(fd.readline())
			Sudoku = readfile(puzzle)
			print_board(Sudoku)
			t1=time.time()
			AC3(None)
			print("Attempting AC-3...")
			if(not any(len(domains[var])!=1 for var in variables)):
				print "Sudoku solved by AC-3 only: "
				print_board(Sudoku)
			else:
				print "Sudoku partially solved by AC-3"
				print_board(Sudoku)
				print "Attempting backtrack search..."
				solution = backTrackingSearch()
				t2=time.time()
				if(solution):
					print "Solution found by Backtrack Search: "
					print_board(Sudoku)
					print "Time elapsed: {} seconds".format(t2-t1)
				else:
					print "Backtrack Search unable to find a solution."
	else:
		path = str(input("Mention the path in double-quotes: "))
		print "\nSolving following puzzle "
		fd = open(path,"r+")
		puzzle = eval(fd.readline())
		Sudoku = readfile(puzzle)
		print_board(Sudoku)
		t1=time.time()
		AC3(None)
		print "Attempting AC-3..."
		if(not any(len(domains[var])!=1 for var in variables)):
			print "Sudoku solved by AC-3 only: "
			print_board(Sudoku)
		else:
			print "Sudoku partially solved by AC-3"
			print_board(Sudoku)
			print "Attempting backtrack search..."
			solution = backTrackingSearch()
			t2=time.time()
			if(solution):
				print "Solution found by Backtrack Search: "
				print_board(Sudoku)
				print "Time elapsed: {} seconds".format(t2-t1)	
			else:
				print "Backtrack Search unable to find a solution."
if __name__ == "__main__":
	rowvalues = "QWERTYUIO"
	colvalues = "ASDFGHJKL"
	variables = domains = constraints =  list()
	main()