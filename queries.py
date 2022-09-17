from readline import append_history_file
from date import *
from datetime import datetime
import pandas as pd

#start = "2022-09-15T00:00:00"
#end = "2022-09-15T23:59:59"

now = datetime.now()
start = now.strftime("%Y-%m-%d"+"T00:00:00")
end = now.strftime("%Y-%m-%d"+str("T23:59:59"))

startms = to_utc_ms(start)
endms = to_utc_ms(end)

sql = [
    ('transaction', 'transactionEntity', [
        {"$match": {"time": {"$gt": startms, "$lt": endms}}},
        {"$group": {
            "_id": '_id', "count": {"$count": {}}
        }}
    ], 'TransaccionesDíaActual'),

    ('trips', 'tripsCrudEntity', [
        {"$match": {'startDate': {"$gte": startms, "$lt": endms}}},
        {"$unwind": "$transits"},
        {"$group": {
            "_id": "$transits.transactionId", "count": {"$sum": 1}
        }
        },
        {"$match": {
            "count": {"$gt": 1}
        }
        }
    ], 'DuplicatedTransactions'),

    ('quarantine', 'quarantineEntity', [
        {"$group": {
            "_id": '$status', "conteo": {"$count": {}}
        }
        }
    ], 'Quarantine'),

    ('quarantine', 'quarantineEntity', [
        {"$match": {"concessionData.statusReason": "8"}},
        {"$group": {
            "_id": '$concessionData.statusReason', "SumaPorRazon": {"$count": {}}
        }
        }
    ], 'VideoWithoutImages'),

    ('trips', 'tripsCrudEntity', [
        {"$match": {'endDate': {"$gte": startms, "$lt": endms}}},
        {"$group": {
            "_id": '_id', "conteo": {"$count": {}}
        }
        }
    ], 'TripsCreatedXDia'),

    ('transaction', 'transactionEntity', [
        {"$match": {"status": 'PROCESSING'}},
        {"$group": {
            "_id": '$status', "count": {"$count": {}}
        }}
    ], 'TransactionProcessing'),

    ('transaction', 'validationWaitEntity', [
        {"$match": {"completedAndSentToPlateResolver": "false"}},
        {"$group": {
            "_id": '$status', "count": {"$count": {}}
        }}
    ], 'Trx Waiting Images'),

    ('trips', 'tripsCrudEntity', [
        {"$match": {"status": {"$in": ["TRIP_BUILT"]}}},
        {"$group": {
            "_id": '$status', "count": {"$count": {}}
        }
        }
    ], 'TripsEstatus'),

    ('trips', 'tripsCrudEntity', [
        {"$match": {"status": {"$in": ["TRIP_VALID"]}}},
        {"$group": {
            "_id": '$status', "count": {"$count": {}}
        }
        }
    ], 'TripsEstatus'),
]

df = pd.DataFrame(sql, columns=["database", "entity", "sql", "metric"])
print(df)
print("----------------------------------------------------------------------------")
