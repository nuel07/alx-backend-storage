#!/usr/bin/env python3
''' pymongo module '''
import pymongo


def insert_school(mongo_collection, **kwargs):
    ''' inserts a new document in a collection '''
    new_doc = mongo_collection.insert_one(kwargs)
    return new_doc.inserted_id
