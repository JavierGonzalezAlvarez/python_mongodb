from conexion import *
from queries import *
import pandas as pd

date = datetime.now()
new_date = date.strftime("%Y-%m-%d %H:%M:%S")

client = get_client()
for i in range(len(df)):
    database = df.iloc[i]["database"]
    entity = df.iloc[i]["entity"]
    myquery = df.iloc[i]["sql"]
    metric = df.iloc[i]["metric"]
    print(database, "-", entity, "-", myquery)
    collection = client[database][entity]
    try:
        #mydoc = list(collection.find(myquery))
        mydoc = list(collection.aggregate(myquery))
        if len(mydoc) > 0:
            df_csv = pd.DataFrame(mydoc)
            df_csv["date"] = new_date
            df_csv["metric"] = metric
            df_csv = df_csv.replace(["_id"], "")
            print("data saved")
        else:
            df_csv = pd.DataFrame(mydoc)
            new_row = {'_id': '', 'value': '',
                       'date': new_date, 'metrics': metric}
            df_csv = df_csv.append(new_row, ignore_index=True)
            print("no data")

        df_csv.to_csv("sql.csv", header=False, mode='a', index=False)
    except Exception as e:
        print("error on file: ", type(e))
    print("--------------------------------------")
