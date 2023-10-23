import re
import time
import random
from time import sleep
import os.path
import requests
from bs4 import BeautifulSoup
import json
import csv


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
    author_element = soup.find('span', class_="pl", string=re.compile(r'作者:'))
    if author_element is None:
        author_element = soup.find('span', class_="pl", string=re.compile(r'作者'))
        author = author_element.next_sibling.find_next('a').text.strip() if author_element else ""
    else:
        author = author_element.find_next('a').text.strip() if author_element else ""
    author = author.replace('\n', '').replace('\r', '').replace(' ', '')

    # 获取出版社
    press_elements = soup.find('span', string="出版社:")
    if press_elements:
        pressTry1 = press_elements.next_sibling.text
        pressTry1 = pressTry1.replace(' ', '').replace('\n', '').replace('\r', '')
        pressTry2 = press_elements.find_next_sibling().text
        pressTry2 = pressTry2.replace(' ', '').replace('\n', '').replace('\r', '')
        if pressTry1:
            press = pressTry1
        else:
            press = pressTry2
    else:
        press = ""

    # 获取原作名（仅外语书）
    originName_elements = soup.find('span', string="原作名:")
    originName = originName_elements.next_sibling.strip() if originName_elements else ""

    # 获取ISBN
    ISBN_elements = soup.find('span', string="ISBN:")
    ISBN = ISBN_elements.next_sibling.strip() if ISBN_elements else ""

    # 获取译者（仅外语书）
    translator_element = soup.find('span', class_="pl", string=re.compile(r'译者:'))
    if translator_element is None:
        translator_element = soup.find('span', class_="pl", string=re.compile(r'译者'))
        translator = translator_element.next_sibling.find_next('a').text.strip() if translator_element else ""
    else:
        translator = translator_element.find_next('a').text.strip() if translator_element else ""
    translator = translator.replace(' ', '').replace('\n', '').replace('\r', '')

    # 获取出版时间
    publishingTime_elements = soup.find('span', string="出版年:")
    publishingTime = publishingTime_elements.next_sibling.strip() if publishingTime_elements else ""

    # 获取图书页数
    pageCount_elements = soup.find('span', string="页数:")
    pageCount = pageCount_elements.next_sibling.strip() if pageCount_elements else ""

    # 获取定价
    price_elements = soup.find('span', string="定价:")
    price = price_elements.next_sibling.strip() if price_elements else ""

    # 获取书籍类型
    # genre_elements = soup.select('span[property="v:genre"]')
    # genres = [genre.text for genre in genre_elements]

    # 获取副标题
    subtitle_tags = soup.find('span', string="副标题:")
    subtitle = subtitle_tags.next_sibling.strip() if subtitle_tags else ""

    # 获取书籍简介
    full_summary_element = soup.find('span', class_='all hidden')
    if full_summary_element:
        summary = soup.find('span', class_='all hidden').get_text(strip=True)
    else:
        summary_element = soup.find('div', class_='intro')
        if summary_element:
            summary_element=summary_element.find('p')
        summary = summary_element.text.strip() if summary_element else ""
        summary = summary.replace("\n", "").replace(" ", "").replace('\r', '')

    # 将结果保存到文件
    with open(file_path, 'a', encoding='utf-8', newline="") as file:
        csv_writer = csv.writer(file)
        z = [
            book_id,
            title,
            subtitle,
            rating,
            author,
            press,
            originName,
            ISBN,
            translator,
            publishingTime,
            pageCount,
            price,
            summary
        ]
        csv_writer.writerow(z)
        # print("写入数据成功")
        file.close()


if __name__ == '__main__':
    # 调用函数并输入豆瓣书籍的ID和文件路径
    name = "Book_details.csv"
    cnt = 0
    with open(name, 'r', encoding='utf-8') as f:
        line = f.readline()
        while line:
            cnt = cnt+1
            line = f.readline()

    with open('Book_id.csv', 'r') as f:
        line = f.readline()
        while cnt > 0:
            cnt = cnt-1
            line = f.readline()
        while line:
            print(line)
            timeBegin = time.time()
            save_book_details(line[:-1], name)
            line = f.readline()
            timeEnd = time.time()
            gap = 5-(timeEnd-timeBegin) if 5-(timeEnd-timeBegin)>0 else 0
            sleep(gap+random.uniform(0, 5))
