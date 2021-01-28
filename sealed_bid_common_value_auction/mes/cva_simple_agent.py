from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
from mTree.microeconomic_system.agent import Agent
import logging
import random

EXPERIMENT = 25


@directive_enabled_class
class CVASimpleAgent(Agent):
    def __init__(self):
        self.endowment = None
        self.institution = None
        self.item_for_bidding = None

    @directive_decorator("init_agent")
    def init_agent(self, message: Message):
        pass

    @directive_decorator("auction_result")
    def auction_result(self, message: Message):
        #status = message.get_payload()["status"]
        logging.log(EXPERIMENT, "Agent received item for bid %s", message.get_payload())


    @directive_decorator("set_endowment")
    def set_endowment(self, message: Message):
        self.endowment = message.get_payload()["endowment"]

    @directive_decorator("item_for_bidding", message_schema=["value"], message_callback=self.make_bid)
    def item_for_bidding(self, message: Message):
        self.item_for_bidding = message.get_payload()["value"]
        self.institution = message.get_sender()
        logging.log(EXPERIMENT, "Agent received item for bid %s", str(self.item_for_bidding))
        

    def make_bid(self):
        new_message = Message()  # declare message
        new_message.set_sender(self)  # set the sender of message to this actor
        new_message.set_directive("bid_for_item")
        new_message.set_payload({"bid": self.item_for_bidding})
        self.send(self.institution.myAddress, new_message)  # receiver_of_message, message
