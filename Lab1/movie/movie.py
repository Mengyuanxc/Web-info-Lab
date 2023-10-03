import random
from time import sleep
import os.path
import requests
from bs4 import BeautifulSoup
import json
import csv

def save_movie_details(movie_id, file_path):
    url = f'https://movie.douban.com/subject/{movie_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取电影标题
    chinese_title = soup.title.get_text().strip()[:-5]
    title_element = soup.select_one('h1 span[property="v:itemreviewed"]')
    title = title_element.text.strip() if title_element else ""

    # 获取电影评分
    rating_element = soup.select_one('strong.ll.rating_num')
    rating = rating_element.text.strip() if rating_element else "无"
    if(rating!="无"):
        rating = float(rating)

    # 获取导演
    director_elements = soup.select('a[rel="v:directedBy"]')
    directors = [director.text for director in director_elements]

    # 获取演员
    actor_elements = soup.select('a[rel="v:starring"]')
    actors = [actor.text for actor in actor_elements]

    # 获取电影类型
    genre_elements = soup.select('span[property="v:genre"]')
    genres = [genre.text for genre in genre_elements]

    # 获取上映日期
    release_date_element = soup.select_one('span[property="v:initialReleaseDate"]')
    release_date = release_date_element.text.strip() if release_date_element else ""

    # 获取电影简介
    # summary_element = soup.select_one('span[property="v:summary"]')
    # summary = summary_element.text.strip() if summary_element else ""
    full_summary_element = soup.find('span', class_='all hidden')
    if(full_summary_element):
        summary = soup.find('span', class_='all hidden').get_text(strip=True)
    else:
        summary_element = soup.select_one('span[property="v:summary"]')
        summary = summary_element.text.strip() if summary_element else ""
        summary = summary.replace("\n", "").replace(" ", "")

    # 喜欢这部电影的人也喜欢...
    recommendation_list = []
    recommendation_element = soup.find('div', class_='recommendations-bd')
    dl_tags = recommendation_element.find_all('dl') if recommendation_element else ""
    for dl in dl_tags:
        dd_tag = dl.find('dd')
        a_tag = dd_tag.find('a')
        recommendation_movie_name = a_tag.get_text()
        recommendation_list.append(recommendation_movie_name)

    # 将结果保存到文件
    with open(file_path, 'a', encoding='utf-8',newline="") as file:
        # 2. 基于文件对象构建 csv写入对象
        csv_writer = csv.writer(file)
        # 4. 写入csv文件内容
        z = [
            movie_id,
            chinese_title,
            title,
            rating,
            directors,
            actors,
            genres,
            release_date,
            summary,
            recommendation_list
        ]
        csv_writer.writerow(z)
        print("写入数据成功")
        # 5. 关闭文件
        file.close()


if __name__ == '__main__':
# 调用函数并输入豆瓣电影的ID和文件路径
    name = "Movie_details.csv"
    cnt = 0
    with open(name, 'r', encoding='utf-8') as f:   #跳过已经爬下的部分
        line = f.readline()
        while(line):
            cnt+= 1
            line = f.readline()

    with open('Movie_id.csv', 'r') as f:        #根据ID爬取对应电影
        line = f.readline()
        while(cnt>0):
            cnt-=1
            line = f.readline()
        while line:
            print(line)
            save_movie_details(line[:-1], name)
            line = f.readline()
            #sleep(random.randint(20, 40))
