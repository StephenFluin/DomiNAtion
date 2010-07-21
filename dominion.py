#!/usr/bin/python


import sys,random
from color import echo


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
			
			
			#Buy Phase
			while p.buys > 0:
				p.updateCash()
				print "Cash on hand: %s" % (p.cash)
				print "Enter the name of a card you wish to buy:",
				line = getCardName()
				if line != "":
					card = match(line,g.supplies)
					if card and p.cash >= card.cost:
						g.removeSupplyCard(card)
						p.discard.append(card)
						p.cash -= card.cost
					elif p.cash < card.cost:
						print "Insufficient funds for that card."
						p.buys += 1
						
				p.buys -= 1
			
			p.endTurn()
			
def getCardName():
	line = sys.stdin.readline()
	line = line.strip('\n\r')
	return line
				

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
			
		stack = [[] for row in range(6)]
		# 10 cards for each supply, don't take bottom one
		for i in range(11):
			stack[0].append(Smithy())
			stack[1].append(Market())
			stack[2].append(Laboratory())
			stack[3].append(Village())
			stack[4].append(Festival())
			stack[5].append(Cellar())
			
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
		line = getCardName()
		if line != "":
			card = match(line,stack)
			if card and test(card):
				return card
		return None
		
		


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
		

class Card():
	def __init__(self, cost):
		self.cost = cost
		
	def getVictoryPoints(self):
		pass
	
	def performAction(self,actor,game):
		pass
	
	def getCost(self):
		return self.cost
		
	def isActionable(self):
		return False;


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

class Action(Card):
	def isActionable(self):
		return True

class Smithy(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Smithy"
		
	def performAction(self, p, g):
		p.drawCards(g,3)
		p.showHand()
		
class Laboratory(Action):
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Laboratory"
	def performAction(self,p,g):
		p.actions+= 1
		p.drawCards(g,2)
		p.showHand()
		
class Market(Action):
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Market"
	def performAction(self,p,g):
		p.actions+= 1
		p.buys += 1
		p.cash +=1
		p.drawCards(g,1)
		p.showHand()
		
class Village(Action):
	def __init__(self):
		Action.__init__(self,3)
		self.name = "Village"
	def performAction(self,p,g):
		p.actions+= 2
		p.drawCards(g,1)
		p.showHand()
		
class Festival(Action):
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Festival"
	def performAction(self,p,g):
		p.actions+= 2
		p.buys += 1
		p.cash +=2
		p.showHand()
class Cellar(Action):
	def __init__(self):
		Action.__init__(self,2)
		self.name = "Cellar"
	
	def performAction(self,p,g):
		p.actions += 1
		print "What cards do you want to discard?"
		discards = g.chooseCards(p.hand)
		
		for c in discards:
			p.discard.append(c)
			p.hand.remove(c)
		p.drawCards(g,len(discards))
		p.showHand()
main()
