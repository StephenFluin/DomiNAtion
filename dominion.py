#!/usr/bin/python


import sys,random

def main():
	print "Creating cards"
	g = Game()
	g.addPlayer("stephen")
	
	runConsoleGame(g)
	
	
	
def runConsoleGame(game):
	g = game
	gameOver = False
	while not gameOver:
		#Give each player a turn
		for p in g.players:
			p.draw(g)
			print "Hand:",
			for c in p.hand:
				print "%s" % (c.name),
			print
			actions = 1
			buys = 1
			
			
			#Action Phase
			while actions > 0:
				print "Enter the name of an action card or type skip:"
				line = sys.stdin.readline()
				line = line.strip('\n\r')
				print "You entered '%s'." % (line)
				actions -= 1
			
			
			#Buy Phase
			while buys > 0:
				print "Enter the name of a card you wish to buy:"
				line = sys.stdin.readline()
				line = line.strip('\n\r')
				print "You entered '%s'." % (line)
				buys -= 1
			
			p.endTurn()
				

class Game():
	def __init__(self):
		self.estates = []
		self.duchies = []
		self.provinces = []
		self.golds = []
		self.silvers = []
		self.coppers = []
		self.trash = []
		self.players = []
		
		for i in range(12):
			self.estates.append(Estate())
			self.duchies.append(Duchy())
			self.provinces.append(Province())
			
		for i in range(50):
			self.golds.append(Gold())
			self.silvers.append(Silver())
			self.coppers.append(Copper())
	
	def addPlayer(self,name):
		self.players.append(Player(self,name))


class Player():
	def __init__(self, game,name):
		self.name = name
		self.hand = []
		self.deck = []
		self.discard = []
		for i in range(7):
			self.deck.append(game.coppers.pop())
		for i in range(3):
			self.deck.append(game.estates.pop())
		random.shuffle(self.deck)
			
	def draw(self,game):
		for i in range(5):
			if len(self.deck) <= 0:
				while len(self.discard) > 0:
					self.deck.append(self.discard.pop())
				random.shuffle(self.deck)
			if len(self.deck) > 0:
				self.hand.append(self.deck.pop())
	def endTurn(self):
		while len(self.hand) >0:
			self.discard.append(self.hand.pop())
			
			
				
				
			
		

class Card():
	def __init__(self, cost):
		self.cost = cost
		
	def getVictoryPoints(self):
		pass
	
	def performAction(self,hand,deck,trash):
		pass
	
	def getCost(self):
		return self.cost
		
	def isActionable(self):
		return false;


class VictoryCard(Card):
	def getVictoryPoints(self):
		return self.points
	
class Estate(VictoryCard):
	def __init__(self):
		VictoryCard.__init__(self,2)
		self.name = "Estate"
		self.points = 1
		
class Duchy(VictoryCard):
	def __init__(self):
		VictoryCard.__init__(self,5)
		self.name = "Duchy"
		self.points = 1
		
class Province(VictoryCard):
	def __init__(self):
		VictoryCard.__init__(self,8)
		self.name = "Province"
		self.points = 1

class Treasure(Card):
	def getWorth(self):
		return self.worth

class Gold(Treasure):
	def __init__(self):
		Treasure.__init__(self,6)
		self.name = "Gold"
		self.worth = 3
		
class Silver(Treasure):
	def __init__(self):
		Treasure.__init__(self,3)
		self.name = "Silver"
		self.worth = 2

class Copper(Treasure):
	def __init__(self):
		Treasure.__init__(self,0)
		self.name = "Copper"
		self.worth = 1

main()