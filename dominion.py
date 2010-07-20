#!/usr/bin/python


import sys,random

def main():
	print "Creating cards"
	g = Game()
	g.addPlayer("stephen")
	
	runConsoleGame(g)
	
	

def match(cardName, stack):
	if isinstance(stack[0], Card):
		
		for c in stack:
			if c.name.lower() == cardName.lower():
				stack.remove(c)
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
				print "%s (%s)" % (c[0].name, len(c)),
			print
			p.actions = 1
			p.buys = 1
			
			
			#Action Phase
			while p.actions > 0:
				print "Enter the name of an action card or type skip:"
				line = getCardName()
				if line != "":
					card = match(line,p.hand)
					print "You entered '%s'." % (line)
					if card and card.isActionable():
						card.performAction(p, g)
					else:
						p.actions += 1
				p.actions -= 1
			
			
			#Buy Phase
			while p.buys > 0:
				print "Enter the name of a card you wish to buy:"
				line = getCardName()
				card = match(line,g.supplies)
				if card:
					p.discard.append(card)
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
			
		stack = range(10)
		for i in range(10):
			stack.append(Smithy())
		self.supplies.extend([provinces, duchies, estates, golds, silvers, coppers])
		self.supplies.extend(stack)
	
	def addPlayer(self,name):
		self.players.append(Player(self,name))


class Player():
	def __init__(self, game,name):
		self.name = name
		self.hand = []
		self.deck = []
		self.discard = []
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
	
	def showHand(self):
		print "Hand:",
		for c in self.hand:
			print "%s" % (c.name),
		print
		
	def debugDeck(self):
		print "Deck:",
		for c in self.deck:
			print "%s" % (c.name),
		print
		
	def showDiscard(self):
		print "Discard:",
		for c in self.discard:
			print "%s" % (c.name),
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
class Laboratory(Action)
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Laboratory"
	def performAction(self,p,g):
		p.actions+= 1
		p.drawCards(g,2)
		p.showHand()
		
class Market(Action)
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Market"
	def performAction(self,p,g):
		p.actions+= 1
		p.buys += 1
		p.cash +=1
		p.drawCards(g,1)
		p.showHand()
		
		
main()
