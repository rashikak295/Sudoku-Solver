import math
import random
import time

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

def empty(lst,l):
	for row in range(9):
		for col in range(9):
			if(lst[row][col]==0):
				l[0]=row
				l[1]=col
				return True
	return False
 
def usedRow(lst,row,num):
	for i in range(9):
		if(lst[row][i] == num):
			return False
	return True

def usedCol(lst,col,num):
	for i in range(9):
		if(lst[i][col] == num):
			return False
	return True

def usedBox(lst,row,col,num):
	row = row - row%3
	col = col - col%3
	for i in range(3):
		for j in range(3):
			if(lst[i+row][j+col] == num):
				return False
	return True

def safe(lst,row,col,num):
	return usedRow(lst,row,num) and usedCol(lst,col,num) and usedBox(lst,row,col,num)
 
def solve(lst):
	l=[0,0]
	if(not empty(lst,l)):
		return True
	row=l[0]
	col=l[1]
	for num in range(1,10):
		if(safe(lst,row,col,num)):
			lst[row][col]=num
			if(solve(lst)):
				return True
			lst[row][col] = 0      
	return False

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
			print "Solving the following puzzle using backtracking: "
			printPuzzle(puzzle)
			start_time = time.time()
			result = solve(puzzle)
			end_time = time.time()
			if(result):
				print "Solution:"
				printPuzzle(puzzle)
				print "It took", end_time - start_time, "seconds to solve this puzzle."
			else:
				print "No solution exists"
	else:
		path = str(input("Mention the path in double-quotes: "))
		print "\nSolving puzzle "
		fd = open(path,"r+")
		puzzle = eval(fd.readline())
		print "Solving the following puzzle using backtracking: "
		printPuzzle(puzzle)
		start_time = time.time()
		result = solve(puzzle)
		end_time = time.time()
		if(result):
			print "Solution:"
			printPuzzle(puzzle)
			print "It took", end_time - start_time, "seconds to solve this puzzle."
		else:
			print "No solution exists"
main()