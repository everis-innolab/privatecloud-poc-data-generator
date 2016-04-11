from constants import *
from data_generator import DataGenerator
import pymongo as pymongo


class MongoDataLoader():

    def __init__(self):
        self.mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.mongo_client[MONGO_DB]
        self.commerces_col = self.db[MONGO_COMMERCE_COLLECTION]
        self.clients_col = self.db[MONGO_CLIENT_COLLECTION]
        self.transactions_col = self.db[MONGO_TRANSACTION_COLLECTION]
        self.gen = DataGenerator()

    def go(self, clients, commerces, transactions):
            self.__generate_and_save_clients(clients)
            self.__generate_and_save_commerces(commerces)
            self.__generate_and_save_transactions(transactions)

    def __generate_and_save_transactions(self, transactions):
        print "Generating Transactions"
        self.gen.generate_random_transaction_list(transactions)
        print "Saving Transactions"
        for transaction in self.gen.transaction_list:
            self.transactions_col.insert(transaction)

    def __generate_and_save_clients(self, quantity):
        print "Generating Clients"
        self.gen.generate_client_list(quantity)

        print "Saving Clients"
        for client in self.gen.client_list:
            self.clients_col.insert(client)

    def __generate_and_save_commerces(self, commerces):
        print "Generating Commerces"
        self.gen.generate_random_commerce_list(commerces)
        print "Saving Commerces"
        for commerce in self.gen.commerce_list:
            self.commerces_col.insert(commerce)

if __name__ == "__main__":
    loader = MongoDataLoader()
    loader.go(NUMBER_OF_CLIENTS, NUMBER_OF_COMMERCES, NUMBER_OF_TRANSACTIONS)