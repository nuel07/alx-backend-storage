#!/usr/bin/env python3
''' pymongo module '''


def update_topics(mongo_collection, name, topics):
    ''' changes all topics of a school based on a name '''
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
