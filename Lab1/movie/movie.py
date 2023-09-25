import random
from time import sleep
import os.path
import requests
from bs4 import BeautifulSoup
import json


def save_movie_details(movie_id, file_path):
    url = f'https://movie.douban.com/subject/{movie_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取电影标题
    title_element = soup.select_one('h1 span[property="v:itemreviewed"]')
    title = title_element.text.strip() if title_element else ""

    # 获取电影评分
    rating_element = soup.select_one('strong.ll.rating_num')
    rating = rating_element.text.strip() if rating_element else ""

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
    # 将结果保存到文件
    with open(file_path, 'w', encoding='utf-8') as file:
        movie_details = {
            "title": title,
            "rating": rating,
            "directors": directors,
            "actors": actors,
            "genres": genres,
            "release_date": release_date,
            "summary": summary
        }
        movie_details_json = json.dumps(movie_details, ensure_ascii=False)
        file.write(movie_details_json)


if __name__ == '__main__':
# 调用函数并输入豆瓣电影的ID和文件路径
    with open('Movie_id.csv', 'r') as f:
        line = f.readline()
        while line:
            name = 'details/movie_details_'
            name += line[:-1]
            name += '.json'
            print(line)
            if os.path.exists(name):
                line = f.readline()
                continue
            save_movie_details(line[:-1], name)
            line = f.readline()
            sleep(random.randint(10, 20))
