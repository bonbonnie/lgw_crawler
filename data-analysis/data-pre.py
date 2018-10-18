import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl
import os
path = os.path.abspath(os.path.dirname(os.getcwd()))

# 使matplotlib模块能显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号'-'

# 读取数据
positionlist = ['Java', 'PHP', 'C++', '区块链', 'Android', 'iOS', '数据挖掘', '深度学习', '自然语言处理', '机器学习',
                    '测试', 'html5', '技术总监', '架构师', '搜索算法', 'Python', 'UI设计师', '新媒体运营','产品经理', '市场营销', 'HR'
                    ]
for p in positionlist:
    df = pd.read_csv(path + '/gotcsv/lagou_jobs_{}.csv'.format(p), encoding='utf-8')


    # 数据清洗,剔除实习岗位
    df.drop(df[df['职位名称'].str.contains('实习')].index, inplace=True)
    # print(df.describe())

    # 将学历不限的职位要求认定为最低学历:大专
    df['学历要求'] = df['学历要求'].replace('不限', '大专')

    # 由于CSV文件内的数据是字符串形式,先用正则表达式将字符串转化为列表,再取区间的均值
    pattern = '\d+'

    df['工作年限'] = df['工作经验'].str.findall(pattern)
    avg_work_year = []
    for i in df['工作年限']:
        # 如果工作经验为'不限'或'应届毕业生',那么匹配值为空,工作年限为0
        if len(i) == 0:
            avg_work_year.append(0)
        # 如果匹配值为一个数值,那么返回该数值
        elif len(i) == 1:
            avg_work_year.append(int(''.join(i)))
        # 如果匹配值为一个区间,那么取平均值
        else:
            num_list = [int(j) for j in i]
            avg_year = sum(num_list)/2
            avg_work_year.append(avg_year)
    df['经验'] = avg_work_year

    # 将字符串转化为列表,再取区间的前25%，比较贴近现实
    df['salary'] = df['工资'].str.findall(pattern)
    avg_salary = []
    for k in df['salary']:
        # 如果工资为一个值，那么取该值
        if len(k) == 1:
            avg_salary.append(int(''.join(k)))
        # 如果公司规模匹配值为一个区间,那么取平均值
        else:
            int_list = [int(n) for n in k]
            avg_wage = int_list[0]+(int_list[1]-int_list[0])/4
            avg_salary.append(avg_wage)
    df['月工资'] = avg_salary

    df['works'] = df['公司规模'].str.findall(pattern)
    avg_works = []
    for k in df['works']:
        # 如果没有相应的数字表示
        if len(i) == 0:
            avg_works.append(0)
        # 如果公司规模为一个数表示，那么取该值
        elif len(k) == 1:
            avg_works.append(int(''.join(k)))
        # 如果公司规模匹配值为一个区间,那么取平均值
        else:
            num_list = [int(j) for j in k]
            avg_people = sum(num_list) / 2
            avg_works.append(avg_people)
    df['公司人数'] = avg_works

    # 将清洗后的数据保存,以便检查
    df.to_csv(path + '/cleared/{}-pred.csv'.format(p), index = False)

    # 描述统计
    # with open('jobdescripton.txt', 'a', encoding='utf-8') as f:
    #     f.write('{}工资描述：\n{}'.format(p, df['月工资'].describe()) + '\n')
    # print('{}工资描述：\n{}'.format(p, df['月工资'].describe()))




#/Users/kevin/git/lgw_crawler/gotcsv
