from bson import ObjectId

from cis498.mongodb.mongoclient import MongoClientHelper


class Cart:

	def __init__(self):
		self.mc = MongoClientHelper()
		self.cart_db = self.mc.db['cart']

	def createCartItem(self, user, item):
		listItems = []
		listItems.append(item)
		order = {
			"email": user.lower(),
			"item": listItems
		}
		self.cart_db.insert_one(order)

	def addToCart(self, email, item):
		customer_query = {"email": email.lower()}
		order = self.cart_db.find_one(customer_query)
		order['item'].append(item)
		self.cart_db.update_one(customer_query, {"$set": {"item": order['item']}})


	def doesOrderExist(self, email):
		orderExist = self.cart_db.find_one({"email": email.lower()})
		return orderExist

	def deleteCart(self, email):
		self.cart_db.delete_one({"email": email.lower()})

	def deleteItemFromCart(self, email, id):
		cart = self.doesOrderExist(email)
		if cart:
			for item in cart['item']:
				if id == str(ObjectId(item['item_id'])):
					cart['item'].remove(item)
					break

		self.cart_db.update_one({"email": email.lower()}, {"$set": {"item": cart['item']}})


	def cartItems(self, email):
		orders = self.doesOrderExist(email)
		if orders is not None:
			return orders['item']
		return None

	def getCartOrder(self, email):
		order = self.doesOrderExist(email)
		cartOrder = CartOrder(order['_id'], order['email'], order['item'])
		return cartOrder

class CartOrder:

	def __init__(self, id, email, items):
			self.id = id,
			self.email = email
			self.items = items

