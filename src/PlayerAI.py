#!/usr/bin/env python
#coding:utf-8

from BaseAI import BaseAI

class PlayerAI(BaseAI):
	def getMove(self, grid):
		
		result = self.alphabeta(grid, 4, -10000, 10000, 'Player')
		move = result[1]
		return move
	
	'''alpha beta function, returns a list [score, bestMove]'''
	def alphabeta(self, grid, depth, alpha, beta, ai):
		if grid.canMove() == False:
			return [self.totalScore(grid), None]
		if depth == 0:
			return [self.totalScore(grid), None]
		if ai == 'Player':
			v = -10000 #initialize result
			nextMoves = grid.getAvailableMoves()
			nextStates = [] #initialize list that stores the next states
			for m in nextMoves:
				newGrid = grid.clone()
				newGrid.move(m)
				temp = [newGrid, m] #stores each new state and the corresponding move
				nextStates.append(temp)
			for s in nextStates:
				vtmp = self.alphabeta(s[0], depth - 1, alpha, beta, 'Computer')
				if vtmp > v:
					v = vtmp
					bestMove = s[1]
				if v >= beta:
					return [v, bestMove]
				alpha = max(alpha, v)
			#print str(depth) + '---max---' + str(v) +',' + str(bestMove)
			return [v, bestMove]
		if ai == 'Computer':
			v = 10000
			nextStates = [] #initialize list that stores the next states
			emptyCells = grid.getAvailableCells()
			for c in emptyCells: #populates each empty cell with a 2 tile and adds new state to nextStates
				i, j = c
				newGrid = grid.clone()
				newGrid.map[i][j] = 2
				nextStates.append(newGrid)
			for d in emptyCells: #populates each empty cell with a 4 tile and adds new state to nextStates
				k, l = d
				newGrid = grid.clone()
				newGrid.map[k][l] = 4
				nextStates.append(newGrid)
			for s in nextStates:
				v = min(v, self.alphabeta(s, depth - 1, alpha, beta, 'Player')[0])
				if v <= alpha:
					return v
				beta = min(beta, v)
			#print str(depth) + '---------' + str(v)
			return v
	
	'''calculates total score of a state using various heuristic functions'''
	def totalScore(self, grid):
		return self.snakeScore(grid) + self.emptyTilesScore(grid)
	
	def gradientScore(self, grid):
		score1 = (grid.map[0][0]*3 + grid.map[0][1]*2 + grid.map[1][0]*2 + grid.map[0][2]*1 + grid.map[1][1]*1
				+ grid.map[2][0]*1 + grid.map[1][3]*-1 + grid.map[2][2]*-1 + grid.map[3][1]*-1 + grid.map[2][3]*-2
				+ grid.map[3][2]*-2 + grid.map[3][3]*-3)
		
		score2 = (grid.map[0][3]*3 + grid.map[0][2]*2 + grid.map[1][3]*2 + grid.map[0][1]*1 + grid.map[1][2]*1
				+ grid.map[2][3]*1 + grid.map[1][0]*-1 + grid.map[2][1]*-1 + grid.map[3][2]*-1 + grid.map[2][0]*-2
				+ grid.map[3][1]*-2 + grid.map[3][0]*-3)
		
		score3 = (grid.map[3][0]*3 + grid.map[2][0]*2 + grid.map[3][1]*2 + grid.map[3][2]*1 + grid.map[2][1]*1
				+ grid.map[1][0]*1 + grid.map[2][3]*-1 + grid.map[1][2]*-1 + grid.map[0][1]*-1 + grid.map[1][3]*-2
				+ grid.map[0][2]*-2 + grid.map[0][3]*-3)
		
		score4 = (grid.map[3][3]*3 + grid.map[2][3]*2 + grid.map[3][2]*2 + grid.map[1][3]*1 + grid.map[2][2]*1
				+ grid.map[3][1]*1 + grid.map[0][2]*-1 + grid.map[1][1]*-1 + grid.map[2][0]*-1 + grid.map[0][1]*-2
				+ grid.map[1][0]*-2 + grid.map[0][0]*-3)
		
		score = max(score1, score2, score3, score4)
		return score
	
	def snakeScore(self, grid):
		score = 0
		r = 0.125
		def calcScore(x, y):
			return x * pow(r, y)
		score1 = (score + calcScore(grid.map[0][0], 0) + calcScore(grid.map[0][1], 1) + calcScore(grid.map[0][2], 2)
			+ calcScore(grid.map[0][3], 3) + calcScore(grid.map[1][3], 4) + calcScore(grid.map[1][2], 5)
			+ calcScore(grid.map[1][1], 6) + calcScore(grid.map[1][0], 7) + calcScore(grid.map[2][0], 8)
			+ calcScore(grid.map[2][1], 9) + calcScore(grid.map[2][2], 10) + calcScore(grid.map[2][3], 11)
			+ calcScore(grid.map[3][3], 12) + calcScore(grid.map[3][2], 13) + calcScore(grid.map[3][1], 14)
			+ calcScore(grid.map[3][0], 15))
		
		score2 = (score + calcScore(grid.map[0][0], 0) + calcScore(grid.map[1][0], 1) + calcScore(grid.map[2][0], 2)
			+ calcScore(grid.map[3][0], 3) + calcScore(grid.map[3][1], 4) + calcScore(grid.map[2][1], 5)
			+ calcScore(grid.map[1][1], 6) + calcScore(grid.map[0][1], 7) + calcScore(grid.map[0][2], 8)
			+ calcScore(grid.map[1][2], 9) + calcScore(grid.map[2][2], 10) + calcScore(grid.map[3][2], 11)
			+ calcScore(grid.map[3][3], 12) + calcScore(grid.map[2][3], 13) + calcScore(grid.map[1][3], 14)
			+ calcScore(grid.map[0][3], 15))
		
		score = max(score1, score2)
		'''
		if grid.map[0][0] != grid.getMaxTile(): #penalty for moving max tile from corner
			score = 0.65 * score
		'''
		if grid.map[0][0] == grid.getMaxTile(): #award bonus for keeping max tile in corner
			score1 = 1.25 * score1
		
		return score1
	
	def emptyTilesScore(self, grid):
		score = 0
		for i in range(grid.size):
			for j in range(grid.size):
				if grid.map[i][j] == 0:
					score += 1
		return score
