#-----NEW------
#Create a DB with SQLite:
#run 'python3'
#type 'from app import db' in python shell
#type 'db.create_all()'
#type 'exit()'

import os
from . import default
from flask import redirect, jsonify, request
import eventlet
eventlet.monkey_patch()
from websocket import create_connection
import json
from app.models.models import OrderBook
from app import socketio, db
from flask_socketio import SocketIO, emit
from threading import Thread, Event, Timer
import time

#thread setup
thread = Thread()
thread_stop_event = Event()

print("Server running on localhost:5000")

#SQLALCHEMY THINGS
# OrderBook.query.delete()
# db.session.commit()

#print(len(OrderBook.query.all()))
#print(OrderBook.query.filter_by(exchange='Bitfinex').all())

# new_transaction = OrderBook('bid', 5, 10, 'Gdax', 'BTC')
# db.session.add(new_transaction)
# db.session.commit()

#Bitfinex connection
wsfinex = create_connection("wss://api.bitfinex.com/ws")
#Gdax connection
wsgdax = create_connection('wss://ws-feed.gdax.com')

#Thread that will collect websocket data from bitfinex and gdax in the background
class WebsocketAPI(Thread):
	def __init__(self):
		#self.delay = 1
		super(WebsocketAPI, self).__init__()
		self._stop_event = Event()

	def orderBookData(self):

		#Delete all rows in the DB so I can put a fresh snapshot into it
		OrderBook.query.delete()
		db.session.commit()

		#Send a subscribe message to start recieving websocket data
		wsfinex.send(json.dumps({
		    "event": "subscribe",
		    "channel": "book",
		    "pair": "BTCUSD",
		    "prec": "P0"
		}))
		wsgdax.send(json.dumps({
			"type": "subscribe",
			"product_ids": ["BTC-USD"],
			"channels": ["level2"]
		}))

		#1st message recieved from bitfinex api
		resultFinex = wsfinex.recv()
		# print(resultFinex)

		#2nd message recieved from bitfinex api
		resultFinex = wsfinex.recv()
		# print(resultFinex)

		#snapshot from Bitfinex
		snapshotFinex = wsfinex.recv()
		snapshotFinex = json.loads(snapshotFinex)
		# print(snapshotFinex[1][0])
		exchange = 'Bitfinex'
		pairname = 'BTC-USD'
		#print(priceFinex, countFinex, amountFinex, sideFinex)

		for i in range(0, len(snapshotFinex[1])):
			if(snapshotFinex[1][i][1] != 0):
				priceFinex = snapshotFinex[1][i][0]
				countFinex = snapshotFinex[1][i][1]
				amountFinex = snapshotFinex[1][i][2]
				if(amountFinex > 0):
					sideFinex = 'buy'
				else:
					sideFinex = 'sell'
				new_transaction = OrderBook(sideFinex, priceFinex, countFinex, exchange, pairname)
				db.session.add(new_transaction)
				db.session.commit()



		#snapshot from Gdax
		snapshotGdax = wsgdax.recv()
		snapshotGdax = json.loads(snapshotGdax)
		exchange = 'Gdax'
		# print(snapshotGdax['bids'][0])
		for i in range(0, 25):
			if(snapshotGdax['bids'][i][1] != 0):
				sideGdax = 'buy'
				priceGdax = snapshotGdax['bids'][i][0]
				countGdax = snapshotGdax['bids'][i][1]
				new_transaction = OrderBook(sideGdax, priceGdax, countGdax, exchange, pairname)
				db.session.add(new_transaction)
				db.session.commit()

		for i in range(0, 25):
			if(snapshotGdax['asks'][i][1] != 0):
				sideGdax = 'sell'
				priceGdax = snapshotGdax['asks'][i][0]
				countGdax = snapshotGdax['asks'][i][1]
				new_transaction = OrderBook(sideGdax, priceGdax, countGdax, exchange, pairname)
				db.session.add(new_transaction)
				db.session.commit()

		#updates from both Gdax and Bitfinex
		while True:
			resultGdax = wsgdax.recv()
			resultGdax = json.loads(resultGdax)

			#if the 'time' is equal to None, 'changes' will not show up in the json object returned by Gdax
			if(resultGdax.get('time') != None):
				# print(resultGdax['changes'][0])
				if(resultGdax['changes'][0][0] == 'buy'):
					socketio.emit('my response', {"price": resultGdax['changes'][0][1], "buy": resultGdax['changes'][0][2]})
				else:
					socketio.emit('my response', {"price": resultGdax['changes'][0][1], "sell": resultGdax['changes'][0][2]})

			#RECIEVE UPDATES FROM BITFINEX
			resultFinex = wsfinex.recv()
			resultFinex = json.loads(resultFinex)
			# print (resultFinex)
			
			#when there is no new message for 1 second a 'hb' is sent
			#if we see an 'hb' just skip it
			if(resultFinex[1] != 'hb'):
				if(resultFinex[3] > 0):
					socketio.emit('my response', {"price": resultFinex[1], "count": resultFinex[2], "buy": resultFinex[3]})
				else:
					socketio.emit('my response', {"price": resultFinex[1], "count": resultFinex[2], "sell": abs(resultFinex[3])})
			#This is needed to make socketio emite messages while in this loop
			socketio.sleep(0)
			

		#close connections
		wsgdax.close()
		wsfinex.close()

	def run(self):
		self.orderBookData()

