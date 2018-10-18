import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from wordcloud import WordCloud
from scipy.misc import imread
import jieba


# 读取数据
df = pd.read_csv('data-pred.csv', encoding='utf-8')

# 绘制词云,将职位福利中的字符串汇总
text = ''
for line in df['职位福利']:
    text += line
# 使用jieba模块将字符串分割为单词列表
cut_text = ' '.join(jieba.cut(text))
color_mask = imread('cloud.jpg')  #设置背景图
cloud = WordCloud(
        font_path='yahei.ttf',
        background_color='white',
        mask=color_mask,
        max_words=1000,
        max_font_size=100
        )

word_cloud = cloud.generate(cut_text)
# 保存词云图片
word_cloud.to_file('word_cloud.jpg')
plt.imshow(word_cloud)
plt.axis('off')
plt.show()


# 学历分为大专\本科\硕士,将它们设定为虚拟变量
dummy_edu = pd.get_dummies(df['学历要求'], prefix='学历')
# 构建回归数组
df_with_dummy = pd.concat([df['月工资'], df['经验'], dummy_edu], axis=1)

# 建立多元回归模型
y = df_with_dummy['月工资']
X = df_with_dummy[['经验', '学历_大专', '学历_本科', '学历_硕士']]
X=sm.add_constant(X)
model = sm.OLS(y,X)
results = model.fit()
print('回归方程的参数：\n{}\n'.format(results.params))
print('回归结果：\n{}'.format(results.summary()))

