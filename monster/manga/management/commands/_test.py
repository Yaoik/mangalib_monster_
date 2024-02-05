import django.shortcuts
from typing import Any
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag
import json
import re

with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\test1.txt', 'r', encoding='utf-8') as f:
    data = '\n'.join(f.readlines())

def style_to_href(style:str):
    assert isinstance(style, str)
    href = re.search(r"\(.*?\)", style)
    if isinstance(href, re.Match):
        return href[0][1:href[0].index(')')].replace('?', '')
    return False

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
        result_data['description'] = description.text.replace('\n', '').strip()
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
    
def add_teams(result_data:dict[str, Any], soup:BeautifulSoup, manga_json:dict[Any, Any]):
    result_data.setdefault('teams', [])
    try:
        team_list = soup.find('div', {'class':'team-list'})
        assert isinstance(team_list, Tag)
        teams = team_list.find_all('a')
        for team in teams:
            team_data = {}
            team_data.setdefault('href', None)
            team_data.setdefault('img', None)
            team_data['href'] = team.get('href', None)
            div = team.find('div')
            if isinstance(div, Tag):
                style = div.get('style', None)
                if isinstance(style, str):
                    team_data['img'] = style_to_href(style)
                    assert team_data['img']
            for team_json in manga_json.get('chapters', {}).get('teams', []):
                print(team_json)
                if team_json.get('href', None) == team_data['href']:
                    team_data.update(team_json)
            result_data['teams'].append(team_data)
        return True
    except AssertionError:
        return False
    
def add_chapters(result_data:dict[str, Any], manga_json:dict[Any, Any]):
    result_data.setdefault('chapters', [])
    try:
        for chapter in manga_json.get('chapters', {}).get('list', []):
            result_data['chapters'].append(chapter)
        return True
    except AssertionError:
        return False
    
