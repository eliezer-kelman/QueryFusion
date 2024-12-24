from app.db.database import get_collection


def execute_mongo_query(query_id: int, filters: dict = None):
    if query_id == 1:
        return get_attack_types_severity(filters.get('top_5'))
    if query_id == 2:
        return average_casualties_by_region(filters.get('top_5'))
    if query_id ==3:
        return top_5_terror_groups()
    if query_id == 4:
        return top_5_groups_per_region()
    if query_id == 5:
        return yearly_change_by_region()


def yearly_change_by_region():

    collection = get_collection('terrorism')

    pipeline = [
        {
            "$project": {
                "region": "$location.region",
                "year": {"$year": {"$dateFromString": {"dateString": "$date"}}}
            }
        },
        {
            "$group": {
                "_id": {"region": "$region", "year": "$year"},
                "event_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id.region": 1,
                "_id.year": 1
            }
        },
        {
            "$group": {
                "_id": "$_id.region",
                "yearly_data": {
                    "$push": {
                        "year": "$_id.year",
                        "event_count": "$event_count"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "region": "$_id",
                "yearly_change": {
                    "$map": {
                        "input": {"$range": [1, {"$size": "$yearly_data"}]},
                        "as": "index",
                        "in": {
                            "year": {
                                "$arrayElemAt": ["$yearly_data.year", "$$index"]
                            },
                            "change_percentage": {
                                "$multiply": [
                                    {
                                        "$divide": [
                                            {
                                                "$subtract": [
                                                    {"$arrayElemAt": ["$yearly_data.event_count", "$$index"]},
                                                    {"$arrayElemAt": ["$yearly_data.event_count", {"$subtract": ["$$index", 1]}]}
                                                ]
                                            },
                                            {"$arrayElemAt": ["$yearly_data.event_count", {"$subtract": ["$$index", 1]}]}
                                        ]
                                    },
                                    100
                                ]
                            }
                        }
                    }
                }
            }
        }
    ]

    return list(collection.aggregate(pipeline))


def get_attack_types_severity(top_only: bool = False):

    collection = get_collection('terrorism')

    pipeline = [
        {
            "$project": {
                "attack_type": "$attack.type",
                "severity": {
                    "$sum": [
                        {"$multiply": [{"$ifNull": ["$casualties.killed", 0]}, 2]},
                        {"$ifNull": ["$casualties.wounded", 0]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$attack_type",
                "total_severity": {"$sum": "$severity"}
            }
        },
        {"$sort": {"total_severity": -1}}
    ]

    if top_only:
        pipeline.append({"$limit": 5})

    return list(collection.aggregate(pipeline))


def average_casualties_by_region(top_only: bool = False):

    collection = get_collection('terrorism')

    pipeline = [
        {
            "$project": {
                "region": "$location.region",
                "severity": {
                    "$sum": [
                        {"$multiply": [{"$ifNull": ["$casualties.killed", 0]}, 2]},
                        {"$ifNull": ["$casualties.wounded", 0]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$region",
                "total_severity": {"$sum": "$severity"},
                "event_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "region": "$_id",
                "_id": 0,
                "average_casualties": {"$divide": ["$total_severity", "$event_count"]}
            }
        },
        {"$sort": {"average_casualties": -1}}
    ]

    if top_only:
        pipeline.append({"$limit": 5})

    return list(collection.aggregate(pipeline))


def top_5_terror_groups():

    collection = get_collection('terrorism')

    pipeline = [
        {
            "$project": {
                "primary_group": "$attackers.primary_group",
                "civilian_casualties": {
                    "$sum": [
                        {"$ifNull": ["$casualties.killed", 0]},
                        {"$ifNull": ["$casualties.wounded", 0]}
                    ]
                }
            }
        },
        {
            "$group": {
                "_id": "$primary_group",
                "total_casualties": {"$sum": "$civilian_casualties"}
            }
        },
        {"$sort": {"total_casualties": -1}},
        {"$limit": 5}
    ]

    return list(collection.aggregate(pipeline))


def top_5_groups_per_region():

    collection = get_collection('terrorism')

    pipeline = [
        {
            "$project": {
                "region": "$location.region",
                "primary_group": "$attackers.primary_group"
            }
        },
        {
            "$group": {
                "_id": {"region": "$region", "primary_group": "$primary_group"},
                "event_count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "_id.region": 1,
                "event_count": -1
            }
        },
        {
            "$group": {
                "_id": "$_id.region",
                "top_groups": {
                    "$push": {
                        "group": "$_id.primary_group",
                        "event_count": "$event_count"
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "region": "$_id",
                "top_groups": {"$slice": ["$top_groups", 5]}
            }
        }
    ]

    return list(collection.aggregate(pipeline))
