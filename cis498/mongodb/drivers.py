from bson import ObjectId

from cis498.mongodb.mongoclient import MongoClientHelper


class Drivers:

    def __init__(self):
        self.mc = MongoClientHelper()
        self.db = self.mc.db['drivers']

    # Define Actions of a driver

    def is_driver(self, email):
        driver = self.db.find_one({"email": email})
        if driver is None:
            return False
        return True

    def find_contract_driver(self):
        drivers = self.db.find()
        contractor_list = []
        for driver in drivers:
            if driver['type'] == "contractor":
                contractor_list.append(driver)
        for contractor in contractor_list:
            if contractor['on_delivery'] is False:
                return contractor['email']
        return None

    def find_staff_driver(self):
        drivers = self.db.find()
        staff_list = []
        for driver in drivers:
            if driver['type'] == "staff":
                staff_list.append(driver)
        for staff in staff_list:
            if staff['on_delivery'] is False:
                return driver['email']
        return None

    # This method will update customer the customer order list for maintaining order history
    def update_driver_on_delivery(self, email):
        driver_query = {"email": email.lower()}
        driver = self.db.find_one(driver_query)
        self.db.update_one(driver_query, {"$set": {"on_delivery": True}})

    def update_driver_off_delivery(self, email):
        driver_query = {"email": email.lower()}
        driver = self.db.find_one(driver_query)
        self.db.update_one(driver_query, {"$set": {"on_delivery": False}})
