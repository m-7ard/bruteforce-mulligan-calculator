from random import shuffle

class Deck():

	def __init__(self, deck_size, successes_in_deck, traps_in_deck, mulligans=0, replacement=False):
		self.deck_size = deck_size
		self.successes_in_deck = successes_in_deck
		self.traps_in_deck = traps_in_deck
		self.mulligans = mulligans
		self.replacement = replacement
		self.deck_contents = self.generate_deck(deck_size, successes_in_deck, traps_in_deck, mulligans)
	
	def generate_deck(self, deck_size, successes_in_deck, traps_in_deck, mulligans=0):
		failures_in_deck = deck_size - (successes_in_deck + mulligans + traps_in_deck)
		deck =  ["F" for f in range(failures_in_deck)]  + \
				["S" for s in range(successes_in_deck)] + \
				["T" for s in range(traps_in_deck)]	    + \
				["M" for r in range(mulligans)]
		return deck

	def switch_cards(self, source, finish, hand_size):
		while hand_size:
			finish.append(source.pop())
			hand_size -= 1
	
	def mean(self, hand_size, decklist=None, cards_in_hand=[]):
		if decklist == None:
			decklist = self.deck_contents
		deck = decklist[:]
		shuffle(deck)
		self.switch_cards(deck, cards_in_hand, hand_size) # Deal cards

		if "S" in cards_in_hand and cards_in_hand.count("T") >= 1:
			res = 1
			self.switch_cards(cards_in_hand, deck, hand_size)
			return res 
		elif "S" not in cards_in_hand and "M" in cards_in_hand or self.mulligans and self.replacement:
			try: cards_in_hand.remove("M")
			except: self.mulligans -= 1
			self.switch_cards(cards_in_hand, deck, hand_size - 1)
			return self.mean(hand_size - 1, deck)
		else:
			self.switch_cards(cards_in_hand, deck, hand_size)
			return 0

Deskbot = Deck(26, 6, 8, 3)
print(sum(Deskbot.mean(4) for i in range(100000)) / 100000)
