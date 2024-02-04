from typing import Any
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
import json
import re

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

def get_manga_json(soup:BeautifulSoup):
    scripts = soup.find_all('script')
    input_text = ''
    for script in scripts:
        if 'window.__DATA__' in script.text:
            input_text = script.text
            break
    pattern = r"window.__DATA__ = \{(.+)\};.*?window._SITE_COLOR_"
    match = re.search(pattern, input_text, re.DOTALL)
    assert match is not None
    if match:
        json_data = json.loads('{'+match.group(1).strip()+'}')
    else:
        json_data = None
    assert json_data is not None
    if isinstance(json_data, dict):
        return json_data
    else:
        raise

def add_json_data(result_data:dict[str, Any], manga_json:dict[Any, Any]):
    result_data.setdefault('rus_name', None)
    result_data.setdefault('eng_name', None)
    result_data.setdefault('slug', None)
    result_data.setdefault('status', None)
    try:
        manga = manga_json.get('manga', None)
        assert isinstance(manga, dict)
        result_data['rus_name'] = manga.get('rusName', None)
        result_data['eng_name'] = manga.get('engName', None)
        result_data['slug'] = manga.get('slug', None)
        result_data['status'] = manga.get('status', None)
        return True
    except AssertionError:
        return False
    
def add_translators(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('translators', [])
    try:
        team_list = soup.find('div', {'class':'team-list'})
        assert isinstance(team_list, Tag)
        teams = team_list.find_all('a')
        for team in teams:
            team_data = {}
            team_data.setdefault('href', None)
            team_data.setdefault('img', None)
            team_data.setdefault('name', None)
            team_data['href'] = team.get('href', None)
            div = team.find('div')
            if isinstance(div, Tag):
                style = div.get('style', None)
                if isinstance(style, str):
                    url = re.search(r"\(.*?\)", style)
                    if isinstance(url, re.Match):
                        team_data['img'] = url[0][1:-2]
            team_data['name'] = team.text.replace('\n', '')
            result_data['translators'].append(team_data)

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
    assert add_translators(result_data, soup)
    manga_json = get_manga_json(soup)
    assert add_json_data(result_data, manga_json)
    
    
    
    print(json.dumps(result_data, indent=4, ensure_ascii=False))
    print('---'*10)
    #print(json.dumps(get_manga_json(soup), indent=4, ensure_ascii=False))
    
    
manga_html_parser(data)