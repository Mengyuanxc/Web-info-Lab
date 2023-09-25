import random
from time import sleep
import os.path
import requests
from bs4 import BeautifulSoup


def save_book_details(book_id, file_path):
    url = f'https://book.douban.com/subject/{book_id}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取书籍标题
    title_element = soup.select_one('h1 span[property="v:itemreviewed"]')
    title = title_element.text.strip() if title_element else ""

    # 获取书籍评分
    rating_element = soup.select_one('strong.ll.rating_num')
    rating = rating_element.text.strip() if rating_element else ""

    # 获取作者
    director_elements = soup.select('a[href*="author"]')
    directors = [director.text for director in director_elements]

    # 获取出版社
    actor_elements = soup.select('a[rel="v:starring"]')
    actors = [actor.text for actor in actor_elements]

    # 获取书籍类型
    genre_elements = soup.select('span[property="v:genre"]')
    genres = [genre.text for genre in genre_elements]

    # 获取出版日期
    release_date_element = soup.select_one('span[property="v:initialReleaseDate"]')
    release_date = release_date_element.text.strip() if release_date_element else ""

    # 获取书籍简介
    summary_element = soup.select_one('span[property="v:summary"]')
    summary = summary_element.text.strip() if summary_element else ""

    # 获取书籍定价
    price_element = soup.select_one('span[property="v:summary"]')
    price = price_element.text.strip() if price_element else ""

    # 将结果保存到文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('标题: ' + title + '\n')
        f.write('评分: ' + rating + '\n')
        f.write('导演: ' + ', '.join(directors) + '\n')
        f.write('演员: ' + ', '.join(actors) + '\n')
        f.write('类型: ' + ', '.join(genres) + '\n')
        f.write('上映日期: ' + release_date + '\n')
        f.write('简介: ' + summary + '\n')
        f.write('定价: ' + price + '\n')


if __name__ == '__main__':
# 调用函数并输入豆瓣电影的ID和文件路径
    with open('Book_id.csv', 'r') as f:
        line = f.readline()
        while line:
            name = 'details/book_details_'
            name += line[:-1]
            name += '.txt'
            print(line)
            if os.path.exists(name):
                line = f.readline()
                continue
            save_book_details(line[:-1], name)
            line = f.readline()
            sleep(random.randint(10,20))
