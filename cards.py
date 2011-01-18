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
		
# Try to keep the action cards organized alphabetically

class Bureaucrat(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Bureaucrat"
	def performAction(self,p,g):
		if(len(g.silvers) > 0):
			p.deck.insert(0,g.silvers.pop())
		else:
			print "Wasted the action because no more silvers are available."

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
		
class Chancellor(Action):
	def __init__(self):
		Action.__init__(self,3)
		self.name = "Chancellor"
	
	def performAction(self,p,g):
		p.cash += 2
		print "Do you want to immediately put your deck into your discard pile?"
		line = g.getCleanLine()
		if line == "y" or line == "yes":
			p.discard.extend(p.deck)
			p.deck = []
			
class Chapel(Action):
	def __init__(self):
		Action.__init__(self,2)
		self.name = "Chapel"
		
	def performAction(self,p,g):
		print "What cards do you want to trash (up to 4)?"
		discards = g.chooseCards(p.hand)
		
		count = 0
		for c in discards:
			count += 1
			if count > 4:
				break
			
			p.hand.remove(c)
		p.showHand()
		
		
			
class CouncilRoom(Action):
	def __init__(self):
		Action.__init__(self,5)
		self.name = "Council Room"
	def performAction(self,p,g):
		p.drawCards(g,4)
		p.buys += 1
		for player in g.players:
			if p != player:
				player.drawCards(g,1)

class Feast(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Feast"
	def performAction(self,p,g):
		p.drawCards(g,1)
		p.actions += 1
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
		
class Militia(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Militia"
	def performAction(self,p,g):
		p.cash += 2
	
class Moat(Action):
	def __init__(self):
		Action.__init__(self,2)
		self.name = "Moat"
	def performAction(self,p,g):
		p.drawCards(g,2)
		p.showHand()
		
class Moneylender(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Moneylender"
	def performAction(self,p,g):
		for c in p.hand:
			if isinstance(c,Copper):
				p.hand.remove(c)
				p.cash += 3
				p.showHand()
				break
			
			

class Remodel(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Remodel"
	def performAction(self,p,g):
		print "What card do you want to remodel?",
		victim = g.chooseCard(p.hand)
		if victim:
			p.hand.remove(victim)
			g.trash.append(victim)
			
			print "Allow purchase of card worth %s." % (victim.cost + 2)
			
		else:
			print "Error: victim for remodel not chosen"
		
class Smithy(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Smithy"
		
	def performAction(self, p, g):
		p.drawCards(g,3)
		p.showHand()
		
class Spy(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Spy"
	def performAction(self,p,g):
		p.drawCards(g,1)
		p.actions += 1
		p.showHand()
		
class Thief(Action):
	def __init__(self):
		Action.__init__(self,4)
		self.name = "Thief"
	def performAction(self,p,g):
		p.showHand()
		
class Village(Action):
	def __init__(self):
		Action.__init__(self,3)
		self.name = "Village"
	def performAction(self,p,g):
		p.actions+= 2
		p.drawCards(g,1)
		p.showHand()
		
class Woodcutter(Action):
	def __init__(self):
		Action.__init__(self,3)
		self.name = "Woodcutter"
	def performAction(self,p,g):
		p.buys += 1
		p.cash += 2
		
class Workshop(Action):
	def __init__(self):
		Action.__init__(self,3)
		self.name = "Workshop"
	def performAction(self,p,g):
		p.drawCards(g,1)
		p.actions += 1
		p.showHand()
		