#!/usr/bin/python


import sys,random
from color import echo
from cards import *

def main():
	g = Game()
	g.addPlayer("stephen")
	
	runConsoleGame(g)
	
	

def match(cardName, stack):
	if isinstance(stack[0], Card):
		
		for c in stack:
			if c.name.lower() == cardName.lower():
				return c
	else:
		for s in stack:
			ret = match(cardName, s)
			if ret:
				return ret
	
	return None

def runConsoleGame(game):
	g = game
	gameOver = False
	while not gameOver:
		#Give each player a turn
		for p in g.players:
			p.draw(g)
			p.showHand()
			p.debugDeck()
			p.showDiscard()
			
			print "Supplies:",
			for c in g.supplies:
				print "%s (Cost: %s, Left:%s)" % (c[0].name, c[0].cost, len(c)),
			print
			p.actions = 1
			p.buys = 1
			p.cash = 0
			
			#Action Phase
			while p.actions > 0:
				print "Enter the name of an action card or type skip:",
				card = g.chooseCard(p.hand, lambda x: x and x.isActionable())
				if card and card.isActionable():
					p.hand.remove(card)
					p.discard.append(card)
					card.performAction(p, g)
					
				elif card:
					p.actions += 1
				else: 
					p.actions = 0
				p.actions -= 1
			
			
			p.updateCash()
			
			#Buy Phase
			while p.buys > 0:
				
				
				print "Cash on hand: %s" % (p.cash)
				print "Enter the name of a card you wish to buy:",
				line = g.getCleanLine()
				if line != "":
					card = match(line,g.supplies)
					if card and p.cash >= card.cost and not g.isLastCard(card):
						g.removeSupplyCard(card)
						p.discard.append(card)
						p.cash -= card.cost
					elif p.cash < card.cost:
						print "Insufficient funds for that card."
						p.buys += 1
				else:
					p.buys = 0
				p.buys -= 1
			
			p.endTurn()
			

				

class Game():
	def __init__(self):
		self.trash = []
		self.players = []
		
		estates = []
		duchies = []
		provinces = []
		golds = []
		silvers = []
		coppers = []
		
		self.supplies = []
		
		for i in range(12):
			estates.append(Estate())
			duchies.append(Duchy())
			provinces.append(Province())
			
		for i in range(50):
			golds.append(Gold())
			silvers.append(Silver())
			coppers.append(Copper())
			
		stack = [[] for row in range(9)]
		# 10 cards for each supply, don't take bottom one
		for i in range(11):
			stack[0].append(Smithy())
			stack[1].append(Market())
			stack[2].append(Laboratory())
			stack[3].append(Village())
			stack[4].append(Festival())
			stack[5].append(Cellar())
			stack[6].append(Chancellor())
			stack[7].append(CouncilRoom())
			stack[8].append(Remodel())
			
		self.supplies.extend([provinces, duchies, estates, golds, silvers, coppers])
		self.supplies.extend(stack)
	
	# Add a player to the game
	def addPlayer(self,name):
		self.players.append(Player(self,name))
		
	#def tidyCard(self,card):
	#	print "tidyCard is putting away a %s" % (card)
	#	for stack in self.supplies:
	#		if stack[0].name == card.name:
	#			stack.append(card)
	#			return
	
	# Remove a card from the appropriate pile
	def removeSupplyCard(self,card):
		for stack in self.supplies:
			if stack[0].name == card.name:
				stack.remove(card)
				return
	
	# Present a list of cards to the user and let them pick one
	def chooseCards(self,stack):
		ret = []
		while True:
			card = self.chooseCard(stack)
			
			if not card:
				break
			else:
				ret.append(card)
				stack.remove(card)
		for c in ret:
			stack.append(c)
		return ret
			
			
		
	def chooseCard(self,stack, test = lambda x: True):
		print "\nOptions:",
		printCardList(stack, test)
		line = self.getCleanLine()
		if line != "":
			card = match(line,stack)
			if card and test(card):
				return card
		return None
		
	def isLastCard(self,card):
		for stack in self.supplies:
			if stack[0].name == card.name:
				return len(stack) <= 1
		return None
	
	def getCleanLine(self):
		line = sys.stdin.readline()
		line = line.strip('\n\r')
		return line
		


class Player():
	def __init__(self, game,name):
		self.name = name
		self.hand = []
		self.deck = []
		self.discard = []
		self.cash = 0
		for i in range(7):
			self.deck.append(game.supplies[5].pop())
		for i in range(3):
			self.deck.append(game.supplies[2].pop())
		random.shuffle(self.deck)
			
	def draw(self,game):
		self.drawCards(game,5)
		
	def drawCards(self,game,count):
		for i in range(count):
			if len(self.deck) <= 0:
				while len(self.discard) > 0:
					self.deck.append(self.discard.pop())
				random.shuffle(self.deck)
			if len(self.deck) > 0:
				self.hand.append(self.deck.pop())
	def endTurn(self):
		while len(self.hand) >0:
			self.discard.append(self.hand.pop())
			
	def updateCash(self):
		i = len(self.hand) - 1
		while i >= 0:
			c = self.hand[i]
			if isinstance(c,Treasure):
				self.cash += c.getWorth()
				self.hand.remove(c)
				self.discard.append(c)
				
			i -= 1
	
	def showHand(self):
		print "Hand:",
		printCardList(self.hand)
		
	def debugDeck(self):
		print "Deck:",
		printCardList(self.deck)
		
	def showDiscard(self):
		print "Discard:",
		printCardList(self.discard)

				
def printCardList(list, test = lambda x: True):
	for c in list:
		if isinstance(c,VictoryCard):
			echo('green')
		if isinstance(c,Treasure):
			echo('yellow')
		if isinstance(c,Action):
			echo('white')
		if test(c):
			print "%s " % (c.name),
		echo('none')
	print		
		


main()
