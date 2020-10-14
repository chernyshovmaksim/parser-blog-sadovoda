import requests
import csv
from bs4 import BeautifulSoup



HOST    = 'https://web.archive.org/web/20160610111630/http://www.blog-sadovoda.ru/'
URL     = 'https://web.archive.org/web/20160610111630/http://www.blog-sadovoda.ru/category/blogoustrojstvo/'
HEADERS = {
    'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Atom/8.1.0.31 Safari/537.36'
} 

posts_links = []
posts       = []

def get_html(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='post')

    for item in items:
        posts_links.append(
            item.find('h2').find('a').get('href')
        )




def parser_links():
    html = get_html(URL)
    if html.status_code == 200:
        print("Status: " + str(html.status_code))
        
        page = BeautifulSoup(html.text, 'html.parser')
        get_content(html.text)
        print(f'Спарсили ссылки с главной страницы ✅')

        next_link = page.find('div', class_='nav-next').find('a')

        if next_link:
            for i in range(2, int(MAX_PAGES)):
                page_in_pagination = get_html(URL + f'page/{i}/')
                if page_in_pagination.status_code == 200:
                    get_content(page_in_pagination.text)
                    print(f'Спарсили ссылки со страницы: {i} ✅')
                else:
                    break
            print('Сбор ссылок окончен')

    else:
        print("Status: " + str(html.status_code))



def parser_contents():
    i = 0
    for link in posts_links:
        html = get_html(HOST + link)
        soup = BeautifulSoup(html.text)

        # POST TITLE
        if soup.find('div', class_='entry').find('h2'):
            post_title = soup.find('div', class_='entry').find('h2').get_text(strip=True)
        else:
            post_title = soup.find('div', class_='entry').find('h1').get_text(strip=True)

        # POST CONTENT
        post_content = soup.find('div', class_='post-content')
        if post_content.find('div', class_='crp_related'):
            post_content.find('div', class_='crp_related').decompose()
        if post_content.find('div', class_='likes'):
            post_content.find('div', class_='likes').decompose()
        if post_content.find_all('script'):
            for script in post_content.find_all('script'):
                script.decompose()
        if post_content.find('div', id='ya_direct'):
            post_content.find('div', id='ya_direct').decompose()
        if post_content.find('h3', class_='related_post_title'):
            post_content.find('h3', class_='related_post_title').decompose()
        if post_content.find('ul', class_='related_post'):
            post_content.find('ul', class_='related_post').decompose()
        if post_content.find_all('div', class_='yashare-auto-init'):
            for el in post_content.find_all('div', class_='yashare-auto-init'):
                el.decompose()

        posts.append({
            'title'   : post_title,
            'content' : post_content 
        })

        i = i + 1
        print(f'Страница #{i} - {post_title} ✔️✔️✔️')


if __name__ == "__main__":
    MAX_PAGES = input('Укажите максимальное колличество страниц для парсинга  -  ')
    parser_links()
    parser_contents()
    print(posts)
    
