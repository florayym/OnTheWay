from geopy.distance import geodesic
from datetime import date
from aip import AipNlp
from ..models import Store
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import jieba
import os


def calDistance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).m


def recommend(latitude, longitude):
    stores = Store.query.all()
    recommend_list = list()
    for store in stores:
        dis = calDistance(latitude, longitude, store.latitude, store.longtitude)
        if dis <= 2000:
            recommend_list.append(
                {
                    'img_url': store.img_url,
                    'store': store.storename,
                    'score': store.score,
                    'distance': dis,
                }
            )
    return recommend_list


def mark(comment):
    try:
        APP_ID = '15797847'
        API_KEY = 'Ciya2SWNN1i9ti3UZKXkaQxD'
        SECRET_KEY = 'hNjCqO6PBHCe7iGvId34v2Q5e5v9oYBN'
        client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
        result = client.sentimentClassify(comment)
        score = result['items'][0]['positive_prob']
        score = score * 10 - 5
    except ConnectionError as e:
        return None
    return score


def birth(birthday):
    tmp = birthday.split('-')
    return date(int(tmp[0]), int(tmp[1]), int(tmp[2]))


def stop_words_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def generate_word_cloud(store):
    # 加载自定义词典
    # jieba.load_userdict('userdict.txt')
    stop_words = stop_words_list('./tmp/stop_words.txt')
    sentence = ''
    for comment in store.comments:
        sentence += str(comment.comment).strip()
    sentence_depart = jieba.cut(sentence)
    out_str = ''
    for word in sentence_depart:
        if word not in stop_words:
            if word != '\t':
                out_str += word
                out_str += " "

    back_coloring_path = "./static/images/word_cloud/background.jpg"  # 随意准备一张图片，用来设置词云形状
    back_coloring = imread(back_coloring_path)  # 读取图片
    # tags = analyse.extract_tags(out_str, topK=15, withWeight=False)  # 关键词提取 topK=100 提取TF-IDF权重最大的前100个关键词
    # text = " ".join(tags)
    # print(text)
    w = WordCloud(background_color='white',
                          width=2000,
                          height=1000,
                          margin=2,
                          max_words=30,  # 设置最多显示的词数
                          mask=back_coloring,  # 设置词云形状
                          font_path="./static/images/word_cloud/msyh.ttc",  # 中文词图必须设置字体格式，否则会乱码，这里加载的是黑体
                          random_state=10)  # 设置有多少种随机生成状态，即有多少种配色方案
    word_cloud = w.generate(out_str)  # 传入需画词云图的文本
    plt.imshow(word_cloud)
    plt.axis('off')
    # if not os.path.exists('./static/images/word_cloud/{}.jpg'.format(store.id)):
    #     os.mkdir('./static/images/word_cloud/{}.jpg'.format(store.id))
    plt.savefig('./static/images/word_cloud/stores/{}.png'.format(store.id))
