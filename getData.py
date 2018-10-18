import csv
import os
import numpy as np
from pymongo import MongoClient
import pandas as pd

client = MongoClient('localhost', 27017)
db = client.lagou
table = db.position

# 读取数据
data = pd.DataFrame(list(table.find()))

# 选择需要显示的字段
data = data[['companyFullName', 'longitude', 'latitude']]

print(len(data))
print(data)

data.to_csv('my_csv.csv', mode='a', header=False)
