#encoding = utf-8

import csv
import os
import numpy as np
from pymongo import MongoClient

def getallfiles():
    path = os.path.abspath(os.getcwd())+ '/cleared/'
    lines = []
    for c in os.listdir(path):
        if c.endswith('.csv'):
            lines.append(os.path.join(path, c))
    return lines




def readCSV(path):
    # global workData
    # 改变CSV的名字就可以把单个CSV写入MongoDB了
    workData = []
    with open(path) as csvfile:
        csv_reader = csv.reader(csvfile)  # 使用csv.reader读取csvfile中的文件
        work_header = next(csv_reader)  # 读取第一行每一列的标题
        # print(work_header)
        for row in csv_reader:  # 将csv 文件中的数据保存到birth_data中
            # print(row)
            workData.append(row)

    return workData
    # print(workData[0])
    # workData = np.array(workData)  # 将list数组转化成array数组便于查看数据结构
    # work_header = np.array(work_header)
    # print(workData.shape)  # 利用.shape查看结构。
    # print(workData[0])  # 利用.shape查看结构。
    #
    # print(work_header.shape)


def storeToMongoDB():
    pass




if __name__ == '__main__':
    count = 0
    client = MongoClient('localhost', 27017)
    db = client.lagou
    con = db.position
    csvPath = getallfiles()
    print(len(csvPath))
    for path in csvPath:

        workData = readCSV(path)
        for item in workData:
            count += 1
            # print(item)
            # print(len(item))

            # for value in item:
            #     print(value)
            # i = 0
            # for i in range(len(item)):
            #     print(item[i])
            data = {
                'companyFullName': item[0],
                'companyShortName': item[1],
                'companySize': item[2],
                'financeStage': item[3],
                'district': item[4],
                'positionName': item[5],
                'workYear': item[6],
                'education': item[7],
                'salary': item[8],
                'positionAdvantage': item[9],
                'longitude': item[10],
                'latitude': item[11],
                'crearedWorkYear': item[12],
                'crearedJinyan': item[13],
                'crearedSalary': item[14],
                'crearedYueGongZi': item[15],
                'crearedCompanySize': item[16],
                'crearedRenShu': item[17]
            }
            con.insert(data)
    print('总计写入{}条数据'.format(count))
