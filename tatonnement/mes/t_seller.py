from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random

EXPERIMENT = 25


@directive_enabled_class
class TSeller(Agent):
    def __init__(self):
        self.value = None
        self.institution = None
        self.item_for_bidding = None

    @directive_decorator("set_value")
    def set_value(self, message: Message):
        self.value = message.get_payload()["value"]
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("seller_checkin")
        self.send(message.get_sender(), new_message)


    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("sell_result")
    def sell_result(self, message: Message):
        sell_price = message.get_payload()["price"]
        logging.log(EXPERIMENT, "Agent sold item at %s", str(sell_price))

    @directive_decorator("sell_price_message") #, message_schema=["value"], message_callback="make_bid")
    def sell_price_message(self, message: Message):
        self.current_sell_price = message.get_payload()["sell_price"]
        self.institution = message.get_sender()
        logging.log(EXPERIMENT, "Agent received item for bid %s", str(self.item_for_bidding))
        self.log_experiment_data("Agent received item for bid " + str(self.item_for_bidding))
        self.determine_sale()
        

    def determine_sale(self):
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("sell_price_response")
        
        if self.current_sell_price >= self.value:
            new_message.set_payload({"determination": "sell"})
        else:
            new_message.set_payload({"determination": "hold"})
        self.send(self.institution, new_message)  # receiver_of_message, message
