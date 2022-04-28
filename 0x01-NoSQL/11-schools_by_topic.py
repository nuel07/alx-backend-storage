#!/usr/bin/env python3
''' pymongo module '''


def schools_by_topic(mongo_collection, topic):
    ''' returns list of schools having specific topic '''
    return mongo_collection.find({"topics": topic})
