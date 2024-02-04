from typing import Any
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
import json


with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\test.txt', 'r', encoding='utf-8') as f:
    data = '\n'.join(f.readlines())


def add_img(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('img', None)
    try:
        div = soup.find('div', {'class': 'media-sidebar__cover paper'})
        assert isinstance(div, Tag)
        img = div.find('img')
        assert isinstance(img, Tag)
        result_data['img'] = img.get('src', None)
        return True
    except AssertionError:
        result_data['img'] = None
        return False
def add_tags(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('tags', [])
    try:
        div = soup.find('div', {'class': 'media-tags'})
        assert isinstance(div, Tag)
        tags = div.find_all('a', {'class':'media-tag-item'})
        for tag in tags:
            result_data.setdefault('tags', []).append(tag.text)
        return True
    except AssertionError:
        result_data.setdefault('tags', [])
        return False  
def add_description(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('description', None)
    try:
        description = soup.find('div', {'class': 'media-description__text'})
        assert isinstance(description, Tag)
        result_data['description'] = description.text
        return True
    except AssertionError:
        result_data['description'] = None
        return False
def add_info_list(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('type', None) # Тип
    result_data.setdefault('release_year', None) # Год релиза
    result_data.setdefault('title_status', None) # Статус тайтла
    result_data.setdefault('transfer_status', None) # Статус перевода
    result_data.setdefault('author', None) # Автор
    result_data.setdefault('artist', None) # Художник
    result_data.setdefault('publishing_house', None) # Издательство
    result_data.setdefault('age_rating', None) # Возрастной рейтинг
    result_data.setdefault('chapters_uploaded', None) # Загружено глав
    result_data.setdefault('alternative_names', []) # Альтернативные названия
    try:
        info_list = soup.find('div', {'class': 'media-info-list paper'})
        assert isinstance(info_list, Tag)
        for tag in info_list.find_all('a', {'class':'media-info-list__item'}):
            title = tag.find('div', {'class': 'media-info-list__title'})
            value = tag.find('div', {'class': 'media-info-list__value'})
            if (title is None or value is None): continue
            match title.text:
                case 'Тип':
                    result_data['type'] = value.text
                case 'Год релиза':
                    result_data['release_year'] = value.text
                case 'Статус тайтла':
                    result_data['title_status'] = value.text
                case 'Статус перевода':
                    result_data['transfer_status'] = value.text
                case 'Возрастной рейтинг':
                    result_data['age_rating'] = value.text
        for tag in info_list.find_all('div', {'class':'media-info-list__item'}):
            tag:Tag
            title = tag.find('div', {'class': 'media-info-list__title'})
            value = tag.find('div', {'class': 'media-info-list__value'})
            if (title is None or value is None): continue
            a = value.find('a')
            if isinstance(a, Tag):
                match title.text:
                    case 'Автор':
                        result_data['author'] = a.get('href', None)
                    case 'Художник':
                        result_data['artist'] = a.get('href', None)
                    case 'Издательство':
                        result_data['publishing_house'] = a.get('href', None)
            else:
                match title.text:
                    case 'Загружено глав':
                        result_data['chapters_uploaded'] = int(value.text)
                    case 'Альтернативные названия':
                        if isinstance(value, Tag):
                            for div in value.find_all('div', {'class':''}):
                                result_data.setdefault('alternative_names', []).append(div.text)
        return True
    except AssertionError:
        return False
def add_href(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('href', None)
    try:
        #<meta property="og:site_name" content="https://mangalib.me/adabana">
        meta = soup.find('meta', {'property':'og:site_name'})
        assert isinstance(meta, Tag)
        result_data['href'] = meta.get('content', None)
        return True
    except AssertionError:
        return False
    
def manga_html_parser(html_text:str):
    soup = BeautifulSoup(html_text, 'html.parser')
    result_data = {}

    assert add_img(result_data, soup)
    assert add_tags(result_data, soup)
    assert add_description(result_data, soup)
    assert add_info_list(result_data, soup)
    assert add_href(result_data, soup)
    print(json.dumps(result_data, indent=4, ensure_ascii=False))

    
    
manga_html_parser(data)