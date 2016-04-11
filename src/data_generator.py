#-*- encoding: utf-8 -*-
"""
DAREMOS COMO FRAUDULENTAS COMPRAS QUE SE HAYAN REALIZADO A DISTINTO PAIS, EN
HORA NOCTURNA.

Id transaccion, usuario/numero tarjeta, tipologia de consumo , notengoniputaidea ,cantidad,fecha de transaccion


Transaccion:
    ID Comercio
    Pais Comercio
    TPV
    importe
    Numero Pedido
    Nº tarjeta
    Datetime


Tarjetas
    Nombre
    Apellidos
    Numero
    Pais

Comercio
    TPV
    Pais Comercio
    Cuenta de cargo



1 titular - 1 tarjeta
1 comercio - 1 tpv con un nº de cuenta asociado.

Intentos erroneos en TPV

pais del cliente
numero de tarjeta
importe



ID  USUARIO NUMERO TARJETA
"""
import random
import pycountry as pycountry
from django_iban.generator import IBANGenerator
from constants import countries
from faker import Factory, Faker


class DataGenerator():

    def __init__(self):
        self.locale_by_country_cache = self.__build_locale_by_country_dict()
        # No es viable cambiar el Locale del faker, hay que volver a crearlo.
        # Para evitar esto tenemos un pool de fakers ya creados, uno por locale.
        self.faker_by_country_cache = self.__build_faker_by_country_dict()
        self.iban_generator = IBANGenerator()
        self.commerce_list = []
        self.client_list = []
        self.transaction_list = []

##=============================================================================
## CLIENT
##=============================================================================
    def generate_client_list(self, quantity):
        self.client_list = []
        for i in range(quantity):
            person = self.get_random_client(i)
            self.client_list.append(person)

    def get_random_client(self, id, country_object=None):
        if country_object is None:
            country_object = self.get_random_country_object()
        random_iban = self.get_random_iban_for_country(country_object)
        # self.faker = \
        #     Factory.create(self.__get_locale_for_country_object(country_object))

        faker = self.__get_faker_for_country_object(country_object)
        data = {
            'credit_card':faker.credit_card_number(card_type=None),
            'account_iban':random_iban["generated_iban"],
            '_id':id,
            "country":country_object.alpha2,
            "contry_name":country_object.name,
            "birth_day":faker.date_time_between(start_date="-30y", end_date="-18y"),
            #La address a veces tiene \n
            "address":faker.street_address().replace("\n",""),
            "name": faker.first_name(),
            "last_name": faker.last_name()
        }

        return data

##=============================================================================
## COMMERCE
##=============================================================================
    def generate_random_commerce_list(self, quantity):
        self.commerce_list = []
        for index in range(quantity):
            commerce = self.get_random_commerce(id=index)
            self.commerce_list.append(commerce)

    def get_random_commerce(self, id, country_object = None):
        if country_object is None:
            country_object = self.get_random_country_object()
        random_iban = self.get_random_iban_for_country(country_object)
        # self.faker = \
        #     Factory.create(self.__get_locale_for_country_object(country_object))
        faker = self.__get_faker_for_country_object(country_object)
        return {
            "tpv":random_iban["account"],
            "account_iban":random_iban["generated_iban"],
            "country":country_object.alpha2,
            "contry_name":country_object.name,
            "_id":id,
            "url": faker.url(),
            "email":faker.company_email()
        }

##=============================================================================
## TRANSACTIONS
##=============================================================================
    def generate_random_transaction_list(self, quantity):
        self.transaction_list = []
        for index in range(quantity):
            transaction = self.get_random_transaction(id=index)
            self.transaction_list.append(transaction)

    def get_random_transaction(self, id):
        client = self.normal_distribution_choice(self.client_list)
        commerce = self.normal_distribution_choice(self.commerce_list)
        ammount = self.get_normal_distribution_ammount(20,1500, 200, 80)
        faker = self.__get_faker_for_country_object()

        when = faker.date_time_between(start_date="-1y")
        when = when.replace(hour=self.get_normal_distribution_hour_of_day())
        data = {
            "_id":id,
            "commerce_tpv":commerce["tpv"],
            "commerce_account_iban":commerce["account_iban"],
            "commerce_country":commerce["country"],
            "commerce_contry_name":commerce["contry_name"],
            "commerce_id":commerce["_id"],
            "client_id":client["_id"],
            "client_name":client["name"],
            "client_last_name":client["last_name"],
            "client_credit_card":client["credit_card"],
            "client_country":client["country"],
            "client_country_name":client["contry_name"],
            "transaction_ammount": ammount,
            "transaction_datetime":when,
        }
        return data

##=============================================================================
## ATOMIC FIELDS+
##=============================================================================
    def get_random_country_object(self):
        """
        >>> germany.alpha2
        >>> germany.alpha3
        >>> germany.numeric
        >>> germany.name
        >>> germany.official_name
        """
        country_code = self.normal_distribution_choice(countries)[1]
        return pycountry.countries.get(alpha2=country_code)

    def get_random_iban_for_country(self, country_object):
        return self.iban_generator.generate(country_code=country_object.alpha2)

    def __build_locale_by_country_dict(self):
        data = {}
        for item in countries:
            data[item[1]]=item[2]
        return data

    def __get_locale_for_country_object(self, country_object):
        return self.locale_by_country_cache.get(country_object.alpha2)

    def __build_faker_by_country_dict(self):
        data = {}
        for item in countries:
            data[item[1]]=Factory.create(item[2])
        return data

    def __get_faker_for_country_object(self, country_object=None):
        if country_object is None:
            key = self.faker_by_country_cache.keys()[0]
            return self.faker_by_country_cache.get(key)
        return self.faker_by_country_cache.get(country_object.alpha2)

    def normal_distribution_choice(self, list, mean=None, stddev=None):
        """
        Devuelve un elemento aleatorio de la lista, pero siguiendo una
        distribución normal gausiana.

        http://stackoverflow.com/questions/35472461/select-one-element-from-a-list-using-python-following-the-normal-distribution
        :param list:
        :return:
        """
        if mean is None:
            # if mean is not specified, use center of list
            mean = (len(list) - 1) / 2

        if stddev is None:
            # if stddev is not specified, let list be -3 .. +3 standard deviations
            stddev = len(list) / 6

        while True:
            index = int(random.normalvariate(mean, stddev) + 0.5)
            if 0 <= index < len(list):
                return list[index]

    def get_normal_distribution_ammount(self, min, max, mean=None, stddev=None):
        if mean is None:
            # if mean is not specified, use center of list
            mean = int ((max-min)/2)

        if stddev is None:
            # if stddev is not specified, let list be -3 .. +3 standard deviations
            stddev = max / min

        while True:
            ammount = random.normalvariate(mean, stddev)

            if min <= ammount < max:
                return round(ammount,2)

    def get_normal_distribution_hour_of_day(self):
        mean = 14
        stddev = 4

        while True:
            hour = random.normalvariate(mean, stddev)

            if 0 <= hour < 24:
                return int(hour)



if __name__ == "__main__":
    gen = DataGenerator()

    hours = [0] *24
    for i in range (10000):
        hour=gen.get_normal_distribution_hour_of_day()
        hours[hour]+=1

    print hours





