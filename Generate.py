"""
@author Robert Powell

Simple script to randomly generate a bunch of FOL assertions in TPTP format
given a CSV of seed data
"""

import argparse
import itertools
import re
import random

# Nice little autoincrementing utility for ids
COUNT = itertools.count()

def parse_csv(filepath):
    '''
    Loads a csv file at a given path and returns the data broken into the
    global groups.

    :param string filepath, path to a csv file
    :return dict, dictionary of different types
    '''

    farms = []
    institutions = []
    products = []
    certs = []

    lines = []
    with open(filepath, 'r') as f:
        for line in f:

            print line

            farm, insti, cert, product, typ = line.split(',')

            farms += [farm.strip()]
            institutions += [insti.strip()]
            certs += [cert.strip()]
            products += [(product.strip(), typ.strip())]

    return {'farms':farms, 'institutions':institutions, 'products':products}

def create_type_assertion(predicate, thing):
    '''
    Create a TPTP string that equivalent to the assertion Predicate(THING)
    
    :param string predicate, name of unary predicate to instantiate
    :param string thing, name of constant symbol to be asserted upon
    :return string assertion, TPTP formatted assertion
    '''

    assertion = "fof({},axiom,( {}({}) ) )."
    return assertion.format(next(COUNT), predicate, thing)

def create_subclass_assertion(child, parent):
    '''
    Create a TPTP string that equivalent to the assertion child(x) => parent(x)
    
    :param string child, name of child class
    :param string parent, name of parent class
    :return string assertion, TPTP formatted assertion
    '''

    assertion = "fof({}, axiom, ( ! [X] : ( {}(X) => {}(X))) )."
    return assertion.format(next(COUNT), child, parent)

def create_property_assertion(prop, x, y):
    '''
    Create a TPTP string that equivalent to the assertion Property(thing, it)
    
    :param string prop, name of relation
    :param string x, name of domain class
    :param string y, name of range class
    :return string assertion, TPTP formatted assertion
    '''

    assertion = "fof({},axiom,( {}({}, {}) ) )."
    return assertion.format(next(COUNT), prop, x, y)



if __name__ == '__main__':

    # Getting really hackish here because I want to go to bed now
    products = []
    farms = []
    instit = []

    stuff = parse_csv("Farm_Data.csv")

    for farm in stuff['farms']:
        farm = re.sub(r'\'', '', farm)
        farm = re.sub(r'\W+', '_', farm)
        print create_type_assertion('farm', '"{}"'.format(farm.lower()))
        farms.append('"{}"'.format(farm.lower()))

    for insti in stuff['institutions']:

        if insti != '':
            insti = re.sub(r'\'', '', insti)
            insti = re.sub(r'\W+', '_', insti)
            print create_type_assertion('institution', '"{}"'.format(insti.lower()))
            instit.append('"{}"'.format(insti.lower()))

    for product, typ in stuff['products']:

        if product != '':
            product = re.sub(r'\'', '', product)
            product = re.sub(r'\W+', '_', product)
            print create_subclass_assertion(product.lower(), typ.lower())
            products.append(product.lower())

    for farm in farms:

        for i in range(1, 20):
            product = products[random.randint(0, len(products) - 1)]
            product_instance = product + str(next(COUNT))

            print create_type_assertion(product, '"{}"'.format(product_instance))
            print create_property_assertion('sells', farm, '"{}"'.format(product_instance))

    for ints in instit:

        for i in range(1, 10):
            product = products[random.randint(0, len(products) - 1)]
            print create_property_assertion('buys', ints, product)






    