@default.route('/')
def home():
	#need this variable to be global
	global thread

	#if the thread is not running, start the thread.
	if not thread.isAlive():
		print("Starting Thread")
		thread = WebsocketAPI()
		thread.start()
	return redirect('/noble-markets-realtime-order-book')

@default.route('/noble-markets-realtime-order-book')
def realtimeOrderbook():
	#TEST for SECKETIO
	# @socketio.on('ready')
	# def test_function():
	# 	i = 0
	# 	while i < 10:
	# 		print(i)
	# 		socketio.emit('my response', {"data": i})
	# 		socketio.sleep(1)
	# 		i +=1

	#need this variable to be global
	global thread

	#if the thread is not running, start the thread.
	if not thread.isAlive():
		print("Starting Thread")
		thread = WebsocketAPI()
		thread.start()

	return default.send_static_file('index.html')


@default.route('/noble-markets-order-book-snapshot')
def orderbookSnapshot():

	return default.send_static_file('index.html')


#REST API: Get all data from DB that returns the whole order book snapshot
@default.route('/snapshot', methods=['GET'])
def getSnapshotData():

	#query = OrderBook.query.filter_by(exchange='Gdax').all()
	
	#Query made to the OrderBook DB
	query = OrderBook.query.all()
	snapshotData = []

	#go through each row returned in the query
	for row in query:
		#turn each row into a dict
		castDict = row.__dict__
		#remove unnecessary data from dict
		castDict.pop('_sa_instance_state', None)
		#append Dict to a list
		snapshotData.append(castDict)

	#turn list into a json object
	snapshotData = {'snapshot_data': snapshotData }

	return jsonify(snapshotData)

#REST API: Get all data from DB that has a price greater than a certain value
@default.route('/snapshotGreaterThan/<GTprice>', methods=['GET'])
def getSnapshotPriceGreaterThan(GTprice):

	#query = OrderBook.query.filter_by(exchange='Gdax').all()
	
	#Query made to the OrderBook DB
	query = OrderBook.query.filter(OrderBook.price > GTprice)
	snapshotData = []

	#go through each row returned in the query
	for row in query:
		#turn each row into a dict
		castDict = row.__dict__
		#remove unnecessary data from dict
		castDict.pop('_sa_instance_state', None)
		#append Dict to a list
		snapshotData.append(castDict)

	#turn list into a json object
	snapshotData = {'snapshot_data': snapshotData }

	return jsonify(snapshotData)

#REST API: Get all data from DB that matches the exchange
@default.route('/snapshotByExchange/<findExchange>', methods=['GET'])
def getSnapshotByExchange(findExchange):
	#query = OrderBook.query.filter_by(exchange='Gdax').all()
	
	#Query made to the OrderBook DB
	query = OrderBook.query.filter_by(exchange = findExchange)
	snapshotData = []

	#go through each row returned in the query
	for row in query:
		#turn each row into a dict
		castDict = row.__dict__
		#remove unnecessary data from dict
		castDict.pop('_sa_instance_state', None)
		#append Dict to a list
		snapshotData.append(castDict)

	#turn list into a json object
	snapshotData = {'snapshot_data': snapshotData }

	return jsonify(snapshotData)

#REST API get all data from DB that matches exchange and Greater than a certain price
@default.route('/snapshotByExchangeAndPrice/<findExchange>/<GTprice>', methods=['GET'])
def getSnapshotByExchangeAndGTprice(findExchange,GTprice):
	#query = OrderBook.query.filter_by(exchange='Gdax').all()
	
	#Query made to the OrderBook DB
	query = OrderBook.query.filter(OrderBook.exchange == findExchange, OrderBook.price > GTprice)
	snapshotData = []

	#go through each row returned in the query
	for row in query:
		#turn each row into a dict
		castDict = row.__dict__
		#remove unnecessary data from dict
		castDict.pop('_sa_instance_state', None)
		#append Dict to a list
		snapshotData.append(castDict)

	#turn list into a json object
	snapshotData = {'snapshot_data': snapshotData }

	return jsonify(snapshotData)
