from constants import *
from src.data_generator import DataGenerator
import csv
import unicodecsv

class CSVGenerator():

    def __init__(self):
        self.gen = DataGenerator()

    def go(self, clients, commerces, transactions):
            self.__generate_and_save_clients(clients)
            self.__generate_and_save_commerces(commerces)
            self.__generate_and_save_transactions(transactions)

    def __generate_and_save_transactions(self, transactions):
        print "Generating Transactions"
        self.gen.generate_random_transaction_list(transactions)

        print "Saving Transactions"
        headers = self.__get_transaction_header_order()
        rows = []
        for transaction in self.gen.transaction_list:
            rows.append(self.__document_to_row(transaction, headers))

        self.__clean_and_fill_csv(TRANSACTION_CSV, headers, rows)

    def __generate_and_save_clients(self, quantity):
        print "Generating Clients"
        self.gen.generate_client_list(quantity)

        print "Saving Clients"
        headers = self.__get_client_header_order()
        rows = []
        for client in self.gen.client_list:
            rows.append(self.__document_to_row(client, headers))
        self.__clean_and_fill_csv(CLIENTS_CSV, headers, rows)

    def __generate_and_save_commerces(self, commerces):
        print "Generating Commerces"
        self.gen.generate_random_commerce_list(commerces)

        print "Saving Commerces"
        headers = self.__get_commerce_header_order()
        rows = []
        for commerce in self.gen.commerce_list:
            rows.append(self.__document_to_row(commerce, headers))

        self.__clean_and_fill_csv(COMMERCE_CSV, headers, rows)

    def __clean_and_fill_csv(self, file_path, headers, data_list):
        myfile = open(file_path, 'wb')
        wr = unicodecsv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headers)

        myfile = open(file_path, 'ab')
        wr = unicodecsv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerows(data_list)

##=============================================================================
## DOCUMENT TO ROW CONVERSION
##=============================================================================
    def __document_to_row(self, document, header_order_list):
        row = []
        for index, header in enumerate(header_order_list):
            row.append(document[header])
        return row

    def __get_client_header_order(self):
         return [
            "_id",
            "credit_card",
            "account_iban",
            "country",
            "contry_name",
            "birth_day",
            "address",
            "name",
            "last_name"
         ]

    def __get_commerce_header_order(self):
        return [
             "tpv",
            "account_iban",
            "country",
            "contry_name",
            "_id",
            "url",
            "email"
         ]

    def __get_transaction_header_order(self):
        return [
            "_id",
            "client_country",
            "client_id",
            "commerce_tpv",
            "client_credit_card",
            "transaction_ammount",
            "commerce_id",
            "client_country_name",
            "commerce_country",
            "commerce_contry_name",
            "commerce_account_iban",
            "transaction_datetime",
            "client_name",
            "client_last_name"
        ]

if __name__ == "__main__":
    loader = CSVGenerator()
    loader.go(NUMBER_OF_CLIENTS, NUMBER_OF_COMMERCES, NUMBER_OF_TRANSACTIONS)