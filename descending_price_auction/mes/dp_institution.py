from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random
import logging
import time
import datetime


@directive_enabled_class
class DPInstitution(Institution):
    def __init__(self):
        self.auctions = 10
        self.agents = None

        self.min_item_value = 10
        self.max_item_value = 100

        self.last_bid = 0
        self.last_bid_time = 0

        self.starting_price = None
        self.bids = []

    @directive_decorator("init_institution")
    def init_institution(self, message:Message):
        if self.debug:
            print("Institution: received institution init ...")

    @directive_decorator("start_experiment")
    def start_experiment(self, message:Message):
        # send instructions and prompt lender for rate_of_return_offer
        if self.debug:
            print("INSTITUTION: Start Experiment")

    @directive_decorator("descend_price")
    def descend_price(self, message:Message):
        # send instructions and prompt lender for rate_of_return_offer
        bid_alert_time = message.get_payload()["bid_action_time"]
        
        self.starting_price = self.starting_price - 1
        self.log_message("Descending the price. New price is " + str(self.starting_price))
        self.alert_agents_of_price(self.starting_price)
            

        
    def alert_agents_of_price(self, current_price):
        for agent in self.agents:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("current_price")
                new_message.set_payload({"current_price": current_price})
                self.send(agent, new_message)  # receiver_of_message, message
        
        unixtime2 = time.time()
        self.last_bid_time = unixtime2
        wakeup_message = Message()  # declare message
        wakeup_message.set_sender(self.myAddress)  # set the sender of message to this actor
        wakeup_message.set_directive("descend_price")
        wakeup_message.set_payload({"bid_action_time": unixtime2})
        self.wakeupAfter( datetime.timedelta(seconds=10), payload=None)



    @directive_decorator("start_auction", message_schema=["agents"], message_callback="send_agents_start")
    def start_auction(self, message:Message):
        print("STARTING AN AUCTION")
        if self.auctions > 0:
            self.auctions -= 1
            print("INSTITUTION: Starting Auction")
            self.agents = message.get_payload()["agents"]
            self.bids = []
            self.starting_price = self.max_item_value
            self.alert_agents_of_price(self.starting_price)
            

    @directive_decorator("bid_for_item", message_schema=["bid"])
    def bid_for_item(self, message: Message):
        bidder = message.get_sender()
        bid = int(message.get_payload()["bid"])
        self.log_message("Received bid: " + str(bid) + " - current previous bid " + str(self.last_bid))    
            
        
