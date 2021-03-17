from mTree.microeconomic_system.institution import Institution
from mTree.microeconomic_system.directive_decorators import *
from mTree.microeconomic_system.message import Message
import math
import random
import logging


@directive_enabled_class
class TInstitution(Institution):
    def __init__(self):
        self.auctions = 20

        self.buyers = None
        self.sellers = None

        self.price_low = 28
        self.price_high = 36
        self.buy_responses = []
        self.sell_responses = []

        self.iterations = 10

    @directive_decorator("init_institution")
    def init_institution(self, message:Message):
        if self.debug:
            print("Institution: received institution init ...")

    @directive_decorator("start_experiment")
    def start_experiment(self, message:Message):
        # send instructions and prompt lender for rate_of_return_offer
        if self.debug:
            print("INSTITUTION: Start Experiment")

    @directive_decorator("start_auction", message_schema=["agents"], message_callback="send_agents_start")
    def start_auction(self, message:Message):
        self.log_message("Institution starting the auction")
        self.iterations = 10
        self.price_history = []
        self.price_low = 25
        self.price_high = 36
        self.price_buy = self.price_low
        self.price_sell = self.price_high
        self.t = 0
        self.price_t = None
        self.buyers = message.get_payload()["buyers"]
        self.sellers = message.get_payload()["sellers"]
        self.auction_step()

    def auction_step(self):
        if self.iterations > 0:
            print("!*" * 25)
            print("!*" * 25)
            print("!*" * 25)
            print("!*" * 25)
            print("!*" * 25)
            self.log_message("NEXT AUCTION STEP")
            self.iterations -= 1
            self.price_t = (self.price_buy + self.price_sell)/2
            self.buy_responses = []
            self.sell_responses = []
            print("INSTITUTION: Starting Auction")
            self.log_message("PRICE SET TO: " +  str(self.price_t))
            for buyer in self.buyers:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("buy_price_message")
                new_message.set_payload({"buy_price": self.price_t})
                self.send(buyer, new_message)  # receiver_of_message, message
            for seller in self.sellers:
                new_message = Message()  # declare message
                new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                new_message.set_directive("sell_price_message")
                new_message.set_payload({"sell_price": self.price_t})
                self.send(seller, new_message)  # receiver_of_message, message
    

    @directive_decorator("buy_price_response")
    def buy_price_response(self, message:Message):
        bidder = message.get_sender()
        determinaton = message.get_payload()["determination"]
        if determinaton == "buy":
            self.buy_responses.append((1, bidder))
        else:
            self.buy_responses.append((0, bidder))

        self.check_step_end()

    @directive_decorator("sell_price_response")
    def sell_price_response(self, message:Message):
        bidder = message.get_sender()
        determinaton = message.get_payload()["determination"]
        if determinaton == "sell":
            self.sell_responses.append((1, bidder))
        else:
            self.sell_responses.append((0, bidder))
        
        self.check_step_end()


    def check_step_end(self):
        logging.log(EXPERIMENT, "Buyers in %s", str(len(self.buy_responses)))
        logging.log(EXPERIMENT, "Sellers in %s", str(len(self.sell_responses)))
        self.log_message("Buyers in " + str(len(self.buy_responses)) + " -- " + str(len(self.buyers)))
        print("Sellers in ", str(len(self.sell_responses)), " -- ", len(self.sellers))
        if len(self.buyers) == len(self.buy_responses) and len(self.sellers) == len(self.sell_responses):
            print("ALL PRICES IN")
            logging.log(EXPERIMENT, "ALL PRICES IN")
            self.log_message("ALL PRICES ARE NOW IN AND THE AUCTION CLOSES")
            buy_totals = [val[0] for val in self.buy_responses]
            sell_totals = [val[0] for val in self.sell_responses]
            x_t = sum(buy_totals)
            y_t = sum(sell_totals)
            print("TOTAL BUYERS: ", x_t)
            print("TOTAL SELLERS: ", y_t)
            if x_t == y_t:
                self.p_star = self.price_t
                for i in self.buy_responses:
                    if i[0] == 1:
                        new_message = Message()  # declare message
                        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                        new_message.set_directive("buy_result")
                        new_message.set_payload({"status": "bought", "price": self.p_star})
                        self.send(i[1], new_message) 
                for i in self.sell_responses:
                    if i[0] == 1:
                        new_message = Message()  # declare message
                        new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                        new_message.set_directive("sell_result")
                        new_message.set_payload({"status": "sold", "price": self.p_star})
                        self.send(i[1], new_message) 
            elif self.iterations == 0 and x_t > 0 and y_t > 0:
                self.p_star = self.price_t
                print("Total buyers: ", x_t, " -- total sellers: ", y_t)
                if x_t < y_t:
                    for i in self.buy_responses:
                        if i[0] == 1:
                            new_message = Message()  # declare message
                            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                            new_message.set_directive("buy_result")
                            new_message.set_payload({"status": "bought", "price": self.p_star})
                            self.send(i[1], new_message) 
                elif x_t > y_t:
                    print("BUYERS -> ", self.buy_responses)
                    shuffled_buyers = [buyer for buyer in self.buy_responses if buyer[0] == 1]
                    random.shuffle(shuffled_buyers)
                    for i in shuffled_buyers[0:y_t]:
                        if i[0] == 1:
                            new_message = Message()  # declare message
                            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                            new_message.set_directive("buy_result")
                            new_message.set_payload({"status": "bought", "price": self.p_star})
                            self.send(i[1], new_message) 
                elif y_t < x_t:
                    for i in self.sell_responses:
                        if i[0] == 1:
                            new_message = Message()  # declare message
                            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                            new_message.set_directive("sell_result")
                            new_message.set_payload({"status": "sold", "price": self.p_star})
                            self.send(i[1], new_message) 
                elif y_t > x_t:
                    shuffled_sellers = [seller for seller in self.sell_responses if seller[0] == 1]
                    random.shuffle(shuffled_sellers)
                    for i in shuffled_sellers[0:y_t]:
                        if i[0] == 1:
                            new_message = Message()  # declare message
                            new_message.set_sender(self.myAddress)  # set the sender of message to this actor
                            new_message.set_directive("sell_result")
                            new_message.set_payload({"status": "sold", "price": self.p_star})
                            self.send(i[1], new_message) 
            else:
                print("!#" * 25)
                print("!#" * 25)
                print("!#" * 25)
                print("!#" * 25)
                print("NO MARKET MOVEMENT... ", self.price_t, " -- ", self.price_buy, " -- ", self.price_sell)
                
                if x_t >= y_t:
                    self.price_buy = self.price_t
                elif x_t < y_t:
                    self.price_sell = self.price_t
                print("!!!!!NO MARKET MOVEMENT... ", self.price_t, " -- ", self.price_buy, " -- ", self.price_sell)
                
                self.auction_step()


            
