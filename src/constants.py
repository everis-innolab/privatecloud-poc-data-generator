#-*- encoding: utf-8 -*-

MONGO_HOST = "192.168.56.102"
MONGO_PORT = 27017
MONGO_DB = "microservices_data"
MONGO_CLIENT_COLLECTION = "clients"
MONGO_TRANSACTION_COLLECTION = "transactions"
MONGO_COMMERCE_COLLECTION = "commerces"

COMMERCE_CSV="commerces.csv"
CLIENTS_CSV="clients.csv"
TRANSACTION_CSV="transactions.csv"

NUMBER_OF_CLIENTS = 5000
NUMBER_OF_COMMERCES = 1000
NUMBER_OF_TRANSACTIONS = 10000

south_america_and_spain = [
    ("Argentina","AR"),
    ("Bolivia","BO"),
    ("Brasil","BR"),
    ("Chile","CL"),
    ("Colombia","CO"),
    ("Ecuador","EC"),
    ("Paraguay","PY"),
    ("Peru","PE"),
    ("Surinam","SR"),
    ("Uruguay","UY"),
    ("Venezuela","VE"),
    ("España","ES")
]

"""
El orden de la lista es bastante importante, ya que se utiliza para generar
una distribucion normal. Los paises mas comunes serán los centrales y los
menos frecuentes los de los extremos.
"""
countries = [
    ("Bulgaria ","BG", "bg_BG"),
    ("Czech Republic ","CZ","cs_CZ"),
    ("Denmark ","DK","dk_DK"),
    ("Finland ","FI","fi_FI"),
    ("Greece ","GR","el_GR"),
    ("Ireland ","IE","en_GB"),
    ("France ","FR","fr_FR"),
    ("Germany ","DE","de_DE"),
    ("Spain ","ES","es_ES"),
    ("Portugal ","PT","pt_PT"),
    ("Italy ","IT","it_IT"),
    ("United Kingdom ","GB","en_GB"),
    ("Netherlands ","NL","nl_NL"),
    ("Norway ","NO","no_NO"),
    ("Sweden ","SE","sv_SE"),
    ("Poland ","PL","pl_PL"),
    # ("Russia ","RU","ru_RU"), No tiene IBAN
    ("Slovakia ","SK","sk_SK"),
    ("Slovenia ","SI","sl_SI"),
    ("Lithuania ","LT","lt_LT")
]