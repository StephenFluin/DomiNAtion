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