def add_in_lists(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('in_lists', {})
    result_data.setdefault('user_ratings', {})
    result_data['user_ratings'].setdefault('value', None)
    result_data['user_ratings'].setdefault('total', None)
    result_data['user_ratings'].setdefault('scores', {})
    try:
        div = soup.find('div', {'class':'media-section__col'})
        assert isinstance(div, Tag)
        div = div.find('div', {'class':'media-section__head'})
        assert isinstance(div, Tag)
        div = div.find('div', {'class':'media-section__title'})
        assert isinstance(div, Tag)
        mat = re.search(r'\d+', div.text)
        assert isinstance(mat, re.Match)
        text = int(mat.group())
        result_data['in_lists']['all'] = text
        div: Tag | NavigableString | None = soup.find('div', {'class':'media-stats'})
        assert isinstance(div, Tag)
        divs = div.find_all('div', {'class':'media-stats-item'})
        for div in divs:
            assert isinstance(div, Tag)
            title = div.find('div', {'class':'media-stats-item__column media-stats-item__title'})
            value = div.find('div', {'class':'media-stats-item__column media-stats-item__count'})
            assert isinstance(title, Tag) and isinstance(value, Tag)
            match title.text:
                case 'Читаю':
                    result_data['in_lists']['reading'] = int(value.text)
                case 'В планах':
                    result_data['in_lists']['in_plans'] = int(value.text)
                case 'Брошено':
                    result_data['in_lists']['abandoned'] = int(value.text)
                case 'Прочитано':
                    result_data['in_lists']['read'] = int(value.text)
                case 'Любимые':
                    result_data['in_lists']['favorites'] = int(value.text)
                case 'Другое':
                    result_data['in_lists']['other'] = int(value.text)
        lists = result_data['in_lists']
        res = lists['other']+lists['favorites']+lists['read']+lists['abandoned']+lists['in_plans']+lists['reading']
        assert res == lists['all']
        
        div = soup.find('div', {'class':'media-rating__value'})
        assert isinstance(div, Tag)
        result_data['user_ratings']['value'] = float(div.text)
        divs = soup.find_all('div', {'class':'media-section__col'})
        for div in divs:
            assert isinstance(div, Tag)
            title = div.find('div', {'class':'media-section__title'})
            assert isinstance(title, Tag)
            if title.text == 'Оценки пользователей':
                div = div
                break
        assert isinstance(div, Tag)
        divs = div.find('div', {'class':'media-stats'})
        assert isinstance(divs, Tag)
        for div in divs.find_all('div', {'class':'media-stats-item'}):
            assert isinstance(div, Tag)
            span = div.find('span')
            assert isinstance(span, Tag)
            title = span.text
            value = div.find('div', {'class':'media-stats-item__column media-stats-item__count'})
            assert isinstance(value, Tag)
            mat = re.search(r'\d+', value.text)
            assert isinstance(mat, re.Match)
            value = int(mat.group())
            result_data['user_ratings'].setdefault('scores', {})[int(title)] = value
        result_data['user_ratings']['total'] = sum(val for val in result_data['user_ratings'].get('scores', {}).values())
        return True
    except AssertionError:
        return False

def add_related(result_data:dict[str, Any], soup:BeautifulSoup):
    result_data.setdefault('related', [])
    result_data.setdefault('similar', [])
    try:
        div = soup.find('div', {'data-slider':'related'})
        if isinstance(div, Tag):
            divs = div.find_all('div', {'class':'media-slider__item'})
            for div in divs:
                assert isinstance(div, Tag)
                a: Tag | NavigableString | None = div.find('a')
                assert isinstance(a, Tag)
                a_data = {}
                a_data.setdefault('href', a.get('href', None))
                a_data.setdefault('title', a.get('title', None))
                a_div = a.find('div', {'class':'manga-list-item__cover'})
                assert isinstance(a_div, Tag)
                a_data.setdefault('img', style_to_href(str(a_div.get('style', ''))))
                head = div.find('div', {'class':'manga-list-item__head'})
                name = div.find('div', {'class':'manga-list-item__name'})
                meta = div.find('div', {'class':'manga-list-item__meta'})
                assert isinstance(head, Tag)
                assert isinstance(name, Tag)
                assert isinstance(meta, Tag)
                a_data.setdefault('head', head.text.replace('\n', '').strip())
                a_data.setdefault('name', name.text.replace('\n', '').strip())
                m_type, m_status, *_ = meta.find_all('span')
                a_data.setdefault('type', m_type.text.replace('\n', '').strip())
                a_data.setdefault('status', m_status.text.replace('\n', '').strip())
                result_data['related'].append(a_data)
                
        div = soup.find('div', {'data-slider':'similar'})
        if isinstance(div, Tag):
            divs = div.find_all('div', {'class':'media-slider__item media-slider__item_rate'})
            for div in divs:
                assert isinstance(div, Tag)
                a = div.find('a')
                assert isinstance(a, Tag)
                a_data = {}
                a_data.setdefault('href', a.get('href', None))
                a_data.setdefault('title', a.get('title', None))
                a_div = a.find('div', {'class':'manga-list-item__cover'})
                assert isinstance(a_div, Tag)
                a_data.setdefault('img', style_to_href(str(a_div.get('style', ''))))
                head = div.find('div', {'class':'manga-list-item__head'})
                name = div.find('div', {'class':'manga-list-item__name'})
                rating = a.find('div', {'class':'media-similar-rating__value'})
                assert isinstance(head, Tag)
                assert isinstance(name, Tag)
                assert isinstance(rating, Tag)
                a_data.setdefault('head', head.text.replace('\n', '').strip())
                a_data.setdefault('name', name.text.replace('\n', '').strip())
                a_data.setdefault('rating', int(rating.text.replace('\n', '').strip()))
                result_data['similar'].append(a_data)
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
    manga_json = get_manga_json(soup)
    assert add_teams(result_data, soup, manga_json)
    assert add_json_data(result_data, manga_json)
    assert add_chapters(result_data, manga_json)
    assert add_in_lists(result_data, soup)
    assert add_related(result_data, soup)
    
    with open('C:\\Users\\Shamrock\\Desktop\\mangalib_monster обход блокировки ботов\\monster\\manga\\management\\commands\\manga_json.json', 'w+', encoding='UTF-8') as f:
        f.write(json.dumps(result_data, indent=4, ensure_ascii=False))
    print(json.dumps(result_data, indent=4, ensure_ascii=False))
    #print('---'*10)
    #print(json.dumps(get_manga_json(soup), indent=4, ensure_ascii=False))
    
    
manga_html_parser(data)