from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random


@directive_enabled_class
class TBuyer(Agent):
    def __init__(self):
        self.value = None
        self.institution = None
        self.item_for_bidding = None

    @directive_decorator("set_value")
    def set_value(self, message: Message):
        self.value = message.get_payload()["value"]
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("buyer_checkin")
        self.log_message("Buyer checking in!")
        self.send(message.get_sender(), new_message)

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("buy_result")
    def buy_result(self, message: Message):
        buy_price = message.get_payload()["price"]
        self.log_message("Agent bought item at " + str(buy_price))


    
    @directive_decorator("buy_price_message") #, message_schema=["value"], message_callback="make_bid")
    def buy_price_message(self, message: Message):
        self.current_buy_price = message.get_payload()["buy_price"]
        self.institution = message.get_sender()
        self.log_message("Agent received item for bid " + str(self.current_buy_price))
        self.log_data("Agent received item for bid " + str(self.current_buy_price))
        self.determine_buy()
        

    def determine_buy(self):
        new_message = Message()  # declare message
        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
        new_message.set_directive("buy_price_response")
        self.log_message("Agent determining buy: " + str(self.value) + " -- " + str(self.current_buy_price))
        
        if self.current_buy_price <= self.value:
            new_message.set_payload({"determination": "buy"})
        else:
            new_message.set_payload({"determination": "hold"})
        self.send(self.institution, new_message)  # receiver_of_message, message
