#!/usr/bin/env python3
''' pymongo module '''
import pymongo


def list_all(mongo_collection) -> list:
    ''' lists all documents in a collection '''
    docs = mongo_collection.find()
    return docs

