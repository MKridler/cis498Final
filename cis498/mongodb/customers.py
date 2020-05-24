from cis498.mongodb.mongoclient import MongoClientHelper


class Customers:

    # Established mongo connection and customers collection
    def __init__(self):
        self.mc = MongoClientHelper()
        self.customers_db = self.mc.db['customers']

    def createCustomer(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email').lower()
        address = form.cleaned_data.get('address')
        phone_number = form.cleaned_data.get('phone_number')
        customer = {"name": name,
                    "email": email,
                    "address": address,
                    "phone_number": phone_number}

        self.customers_db.insert_one(customer)

    # def generateCustomerReport(dateRange)

    # def getCustomerHistory()

    # This method will update customer the customer order list for maintaining order history
    def updateCustomerOrders(self, email, uuid):
        customer_query = {"email": email.lower()}
        customer = self.customers_db.find_one(customer_query)

        # Use some try/catch logic to check for existing orders, if it breaks its the customers first order
        try:
            customer['orders'].append(uuid)
            self.customers_db.update_one(customer_query, {"$set": {"orders": customer['orders']}})
        except KeyError:
            uuidList = [uuid]
            self.customers_db.update_one(customer_query, {"$set": {"orders": uuidList}})


    def findCustomerByEmail(self, email):
        customer_query = {"email": email.lower()}
        result = self.customers_db.find_one(customer_query)
        return Customer(result['name'], result['email'], result['address'], result['phone_number'], result['orders'])

    def findCustomerInfoByEmail(self, email):
        customer_query = {"email": email.lower()}
        result = self.customers_db.find_one(customer_query)
        return Customer(result['name'], result['email'], result['address'], result['phone_number'], None)


class Customer:

    def __init__(self, name, email, address, phone_number, orders):
        self.name = name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.orders = orders
