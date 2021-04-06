from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random


@directive_enabled_class
class APSimpleAgent(Agent):
    def __init__(self):
        self.endowment = None
        self.institution = None
        self.item_for_bidding = None

        self.last_bid = 0

        self.max_bid = random.randint(5, 150)
        self.bid_increment = random.randint(1, 10)


    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("auction_result")
    def auction_result(self, message: Message):
        #status = message.get_payload()["status"]
        self.log_data("Agent received item for bid " + str(message.get_payload()))
        logging.log(EXPERIMENT, "Agent received item for bid %s", message.get_payload())


    @directive_decorator("set_endowment")
    def set_endowment(self, message: Message):
        self.endowment = message.get_payload()["endowment"]

    @directive_decorator("current_price", message_schema=["value"], message_callback="make_bid")
    def bid_at_price(self, message: Message):
        self.current_price = message.get_payload()["current_price"]
        self.institution = message.get_sender()
        self.log_data("Agent received item for bid " + str(self.current_price))
        if self.current_price < self.max_bid:
            self.make_bid()
        

    def make_bid(self):
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("bid_for_item")
        self.last_bid = self.current_price + self.bid_increment
        new_message.set_payload({"bid": self.last_bid})
        self.send(self.institution, new_message)  # receiver_of_message, message
        self.log_message("Agent submitted bid: " + str(self.last_bid))