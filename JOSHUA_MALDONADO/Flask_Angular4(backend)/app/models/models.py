from app import db

class OrderBook(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	bid_ask = db.Column(db.Text)
	price = db.Column(db.Integer)
	count = db.Column(db.Integer)
	exchange = db.Column(db.Text)
	pairname = db.Column(db.Text)

	def __init__(self, bid_ask, price, count, exchange, pairname):
		self.bid_ask = bid_ask
		self.price = price
		self.count = count
		self.exchange = exchange
		self.pairname = pairname

# new_transaction = OrderBook('ask', 5, 10, 'Gdax', 'BTC')
# db.session.add(new_transaction)
# db.session.commit()

