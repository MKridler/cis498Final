from cis498.mongodb.customers import Customers
from cis498.mongodb.drivers import Drivers
from cis498.mongodb.mongoclient import MongoClientHelper
from bson.objectid import ObjectId
from decimal import Decimal
import datetime


deliveryDict = {
    "1": "Pickup - No Delivery",
    "2": "Delivery - In House",
    "3": "Delivery - 3rd Party"
}

tipDict = {
    "1": "15%",
    "2": "18%",
    "3": "20%",
    "4": "Custom Amount",
    "5": "None"
}

class Orders:
    ORDER_STATUS = 'orderStatus'
    ORDER_TYPE = 'orderType'
    RECEIVED = 'Received'
    IN_PROGRESS = 'In Progress'
    ORDER_READY = 'Order Ready'
    IN_TRANSIT = 'In Transit'
    READY_FOR_PICKUP = 'Ready For Pickup'
    ORDER_COMPLETE = 'Order Complete'

    def __init__(self):
        self.mc = MongoClientHelper()
        self.orders_db = self.mc.db['orders']

    # This will generate an order document and also update the customer record
    def generateOrder(self, customer, order, form):
        datetime_time = datetime.datetime.now()
        # Determine Delivery Method
        orderType = form['delivery_method'].data
        drivers = Drivers()
        if orderType == '1':
            driver = None
        elif orderType == '2':
            driver = drivers.find_staff_driver()
        else:
            driver = drivers.find_contract_driver()
        order = {
            'email': customer.email,
            'items': order,
            'comments': form['comments'].data,
            'orderStatus': 'Received',
            'orderType': deliveryDict.get(orderType),
            'dateTime': datetime_time,
            'driver': driver,
            'tip_amount': form.data['tipamount']
        }
        generatedOrder = self.orders_db.insert_one(order)
        self.updateCustomerRecord(customer.email, generatedOrder.inserted_id)
        if driver is not None:
            self.driver_on_delivery(driver)

    # Updates the customer record
    def updateCustomerRecord(self, email, orderId):
        customer = Customers()
        customer.updateCustomerOrders(email, orderId)

    # Updates the driver record
    def driver_on_delivery(self, email):
        driver = Drivers()
        driver.update_driver_on_delivery(email)


    # Functional Requirement 5
    def getCurrentOrders(self):
        orderCollection = self.orders_db.find({'orderStatus': {"$ne": self.ORDER_COMPLETE}})
        # orderCollection = self.orders_db.find({"$and":[{"orderStatus":{"$ne": self.ORDER_COMPLETE}},
        #                                                {"orderStatus":{"$ne": self.IN_TRANSIT}}]})
        orderList = []
        for order in orderCollection:
            Dict = dict({
                'email': order['email'],
                'id': order['_id'],
                'comments': order['comments'],
                'items': order['items'],
                'status': order['orderStatus'],
                'driver': order['driver']
            })
            orderList.append(Dict)
        return orderList

        # Functional Requirement 5
    def getCurrentUserOrder(self, email, customer):
        #First get the customer order history
        final_result = None
        customerOrders = customer.orders
        if customerOrders is not None:
            for order in customerOrders:
                status = self.orders_db.find_one({'_id': ObjectId(order)})
                if status['orderStatus'] != 'Order Complete':
                    final_result = status

        if final_result == None:
            order_list = {
                'email': '',
                'id': '',
                'comments': '',
                'items': '',
                'status': 'No Pending Orders'}
        else:

            order_list ={
                    'email': final_result['email'],
                    'id': final_result['_id'],
                    'comments': final_result['comments'],
                    'items': final_result['items'],
                    'status': final_result['orderStatus'],
                    'type': final_result['orderType']
                }

        return order_list


    def get_driver_orders(self, user):
        orderCollection = self.orders_db.find({'orderStatus': self.IN_TRANSIT})
        orderList = []
        for order in orderCollection:
            if order['driver'] == user:
                Dict = dict({
                    'email': order['email'],
                    'id': order['_id'],
                    'comments': order['comments'],
                    'items': ', '.join(order['items']),
                    'status': order['orderStatus']
                })
                orderList.append(Dict)
        return orderList

    def get_driver_order_history(self, email):
        orderCollection = self.orders_db.find()
        driverOrders = []
        for orders in orderCollection:
            if orders['driver'] == email:
                order = Order(orders['email'], orders['items'], orders['comments'], orders['orderType'], orders['dateTime'],
                               orders['driver'], orders['_id'], orders['tip_amount'])
                driverOrders.append(order)
        if not driverOrders:
            return None
        else:
            driverDict = {}
            for driverOrder in driverOrders:
                dictKey = driverOrder.datetime.strftime("%m/%d/%Y")
                if dictKey not in driverDict:
                    driverDict[dictKey] = [1, driverOrder.tips, dictKey]
                else:
                    dictList = driverDict[dictKey]
                    orderTotal = dictList[0] + 1
                    origVal = float(dictList[1])
                    driverTips = float(driverOrder.tips)
                    newVal = Decimal(origVal + driverTips)
                    driverDict[dictKey] = [orderTotal, round(newVal,2), dictKey]
            return driverDict


    def updateOrder(self, order):
        oidQuery = {"_id": ObjectId(order)}
        orderToUpdate = self.orders_db.find_one(oidQuery)
        currentOrderStatus = orderToUpdate[self.ORDER_STATUS]
        if orderToUpdate[self.ORDER_STATUS] == self.RECEIVED:
            orderToUpdate[self.ORDER_STATUS] = self.IN_PROGRESS
        elif orderToUpdate[self.ORDER_STATUS] == self.IN_PROGRESS:
            orderToUpdate[self.ORDER_STATUS] = self.ORDER_READY
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and 'Pickup' not in orderToUpdate[self.ORDER_TYPE]:
            orderToUpdate[self.ORDER_STATUS] = self.IN_TRANSIT
        elif orderToUpdate[self.ORDER_STATUS] == self.ORDER_READY and 'Pickup' in orderToUpdate[self.ORDER_TYPE]:
            orderToUpdate[self.ORDER_STATUS] = self.READY_FOR_PICKUP
        elif orderToUpdate[self.ORDER_STATUS] == self.IN_TRANSIT or orderToUpdate[self.ORDER_STATUS] == self.READY_FOR_PICKUP:
            orderToUpdate[self.ORDER_STATUS] = self.ORDER_COMPLETE

        if(currentOrderStatus == self.IN_TRANSIT and orderToUpdate[self.ORDER_STATUS] == self.ORDER_COMPLETE):
            driver = Drivers()
            driver.update_driver_off_delivery(orderToUpdate['driver'])

        self.orders_db.update_one(oidQuery, {"$set": {self.ORDER_STATUS: orderToUpdate[self.ORDER_STATUS]}})

    def generate_customer_order_report(self):
        orderCollection = self.orders_db.find()
        orders = []
        for order in orderCollection:
            orders.append(order['email'] + " " + order['dateTime'].strftime("%m/%d/%Y, %H:%M:%S") + " Order " + ",".join(order['items']))
        return (orders)

    def generate_driver_report(self):
        orderCollection = self.orders_db.find()
        orders = []
        for order in orderCollection:
            if order['driver'] is None:
                continue
            orders.append(order['driver'] + " " + order['dateTime'].strftime("%m/%d/%Y, %H:%M:%S"))
        return (orders)

    def find_order_by_id(self, oid):
        oidQuery = {"_id": ObjectId(oid)}
        orders = self.orders_db.find_one(oidQuery)
        if orders is not None:
            order = Order(orders['email'], orders['items'], orders['comments'], orders['orderType'], orders['dateTime'],
                               orders['driver'], orders['_id'], orders['tip_amount'])
            return order
        return None

    def get_customer_order_history(self, email):
        customers = Customers()
        customer = customers.findCustomerByEmail(email)
        if customer is None:
            return None
        order_history = []
        if customer.orders is not None:
            for order in customer.orders:
               order_history.append(self.find_order_by_id(ObjectId(order)))
            order_items = []
            for order in order_history:
                order_items.append(order.items)
            return order_items
        return None


class Order:

    def __init__(self, email, items, comments, ordertype, datetime, driver, id, tips):
        self.email = email
        self.items = items
        self.comments = comments
        self.ordertype = ordertype
        self.datetime = datetime
        self.driver = driver
        self.id = id
        self.tips = tips



