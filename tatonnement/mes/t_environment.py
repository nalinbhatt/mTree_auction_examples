from mTree.microeconomic_system.environment import Environment
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.components.property_types import MTreeBoolProperty, MTreeIntProperty, MTreeRealProperty, MTreeSetProperty
from mTree.microeconomic_system.property_decorators import *
import logging
import random

@directive_enabled_class#(expected_properties=["agent_endoment", "num_auctions"])
class TEnvironment(Environment):
    @directive_decorator("outlog")
    def outlog(self, message:Message):
        pass


    @directive_decorator("start_environment")
    def start_environment(self, message:Message):
        self.set_buyer_values()
        self.set_seller_values()
        
    
    @directive_decorator("buyer_checkin")
    def buyer_checkin(self, message:Message):
        self.buyer_checkin -= 1
        self.check_auction_start()
        

    @directive_decorator("seller_checkin")
    def seller_checkin(self, message:Message):
        self.seller_checkin -= 1
        self.check_auction_start()
        
    
    def check_auction_start(self):
        self.log_message("Another agent checked in! - " + str(self.buyer_checkin) + " - " + str(self.seller_checkin))
        if self.buyer_checkin == 0 and self.seller_checkin == 0:
            self.start_auction()

    def start_auction(self):
        self.log_message("Auction Starts!")
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("start_auction")
        new_message.set_payload({"buyers": self.buyers_addresses, "sellers": self.sellers_addresses})
        self.send(self.institutions[0], new_message)  # receiver_of_message, message

    def set_buyer_values(self):
        self.buyer_checkin = 0
        self.buyers_addresses = []
        for agent in self.agents:
            if agent[1] == "t_buyer.TBuyer":
                self.buyer_checkin += 1
                self.buyers_addresses.append(agent[0])
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("set_value")  # Set the directive (refer to 3. Make Messages) - has to match reciever decorator
                value = random.randint(20, 40)
                new_message.set_payload({"value": value})
                self.send(agent[0], new_message )  # receiver_of_message, message

    def set_seller_values(self):
        self.seller_checkin = 0
        self.sellers_addresses = []
        for agent in self.agents:
            if agent[1] == "t_seller.TSeller":
                self.seller_checkin += 1
                self.sellers_addresses.append(agent[0])
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("set_value")  # Set the directive (refer to 3. Make Messages) - has to match reciever decorator
                value = random.randint(20, 40)
                new_message.set_payload({"value": value})
                self.send(agent[0], new_message )  # receiver_of_message, message
